# messaging_app/urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from chats import views as chat_views

router = routers.DefaultRouter()
router.register(r'conversations', chat_views.ConversationViewSet, basename='conversation')
router.register(r'messages', chat_views.MessageViewSet, basename='message')

urlpatterns = [
    path('api/', include(router.urls)),
    # JWT auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # optionally include browsable API auth:
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
