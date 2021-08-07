from django.contrib import admin
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'due_date',
        'created_by',
        'created_on',
        'status',
    )


admin.site.register(ProjectStatus)
admin.site.register(Project, ProjectAdmin)
