from django.db import models
from ancillaries.models import Departments, Locations, Suppliers
from assets.models import Assets
from jobs.models import Job

class PPM(models.Model):
    """
    PPM model
    """
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    time_interval = models.IntegerField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.asset.asset_name
    
    class Meta:
        verbose_name_plural = "PPMs"