from django.db import models
from ancillaries.models import *


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

