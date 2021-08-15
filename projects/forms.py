from django import forms
from .models import Project
from ancillaries.forms import DateInput


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = [
            'created_on',
            'status',
        ]
        widgets = {
            'due_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['created_by'].initial = self.profile.user.id
        self.fields['created_by'].widget.attrs['hidden'] = True
        self.fields['created_by'].label = ""
        self.fields['created_by'].widget.attrs['readonly'] = True
