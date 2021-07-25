from django import forms
from .models import Job, JobStatus, JobPriority, JobTypes, JobSteps
from ancillaries.models import Departments

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = '__all__'
    
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

