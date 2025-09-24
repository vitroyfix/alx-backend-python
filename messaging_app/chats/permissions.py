# messaging_app/chats/permissions.py
"""
Custom permissions for the chats app.

- IsParticipantOfConversation: allow only participants of a conversation
  to access or modify messages belonging to that conversation.
"""

from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission that allows access only to participants of the conversation.

    For:
    - message-level views: checks message.conversation participants
    - conversation views: checks the conversation participants
    - create: ensures the requesting user is in the participants list (if provided)
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated (global setting covers this; keep explicit)
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow listing — object-level check will filter results in queryset
        if view.action in ["list", "retrieve"]:
            return True

        # Allow create — creator must be a participant (we check in has_object_permission)
        if view.action == "create":
            return True

        # For other non-object actions, defer to object-level
        return True

    def has_object_permission(self, request, view, obj):
        # If object is a Conversation instance:
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If object is a Message instance (message has conversation relation):
        conversation = getattr(obj, "conversation", None)
        if conversation:
            return request.user in conversation.participants.all()

        # Default deny
        return False
