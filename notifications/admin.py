from django.contrib import admin
from .models import NotificationType, Notification


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = [
        'type',
    ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'type',
        'created_at',
        'read',
        'value',
    ]


admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(Notification, NotificationAdmin)
