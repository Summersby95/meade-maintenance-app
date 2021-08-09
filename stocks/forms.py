from django import forms
from .models import StockItem, StockReceipts, StockTransfer
from ancillaries.forms import DateInput

class StockItemForm(forms.ModelForm):

    class Meta:
        model = StockItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(StockItemForm, self).__init__(*args, **kwargs)


