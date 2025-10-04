from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal handler: every time a new Message is saved,
    create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler: before saving a Message update,
    store the old content in MessageHistory.
    """
    if not instance.pk:
        # New message, nothing to compare
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Save old content before update
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True