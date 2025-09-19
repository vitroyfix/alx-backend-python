#!/usr/bin/env python3
"""
Serializers for messaging app models.
Defines UserSerializer, ConversationSerializer, and MessageSerializer.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name',
                  'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation',
                  'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
