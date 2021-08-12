from django.db import models
from django.contrib.auth.models import User

class NotificationType(models.Model):
    """
    Notification Types Model
    """

    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = "Notification Types"


class Notification(models.Model):
    """
    Notification Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Notifications"
