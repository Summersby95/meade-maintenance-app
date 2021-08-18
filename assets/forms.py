from django import forms
from django.forms import widgets
from .models import Assets, PPM
from ancillaries.forms import DateInput


class AssetForm(forms.ModelForm):
    """ Assets Form """
    class Meta:
        model = Assets
        fields = '__all__'
        widgets = {
            'installation_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)


class PPMForm(forms.ModelForm):
    """ PPM Form """
    class Meta:
        model = PPM
        exclude = ['asset', 'created_by']

    def __init__(self, *args, **kwargs):
        super(PPMForm, self).__init__(*args, **kwargs)
        self.fields['time_interval'].label = 'Time Interval (Days)'
