from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

app_context = {
    'links': [
        {
            'href': 'notification_table',
            'text': 'Unread Notifications',
        },
        {
            'href': 'read_notifications',
            'text': 'Read Notifications',
        }
    ],
}


@login_required
def notification_table(request):
    """ Notification Table View """
    notificaiton_list = Notification.objects.filter(
        user=request.user, read=False
    ).order_by("-created_at")

    for notification in notificaiton_list:
        notification.read = True
        notification.save()

    context = {
        'notification_list': notificaiton_list,
        'card_tabs': [
            {
                'header': 'Unread Notifications',
                'template': 'notifications/notification_table.html'
            },
        ],
    }
    context = {**context, **app_context}

    return render(request, 'includes/details.html', context)


@login_required
def read_notifications(request):
    """ Read Notifications View """
    notificaiton_list = Notification.objects.filter(
        user=request.user, read=True
    ).order_by("-created_at")[:20]

    context = {
        'notification_list': notificaiton_list,
        'card_tabs': [
            {
                'header': 'Recent Notifications',
                'template': 'notifications/notification_table.html'
            },
        ],
    }
    context = {**context, **app_context}

    return render(request, 'includes/details.html', context)
