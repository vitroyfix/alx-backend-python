# messaging_app/chats/permissions.py
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission that allows only participants in a Conversation to view/create/update/delete messages
    Assumptions about models:
     - There is a Conversation model with a ManyToMany field 'participants' to User, or similar
     - Message instances have a ForeignKey to Conversation named 'conversation'
    If your field names differ, adjust accordingly.
    """

    def has_permission(self, request, view):
        # Require authentication first
        if not request.user or not request.user.is_authenticated:
            return False

        # For list/create actions on messages we may have conversation id in query or request.data
        # If view provides `get_conversation()` or the lookup kwarg 'conversation_pk' we can check.
        return True

    def has_object_permission(self, request, view, obj):
        """
        obj might be a Conversation or a Message instance.
        If Message: check message.conversation.participants includes user (or message.sender/conversation participants).
        If Conversation: check conversation.participants includes user.
        """
        user = request.user

        # If object looks like a Message
        # adjust attribute names to match your models (e.g., obj.conversation or obj.chat)
        conversation = None
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        elif obj.__class__.__name__.lower().startswith('conversation'):
            conversation = obj
        else:
            # Try to see if view has conversation lookup in kwargs
            # fallback: deny
            return False

        # Now check participant membership
        try:
            # assuming conversation.participants is a ManyToMany to User
            return conversation.participants.filter(pk=user.pk).exists()
        except Exception:
            # If participants is a list/iterable
            try:
                return user in list(conversation.participants.all())
            except Exception:
                return False
