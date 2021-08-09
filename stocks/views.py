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
        {
            'href': 'create_stock_receipt',
            'text': 'Receive Stock',
        },
        {
            'href': 'create_stock_transfer',
            'text': 'Withdraw Stock',
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


@login_required
def edit_stock_item(request, stock_id):
    """ View to edit stock item """
    item = get_object_or_404(StockItem, pk=stock_id)
    if request.method == 'POST':
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse(stock_item_details, args=[item.id]))
    else:
        form = StockItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/edit_stock_item.html', context)


@login_required
def create_stock_receipt(request):
    """ View to create stock receipt """
    if request.method == 'POST':
        form = StockReceiptsForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.created_by = request.user
            receipt.save()
            return redirect(reverse(stock_item_details, args=[form.instance.item.id]))
    else:
        form = StockReceiptsForm()

    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/create_stock_receipt.html', context)


@login_required
def create_item_stock_receipt(request, stock_id):
    """ View to create stock receipt for a stock item. """
    item = get_object_or_404(StockItem, pk=stock_id)
    if request.method == 'POST':
        form = StockReceiptsForm(request.POST, initial={'item': item})
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.created_by = request.user
            receipt.save()
            return redirect(reverse(stock_item_details, args=[item.id]))
    else:
        form = StockReceiptsForm(initial={'item': item})

    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/create_stock_receipt.html', context)


@login_required
def edit_stock_receipt(request, receipt_id):
    """ View to edit stock receipt """
    receipt = get_object_or_404(StockReceipts, pk=receipt_id)
    if request.method == 'POST':
        form = StockReceiptsForm(request.POST, instance=receipt)
        if form.is_valid():
            form.save()
            return redirect(reverse(stock_item_details, args=[form.instance.item.id]))
    else:
        form = StockReceiptsForm(instance=receipt)

    context = {
        'form': form,
        'receipt': receipt,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/edit_stock_receipt.html', context)


@login_required
def create_stock_transfer(request):
    """ View to create stock transfer """
    if request.method == 'POST':
        form = StockTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            return redirect(reverse(stock_item_details, args=[form.instance.item.id]))
    else:
        form = StockTransferForm()

    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/create_stock_transfer.html', context)


@login_required
def create_item_stock_transfer(request, stock_id):
    """ View to create stock transfer for a stock item. """
    item = get_object_or_404(StockItem, pk=stock_id)
    if request.method == 'POST':
        form = StockTransferForm(request.POST, initial={'item': item})
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            return redirect(reverse(stock_item_details, args=[item.id]))
    else:
        form = StockTransferForm(initial={'item': item})

    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/create_stock_transfer.html', context)


@login_required
def edit_stock_transfer(request, transfer_id):
    """ View to edit stock transfer """
    transfer = get_object_or_404(StockTransfer, pk=transfer_id)
    if request.method == 'POST':
        form = StockTransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect(reverse(stock_item_details, args=[form.instance.item.id]))
    else:
        form = StockTransferForm(instance=transfer)

    context = {
        'form': form,
        'transfer': transfer,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/edit_stock_transfer.html', context)


@login_required
def user_unassigned_stock(request):
    """ View to list unassigned stock items. """
    transfers = StockTransfer.objects.filter(
        user=request.user,
        job=None,
    )
    context = {
        'transfers': transfers,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/stock_transfer_table.html', context)

