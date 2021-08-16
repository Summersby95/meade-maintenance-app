from functools import wraps
from urllib.parse import urlparse

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url, get_object_or_404

from profiles.models import UserProfile


def custom_user_test(test_func, login_url=None,
                     redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Custom user_passes_test decorator that passes the request to
    the test_func instead of request.user.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access'
                               ' this page.')
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def manager_test(request):
    """
    checks if the user is a manager or admin
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    res = False

    if str(profile.user_type).lower() in (
        'admin', 'manager'
    ):
        res = True

    return res


