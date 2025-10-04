from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal handler: every time a new Message is saved,
    create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
