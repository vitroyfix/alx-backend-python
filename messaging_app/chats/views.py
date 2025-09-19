#!/usr/bin/env python3
"""
Views for messaging app.
Implements ConversationViewSet and MessageViewSet.
"""

from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
