from django.shortcuts import get_object_or_404, render, redirect, reverse
from .models import StockItem, StockReceipts, StockTransfer
from django.contrib.auth.decorators import login_required
from .forms import StockItemForm, StockReceiptsForm, StockTransferForm

app_context = {
    'nbar' : 'stocks',
    'links': [
        {
            'href': 'inventory_view',
            'text': 'Inventory View',
        },
    ]
}


@login_required
def inventory_view(request):
    items = StockItem.objects.all()

    context = {
        'items': items,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/inventory_table.html', context)

