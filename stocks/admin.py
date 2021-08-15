from django.contrib import admin
from .models import *


class StockMastercodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'type',
    )


class StockItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mastercode',
        'location',
        'stock_alert',
    )


class StockReceiptsAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'supplier',
        'quantity',
        'date_received',
        'created_by',
        'created_on',
    )


class StockTransferAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'quantity',
        'user',
        'created_on',
        'job',
    )


admin.site.register(StockType)
admin.site.register(StockMastercode, StockMastercodeAdmin)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(StockReceipts, StockReceiptsAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
