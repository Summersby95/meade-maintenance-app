from django import forms
from .models import Project
from ancillaries.forms import DateInput


class ProjectForm(forms.ModelForm):
    """ Project Form """
    class Meta:
        model = Project
        exclude = [
            'created_by',
            'created_on',
            'status',
        ]
        widgets = {
            'due_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
