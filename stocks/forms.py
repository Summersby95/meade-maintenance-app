from django import forms

from .models import StockItem, StockReceipts, StockTransfer
from ancillaries.forms import DateInput


class StockItemForm(forms.ModelForm):
    """ Stock Item Form """
    class Meta:
        model = StockItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StockItemForm, self).__init__(*args, **kwargs)


class StockReceiptsForm(forms.ModelForm):
    """ Stock Receipts Form """
    class Meta:
        model = StockReceipts
        exclude = ('created_by', 'created_on',)
        widgets = {
            'date_received': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(StockReceiptsForm, self).__init__(*args, **kwargs)


class StockTransferForm(forms.ModelForm):
    """ Stock Transfer Form """
    class Meta:
        model = StockTransfer
        exclude = ('user', 'created_on',)

    """ Checks that stock item has sufficient stock to transfer """
    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        stock_item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        if stock_item.get_current_stock() < quantity:
            raise forms.ValidationError('No Stock')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(StockTransferForm, self).__init__(*args, **kwargs)
