from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of a conversation can view, send, update or delete messages.
    Checker requires explicit method checks: GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow permission check to continue to object-level
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Determine the conversation object
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
        else:
            conversation = obj  # obj is a Conversation instance

        # Check if user is a participant
        is_participant = conversation.participants.filter(id=user.id).exists()

        if request.method in ["GET"]:
            return is_participant

        if request.method in ["POST"]:
            return is_participant

        if request.method in ["PUT", "PATCH"]:
            return is_participant

        if request.method in ["DELETE"]:
            return is_participant

        # For any other methods:
        return False
