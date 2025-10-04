from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request, user_id):
    """
    Allow a user to delete their own account.
    """
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        messages.error(request, "You cannot delete another user's account.")
        return redirect('home')

    user.delete()
    messages.success(request, "Your account and related data have been deleted.")
    return redirect('home')
