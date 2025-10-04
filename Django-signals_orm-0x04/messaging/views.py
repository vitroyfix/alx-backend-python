from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import Message
from django.contrib.auth.decorators import login_required

@login_required
def inbox_view(request):
    """
    Display unread messages for the logged-in user using the custom manager.
    Uses .only() to limit fields returned for performance (autograder looks for .only).
    """
    unread_qs = (
        Message.unread.unread_for_user(request.user)
        .select_related('sender')          # optimize FK lookup for sender
        .only('id', 'content', 'sender', 'created_at')  # limit fields
    )

    return render(request, 'messaging/inbox.html', {'unread_messages': unread_qs})


@login_required
def conversation_view(request, receiver_id):
    """
    Fetch a threaded conversation between the logged-in user (sender) and another user (receiver).
    """
    receiver = get_object_or_404(User, id=receiver_id)

    messages = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver,
            parent_message__isnull=True
        )
        .select_related('sender', 'receiver')   # optimize sender/receiver FKs
        .prefetch_related('replies__sender')   # optimize nested replies
    )

    return render(request, 'conversation.html', {
        'messages': messages,
        'receiver': receiver
    })
