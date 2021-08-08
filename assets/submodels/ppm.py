from django.db import models
from django.contrib.auth.models import User
from assets.submodels.assets import Assets

class PPM(models.Model):
    """
    PPM model
    """
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_interval = models.IntegerField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.asset.asset_name
    
    class Meta:
        verbose_name_plural = "PPMs"