from django.contrib import admin
from .models import Assets, AssetTypes, PPM


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
        'job_title',
        'time_interval',
        'active',
    ]


admin.site.register(Assets, AssetAdmin)
admin.site.register(AssetTypes)
admin.site.register(PPM, PPMAdmin)
