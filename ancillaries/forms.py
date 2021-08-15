from django import forms
from .models import Suppliers


class DateInput(forms.DateInput):
    input_type = 'date'


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Suppliers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
