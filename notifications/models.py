import datetime
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
from stocks.models import StockItem


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
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    stock_item = models.ForeignKey(StockItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def time_since(self):
        """
        Time since notification was created
        """
        time_since = datetime.datetime.now().astimezone() - self.created_at
        hours = time_since.seconds // 3600
        minutes = (time_since.seconds // 60) % 60
        seconds = time_since.seconds % 60
        if hours > 0:
            time_since = str(hours) + " hours ago"
        elif minutes > 0:
            time_since = str(minutes) + " minutes ago"
        else:
            time_since = str(seconds) + " seconds ago"
        
        return time_since

    class Meta:
        verbose_name_plural = "Notifications"
