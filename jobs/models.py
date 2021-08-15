from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User

from ancillaries.models import *
from projects.models import Project
from assets.submodels.assets import Assets
from assets.submodels.ppm import PPM


class JobStatus(models.Model):
    """ Job Status Model """
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Job Status'


class JobPriority(models.Model):
    """ Job Priority Model """
    priority = models.CharField(max_length=20)

    def __str__(self):
        return self.priority

    class Meta:
        verbose_name_plural = 'Job Priorities'


class JobTypes(models.Model):
    """ Job Type Model """
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'Job Types'


class Job(models.Model):
    """ Job Model """
    job_title = models.CharField(max_length=255)
    department = models.ForeignKey(Departments, null=True,
                                   on_delete=models.SET_NULL)
    type = models.ForeignKey(JobTypes, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(JobStatus, null=True,
                               on_delete=models.SET_NULL, default=1)
    due_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True,
                                on_delete=models.SET_NULL)
    asset = models.ForeignKey(Assets, null=True, blank=True,
                              on_delete=models.SET_NULL)
    ppm = models.ForeignKey(PPM, null=True, blank=True,
                            on_delete=models.SET_NULL)
    priority = models.ForeignKey(JobPriority, null=True,
                                 on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ManyToManyField(User, related_name='assigned_to',
                                         blank=True)

    def __str__(self):
        if self.ppm is not None:
            return 'PPM: ' + self.job_title
        else:
            return self.job_title


class JobSteps(models.Model):
    """ Job Steps Model """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    step = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.step

    class Meta:
        verbose_name_plural = 'Job Steps'


class JobTimes(models.Model):
    """ Job Times Model """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    time_start = models.DateTimeField(null=True)
    time_end = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.job_title

    def time_diff(self):
        return self.time_end - self.time_start

    class Meta:
        verbose_name_plural = 'Job Times'
