from django.db import models
from ancillaries.models import Locations, Suppliers
from django.contrib.auth.models import User
from jobs.models import Job


class StockType(models.Model):
    """ Stock Type Model """
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = 'Stock Type'
        verbose_name_plural = 'Stock Types'


class StockMastercode(models.Model):
    """ Stock Mastercode Model """
    code = models.CharField(max_length=20)
    type = models.ForeignKey(StockType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Stock Mastercode'
        verbose_name_plural = 'Stock Mastercodes'


