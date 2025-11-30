from django.db import models
from django.contrib.auth.models import User

# Task 4: Custom Manager to filter unread messages efficiently
class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Task 4: Field to track read status
    read = models.BooleanField(default=False)
    
    # Task 1: Fields to track edits
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    # Task 3: Self-referential FK for threaded replies
    parent_message = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies'
    )

    objects = models.Manager() # Default manager
    unread = UnreadMessagesManager() # Custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class MessageHistory(models.Model):
    # Task 1: Model to store old versions of edited messages
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    # Task 0: Model to store notifications
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)