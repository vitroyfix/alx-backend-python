from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message

# Task 2: Delete user view
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete() # Signals will handle the cleanup
        return redirect('home')
    return render(request, 'delete_account.html')

# Task 3: Threaded conversation view with optimization
@login_required
def conversation_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Optimized query
    replies = message.replies.all().select_related('sender', 'receiver')
    return render(request, 'conversation.html', {'message': message, 'replies': replies})

# Task 5: Caching the message list for 60 seconds
@cache_page(60)
@login_required
def list_messages(request):
    messages = Message.objects.all()
    return render(request, 'message_list.html', {'messages': messages})