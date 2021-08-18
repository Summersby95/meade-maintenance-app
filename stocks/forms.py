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

    def __init__(self, *args, **kwargs):
        super(StockTransferForm, self).__init__(*args, **kwargs)
