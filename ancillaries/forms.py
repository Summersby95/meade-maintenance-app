from django import forms
from .models import Suppliers


class DateInput(forms.DateInput):
    """ custom date widget """
    input_type = 'date'


class SupplierForm(forms.ModelForm):
    """ Supplier Form """
    class Meta:
        model = Suppliers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
