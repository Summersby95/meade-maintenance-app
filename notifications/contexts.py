from .models import Notification


def notification_count(request):
    """
    Returns the number of unread notifications for the user
    """
    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(
            user=request.user, read=False).count()

    return {'notification_count': notification_count}
