"""
Custom pagination classes for the chats application.
"""
from rest_framework.pagination import PageNumberPagination


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
