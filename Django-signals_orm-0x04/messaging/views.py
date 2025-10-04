from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def inbox_view(request):
    """
    Display unread messages for the logged-in user using the custom manager.
    Uses .only() to limit fields returned for performance.
    """
    unread_qs = (
        Message.unread.unread_for_user(request.user)
        .select_related('sender')  # optimize FK lookup for sender
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
        .select_related('sender', 'receiver')  # optimize sender/receiver FKs
        .prefetch_related('replies__sender')  # optimize nested replies
    )

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'receiver': receiver
    })


@login_required
@cache_page(60)  # Cache this view for 60 seconds
def cached_conversation_view(request, receiver_id):
    """
    Cached version of conversation messages between sender and receiver.
    """
    receiver = get_object_or_404(User, id=receiver_id)

    messages = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver,
            parent_message__isnull=True
        )
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender')
    )

    return render(request, 'messaging/conversation_cached.html', {
        'messages': messages,
        'receiver': receiver
    })
