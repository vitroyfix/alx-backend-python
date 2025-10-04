from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import Message
from django.contrib.auth.decorators import login_required

@login_required
def conversation_view(request, receiver_id):
    """
    Fetch a threaded conversation between the logged-in user and a receiver.
    """
    receiver = get_object_or_404(User, id=receiver_id)

    # Root messages between sender and receiver
    messages = (
        Message.objects.filter(
            parent_message__isnull=True,
            user=request.user,
        )
        .select_related('user')  # optimize FK user
        .prefetch_related('replies__user')  # optimize nested replies
    )

    return render(request, 'conversation.html', {
        'messages': messages,
        'receiver': receiver
    })
