from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import Message
from django.contrib.auth.decorators import login_required

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
