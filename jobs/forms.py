from django import forms
from .models import Job, JobStatus, JobPriority, JobTypes, JobSteps
from ancillaries.models import Departments

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
    


