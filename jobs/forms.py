from django import forms
from django.forms.widgets import SplitDateTimeWidget
from .models import Job, JobStatus, JobPriority, JobTimes, JobTypes, JobSteps
from ancillaries.models import Departments
from datetime import datetime, timedelta

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'job_title',
            'department',
            'type',
            'priority',
            'description',
        ]
    
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JobStepsForm(forms.ModelForm):

    class Meta:
        model = JobSteps
        fields = ['job', 'step_number', 'step']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JobTimesForm(forms.ModelForm):
    
    class Meta:
        model = JobTimes
        exclude = ['job']
    
    time_start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(),
        initial=datetime.now()
    )
    time_end = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(),
        initial=datetime.now() + timedelta(hours=1)
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

