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

