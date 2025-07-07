"""
Custom pagination classes for the chats application.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    
    Attributes:
        page_size: Number of messages per page
        page_size_query_param: Query parameter to override page size
        max_page_size: Maximum allowable page size
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with additional metadata.
        
        Args:
            data: Serialized data
            
        Returns:
            Response: Response with pagination metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
    
    
class ConversationPagination(PageNumberPagination):
    """
    Custom pagination class for conversations.
    
    Attributes:
        page_size: Number of conversations per page
        page_size_query_param: Query parameter to override page size
        max_page_size: Maximum allowable page size
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with additional metadata.
        
        Args:
            data: Serialized data
            
        Returns:
            Response: Response with pagination metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
