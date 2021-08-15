from django.contrib import admin
from .models import *


class JobAdmin(admin.ModelAdmin):
    list_display = (
        'job_title',
        'department',
        'status',
        'created_on',
    )


class JobStepsAdmin(admin.ModelAdmin):
    list_display = (
        'job',
        'step_number',
        'step',
        'completed',
    )


class JobTimesAdmin(admin.ModelAdmin):
    list_display = (
        'job',
        'time_start',
        'time_end',
    )


admin.site.register(Job, JobAdmin)
admin.site.register(JobTypes)
admin.site.register(JobStatus)
admin.site.register(JobPriority)
admin.site.register(JobSteps, JobStepsAdmin)
admin.site.register(JobTimes, JobTimesAdmin)
