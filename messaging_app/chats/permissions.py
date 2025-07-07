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


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission to only allow participants of a conversation to access it.
    """
    
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
