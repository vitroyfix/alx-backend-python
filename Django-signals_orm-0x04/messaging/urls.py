from django.urls import path
from . import views

urlpatterns = [
    path('delete_account/', views.delete_user, name='delete_user'),
    path('conversation/<int:message_id>/', views.conversation_view, name='conversation'),
    path('messages/', views.list_messages, name='list_messages'),
]