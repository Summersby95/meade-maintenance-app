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
        {
            'href': 'create_stock_item',
            'text': 'Create Stock Item',
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


@login_required
def create_stock_item(request):
    """ View to create stock item """
    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(stock_item_details, args=[form.instance.id]))
    else:
        form = StockItemForm()

    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/create_stock_item.html', context)


