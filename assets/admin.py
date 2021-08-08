from django.contrib import admin
from .models import *


class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'asset_name',
        'asset_type',
        'department',
        'location',
        'active',
    ]


class PPMAdmin(admin.ModelAdmin):
    list_display = [
        'asset',
        'job',
        'time_interval',
        'active',
    ]


admin.site.register(Assets, AssetAdmin)
admin.site.register(AssetTypes)
admin.site.register(PPM, PPMAdmin)
