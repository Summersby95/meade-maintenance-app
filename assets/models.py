from django.db import models
from ancillaries.models import Departments, Locations, Suppliers
from jobs.models import Job


class AssetTypes(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = 'Asset Types'


