"""
Custom filters for the chats application.
"""
import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Message, Conversation, User


class MessageFilter(filters.FilterSet):
    """
    Filter for Message model.
    
    Allows filtering messages by:
    - sender: Filter by sender's username
    - content: Filter by message body containing text
    - sent_after: Filter by sent_at date after specified date
    - sent_before: Filter by sent_at date before specified date
    - is_read: Filter by read status
    """
    sender = django_filters.CharFilter(field_name='sender__username')
    content = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    is_read = django_filters.BooleanFilter(field_name='is_read')
    
    class Meta:
        model = Message
        fields = ['sender', 'content', 'sent_after', 'sent_before', 'is_read']


class ConversationFilter(filters.FilterSet):
    """
    Filter for Conversation model.
    
    Allows filtering conversations by:
    - participant: Filter by participant's username
    - title: Filter by conversation title containing text
    - created_after: Filter by created_at date after specified date
    - is_group: Filter by group status
    """
    participant = django_filters.CharFilter(method='filter_participant')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    is_group = django_filters.BooleanFilter(field_name='is_group')
    
    class Meta:
        model = Conversation
        fields = ['participant', 'title', 'created_after', 'is_group']
    
    def filter_participant(self, queryset, name, value):
        """
        Filter conversations by participant username.
        
        Args:
            queryset: Base queryset
            name: Field name
            value: Filter value
            
        Returns:
            Filtered queryset
        """
        try:
            # Find user by username
            user = User.objects.get(username=value)
            return queryset.filter(participants=user)
        except User.DoesNotExist:
            # Return empty queryset if user doesn't exist
            return queryset.none()
