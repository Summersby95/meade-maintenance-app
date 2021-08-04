from django.shortcuts import get_object_or_404
from .models import UserProfile


def user_profile(request):
    """
    Returns a user's profile.
    """
    if request.user.is_authenticated:
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        return {'profile': profile}
    else:
        return {}
