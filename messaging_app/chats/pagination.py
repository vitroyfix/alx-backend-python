# messaging_app/chats/pagination.py
"""
Pagination classes used in chats app.
"""

from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    PageNumber pagination for messages; 20 messages per page.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
