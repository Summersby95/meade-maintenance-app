from django.db import models
from django.contrib.auth.models import User
from ancillaries.models import Locations


class ProjectStatus(models.Model):
    """
    Project status
    """
    status = models.CharField(max_length=40)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name_plural = "Project Statuses"


