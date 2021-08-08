from django.contrib import admin
from .models import *


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'department',)


admin.site.register(Departments, DepartmentAdmin)
admin.site.register(Locations, LocationAdmin)
admin.site.register(Suppliers)
