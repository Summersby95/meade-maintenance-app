from datetime import datetime, timedelta

from django import forms

from .models import Job, JobPriority, JobTimes, JobTypes, JobSteps
from ancillaries.forms import DateInput


class JobForm(forms.ModelForm):
    """ Job Form """
    class Meta:
        model = Job
        fields = [
            'job_title',
            'department',
            'type',
            'priority',
            'due_date',
            'description',
            'project',
            'asset',
            'assigned_to',
            'created_by',
        ]
        widgets = {
            'due_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['priority'].initial = JobPriority.objects.get(
            priority='Medium'
        )
        self.fields['department'].initial = self.profile.department
        self.fields['type'].initial = JobTypes.objects.get(
            type='General Maintenance'
        )
        """
        The created by field is hidden because the user is automatically
        assigned to the created_by field.
        """
        self.fields['created_by'].initial = self.profile.user.id
        self.fields['created_by'].widget.attrs['hidden'] = True
        self.fields['created_by'].label = ""
        """
        We dont want non-manager/admin users to be able to
        assign other users to jobs.
        """
        if not str(self.profile.user_type).lower() in ('admin', 'manager'):
            self.fields['assigned_to'].initial = self.profile.user.id
            self.fields['assigned_to'].widget.attrs['hidden'] = True
            self.fields['assigned_to'].label = ""


class JobStepsForm(forms.ModelForm):
    """ Job Steps Form """
    class Meta:
        model = JobSteps
        fields = ['job', 'step_number', 'step']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JobTimesForm(forms.ModelForm):
    """ Job Times Form """
    class Meta:
        model = JobTimes
        exclude = ['job', 'user']

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
