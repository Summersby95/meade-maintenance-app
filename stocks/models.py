from django.db import models
from django.contrib.auth.models import User

from ancillaries.models import Locations, Suppliers
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
    mastercode = models.ForeignKey(StockMastercode, on_delete=models.SET_NULL,
                                   null=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL,
                                 null=True)
    barcode = models.CharField(max_length=20, null=True)
    stock_alert = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_current_stock(self):
        return (
            (StockReceipts.objects.filter(item=self).aggregate(
                models.Sum('quantity')
            )['quantity__sum'] or 0)
            -
            (StockTransfer.objects.filter(item=self).aggregate(
                models.Sum('quantity')
            )['quantity__sum'] or 0)
        )

    class Meta:
        verbose_name = 'Stock Item'
        verbose_name_plural = 'Stock Items'


class StockReceipts(models.Model):
    """ Stock Transaction Model """
    item = models.ForeignKey(StockItem, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.SET_NULL,
                                 null=True)
    quantity = models.IntegerField(null=True)
    date_received = models.DateField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'Stock Receipt'
        verbose_name_plural = 'Stock Receipts'


class StockTransfer(models.Model):
    """ Stock Withdrawl Model """
    item = models.ForeignKey(StockItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True,
                            blank=True)

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'Stock Transfer'
        verbose_name_plural = 'Stock Transfers'
