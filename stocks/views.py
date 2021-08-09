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


@login_required
def stock_item_details(request, stock_id):
    item = get_object_or_404(StockItem, pk=stock_id)
    stock_receipts = StockReceipts.objects.filter(item=item)
    stock_transfers = StockTransfer.objects.filter(item=item)

    context = {
        'item': item,
        'stock_receipts': stock_receipts,
        'stock_transfers': stock_transfers,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/stock_item_details.html', context)

