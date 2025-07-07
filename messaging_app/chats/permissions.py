"""
Custom permissions for the chats application.
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow owners of an object to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object.
        
        Args:
            request: Request object
            view: View object
            obj: Object to check permissions for
            
        Returns:
            bool: True if the user is the owner, False otherwise
        """
        # If the object has a user attribute, check that
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # If the object has a sender attribute (for messages), check that
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        # Default to False
        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission to only allow participants of a conversation to access it.
    Participants can send, view, update, and delete messages in conversations they are part of.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has permission for this request.
        This is called on every request before checking object permissions.
        
        Args:
            request: Request object
            view: View object
            
        Returns:
            bool: True if the user is authenticated, False otherwise
        """
        # First check if the user is authenticated
        if not (request.user and request.user.is_authenticated):
            return False
            
        # For methods that modify data, we need additional checks
        if request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            # For nested routes with conversation_pk
            if hasattr(view, 'kwargs') and 'conversation_pk' in view.kwargs:
                from .models import Conversation
                try:
                    conversation = Conversation.objects.get(
                        conversation_id=view.kwargs['conversation_pk']
                    )
                    return request.user in conversation.participants.all()
                except Conversation.DoesNotExist:
                    return False
                    
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        
        Args:
            request: Request object
            view: View object
            obj: Object to check permissions for
            
        Returns:
            bool: True if the user is a participant, False otherwise
        """
        # For Conversation objects, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # For Message objects, check if user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
            
        # If we're in a viewset with a conversation_pk parameter (nested routes)
        if hasattr(view, 'kwargs') and 'conversation_pk' in view.kwargs:
            from .models import Conversation
            try:
                conversation = Conversation.objects.get(
                    conversation_id=view.kwargs['conversation_pk']
                )
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        
        # Default to False
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit it.
    Anyone can read.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object or if the request is a read-only operation.
        
        Args:
            request: Request object
            view: View object
            obj: Object to check permissions for
            
        Returns:
            bool: True if the user is the owner or the request is a read-only operation, False otherwise
        """
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        return False


class IsAuthenticatedForAPI(permissions.BasePermission):
    """
    Permission to only allow authenticated users to access the API.
    This can be used globally as a default permission class.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        This is called on every request before checking object permissions.
        
        Args:
            request: Request object
            view: View object
            
        Returns:
            bool: True if the user is authenticated, False otherwise
        """
        # Allow registration endpoint without authentication
        if view.__class__.__name__ == 'RegisterView':
            return True
            
        # Require authentication for all other endpoints
        return request.user and request.user.is_authenticated
