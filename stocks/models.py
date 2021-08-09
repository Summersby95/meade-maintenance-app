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


class StockItem(models.Model):
    """ Stock Item Model """
    name = models.CharField(max_length=100)
    mastercode = models.ForeignKey(StockMastercode, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    barcode = models.CharField(max_length=20, null=True)
    stock_alert = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    def get_current_stock(self):
        return (
            (StockReceipts.objects.filter(item=self).aggregate(models.Sum('quantity'))['quantity__sum'] or 0)
            -
            (StockTransfer.objects.filter(item=self).aggregate(models.Sum('quantity'))['quantity__sum'] or 0)
        )
    
    class Meta:
        verbose_name = 'Stock Item'
        verbose_name_plural = 'Stock Items'

