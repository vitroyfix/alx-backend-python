from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        """
        thread = []
        replies = self.replies.all().select_related('user').prefetch_related('replies')
        for reply in replies:
            thread.append(reply)
            thread.extend(reply.get_thread())  # recursion
        return thread

class Notification(models.Model):
    """
    Notification is created when a new message is sent.
    Decoupled from business logic using Django signals.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message {self.message.id}"

class MessageHistory(models.Model):
    """
    Stores old versions of a message when it gets edited.
    """
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"History for Message {self.message.id} edited by {self.edited_by}"
    