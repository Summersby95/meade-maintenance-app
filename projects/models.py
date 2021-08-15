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


class Project(models.Model):
    """
    Project model
    """
    title = models.CharField(max_length=100)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE,
                               default=ProjectStatus.objects.get(
                                   status='Pending'
                               ).id)
    description = models.TextField()
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
