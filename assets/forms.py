from django import forms
from django.forms import widgets
from .models import Assets, PPM
from ancillaries.forms import DateInput


class AssetForm(forms.ModelForm):

    class Meta:
        model = Assets
        fields = '__all__'
        widgets = {
            'installation_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)


