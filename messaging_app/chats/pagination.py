# messaging_app/chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # optional: allow clients to change up to server limit
    max_page_size = 100
