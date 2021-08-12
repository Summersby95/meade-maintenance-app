from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

app_context = {
    'links': [
        {
            'href': 'notification_table',
            'text': 'Unread Notifications',
        },
    ],
}

@login_required
def notification_table(request):
    notificaiton_list = Notification.objects.filter(user=request.user, read=False)

    context = {
        'notification_list': notificaiton_list,
    }
    return render(request, 'notifications/notification_table.html', context)
