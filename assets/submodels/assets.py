from django.db import models
from ancillaries.models import Departments, Locations, Suppliers


class AssetTypes(models.Model):
    """ Asset Types Model """
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'Asset Types'


class Assets(models.Model):
    """
    Assets model
    """
    asset_name = models.CharField(max_length=40)
    asset_type = models.ForeignKey(AssetTypes, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    installation_date = models.DateField()
    description = models.TextField()
    barcode = models.CharField(max_length=20)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.asset_name

    class Meta:
        verbose_name_plural = "Assets"
