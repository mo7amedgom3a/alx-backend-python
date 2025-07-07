from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Max
from django.utils import timezone
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer, 
    UserSerializer
)
from .permissions import IsParticipantOfConversation, IsOwner, IsAuthenticatedForAPI


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling conversations.
    Provides CRUD operations and additional actions for conversation management.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedForAPI, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'participants__username']
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """
        Get conversations where the current user is a participant.
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        """
        Create a new conversation and add the current user as a participant.
        """
        conversation = serializer.save()
        if not conversation.participants.filter(id=self.request.user.id).exists():
            conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Add a participant to an existing conversation.
        """
        conversation = self.get_object()
        # Check if the requester is a participant in the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "Only participants can add users to this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'participant added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def leave_conversation(self, request, pk=None):
        """
        Remove the current user from the conversation.
        """
        conversation = self.get_object()
        conversation.participants.remove(request.user)
        return Response({'status': 'left conversation'}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling messages within conversations.
    Provides endpoints for sending, reading, and managing messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedForAPI, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """
        Get messages for a specific conversation.
        Filter by conversation_id from URL parameters.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).select_related('sender')

    def perform_create(self, serializer):
        """
        Create a new message in the conversation.
        Automatically set the sender as the current user.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        
        # Verify user is a participant
        if not conversation.participants.filter(id=self.request.user.id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
        
        # Update conversation's last activity
        conversation.updated_at = timezone.now()
        conversation.save()

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None, conversation_pk=None):
        """
        Mark a message as read.
        """
        message = self.get_object()
        message.mark_as_read()
        return Response({'status': 'message marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request, conversation_pk=None):
        """
        Mark all messages in a conversation as read.
        """
        messages = self.get_queryset().filter(is_read=False).exclude(sender=request.user)
        messages.update(is_read=True, read_at=timezone.now())
        return Response({'status': 'all messages marked as read'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user profiles.
    Read-only access to prevent unauthorized modifications.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedForAPI]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update the current user's profile.
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def handle_permission_denied(self, request):
        """
        Handle permission denied errors with a proper 403 response.
        """
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )
