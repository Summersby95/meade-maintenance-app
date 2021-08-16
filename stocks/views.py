from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ancillaries.models import Suppliers
from assets.models import Assets
from .models import StockItem, StockReceipts, StockTransfer
from .forms import StockItemForm, StockReceiptsForm, StockTransferForm
from ancillaries.forms import SupplierForm
from ancillaries.decorators import custom_user_test, manager_test, stock_test
from jobs.models import Job
from jobs.views import job_details

app_context = {
    'nbar': 'stocks',
    'links': [
        {
            'href': 'inventory_view',
            'text': 'Inventory View',
        },
        {
            'href': 'create_stock_item',
            'text': 'Create Stock Item',
            'test': 'is_stock'
        },
        {
            'href': 'create_stock_receipt',
            'text': 'Receive Stock',
            'test': 'is_stock'
        },
        {
            'href': 'create_stock_transfer',
            'text': 'Withdraw Stock',
        },
        {
            'href': 'user_unassigned_stock',
            'text': 'My Unassigned Stock',
        },
        {
            'href': 'user_assigned_stock',
            'text': 'My Assigned Stock',
        },
        {
            'href': 'supplier_list',
            'text': 'Supplier List',
            'test': 'is_stock'
        },
        {
            'href': 'create_supplier',
            'text': 'Create Supplier',
            'test': 'is_stock'
        }
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
        'card_tabs': [
            {
                'header': f'Stock Item #{item.id}',
                'template': 'stocks/stock_item_details_card.html'
            },
            {
                'header': 'Stock Receipts',
                'template': 'stocks/stock_receipts_table.html'
            },
            {
                'header': 'Stock Withdrawls',
                'template': 'stocks/stock_withdrawls_table.html'
            },
        ],
        'actions': 'stocks/stock_item_details_actions.html',
    }
    context = {**context, **app_context}

    return render(request, 'includes/details.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def create_stock_item(request):
    """ View to create stock item """
    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Item Successfully Created!')
            return redirect(reverse(stock_item_details,
                            args=[form.instance.id]))
        else:
            messages.error(
                request, 'Error Creating Stock Item! Please Try Again'
            )
    else:
        form = StockItemForm()

    context = {
        'form': form,
        'action': reverse(create_stock_item),
        'header': 'Create Stock Item',
        'submit_text': 'Create Item',
        'cancel': reverse(inventory_view),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def edit_stock_item(request, stock_id):
    """ View to edit stock item """
    item = get_object_or_404(StockItem, pk=stock_id)
    if request.method == 'POST':
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item Updated Successfully!')
            return redirect(reverse(stock_item_details, args=[item.id]))
        else:
            messages.error(request, 'Error Updating Item! Please Try Again')
    else:
        form = StockItemForm(instance=item)

    context = {
        'form': form,
        'action': reverse(edit_stock_item, args=[item.id]),
        'header': 'Edit Stock Item',
        'submit_text': 'Update Item',
        'cancel': reverse(stock_item_details, args=[item.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def create_stock_receipt(request):
    """ View to create stock receipt """
    if request.method == 'POST':
        form = StockReceiptsForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.created_by = request.user
            receipt.save()
            messages.success(request, 'Stock Receipt Created Successfully!')
            return redirect(
                reverse(stock_item_details, args=[form.instance.item.id])
            )
        else:
            messages.error(
                request, 'Error Creating Stock Receipt! Please Try Again'
            )
    else:
        form = StockReceiptsForm()

    context = {
        'form': form,
        'action': reverse(create_stock_receipt),
        'header': 'Receive Stock',
        'submit_text': 'Receive Stock',
        'cancel': reverse(inventory_view),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def create_item_stock_receipt(request, stock_id):
    """ View to create stock receipt for a stock item. """
    item = get_object_or_404(StockItem, pk=stock_id)
    form = StockReceiptsForm(initial={'item': item})

    context = {
        'form': form,
        'action': reverse(create_stock_receipt),
        'header': 'Receive Stock',
        'submit_text': 'Receive Stock',
        'cancel': reverse(stock_item_details, args=[item.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def edit_stock_receipt(request, receipt_id):
    """ View to edit stock receipt """
    receipt = get_object_or_404(StockReceipts, pk=receipt_id)
    if request.method == 'POST':
        form = StockReceiptsForm(request.POST, instance=receipt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Receipt Updated Successfully!')
            return redirect(reverse(
                stock_item_details, args=[form.instance.item.id]
            ))
        else:
            messages.error(
                request, 'Error Updating Stock Receipt! Please Try Again!'
            )
    else:
        form = StockReceiptsForm(instance=receipt)

    context = {
        'form': form,
        'action': reverse(edit_stock_receipt, args=[receipt.id]),
        'header': 'Edit Stock Receipt',
        'submit_text': 'Update Stock Receipt',
        'cancel': reverse(stock_item_details, args=[receipt.item.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
def create_stock_transfer(request):
    """ View to create stock transfer """
    if request.method == 'POST':
        form = StockTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            messages.success(request, 'Stock Withdrawl Successful!')
            return redirect(reverse(
                stock_item_details, args=[form.instance.item.id]
            ))
        else:
            messages.error(request, 'Stock Withdrawl Failed! Please Try Again')
    else:
        form = StockTransferForm()

    context = {
        'form': form,
        'action': reverse(create_stock_transfer),
        'header': 'Withdraw Stock',
        'submit_text': 'Withdraw Stock',
        'cancel': reverse(inventory_view),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
def create_item_stock_transfer(request, stock_id):
    """ View to create stock transfer for a stock item. """
    item = get_object_or_404(StockItem, pk=stock_id)
    form = StockTransferForm(initial={'item': item})

    context = {
        'form': form,
        'action': reverse(create_stock_transfer),
        'header': 'Withdraw Stock',
        'submit_text': 'Withdraw Stock',
        'cancel': reverse(stock_item_details, args=[item.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
def edit_stock_transfer(request, transfer_id):
    """ View to edit stock transfer """
    transfer = get_object_or_404(StockTransfer, pk=transfer_id)
    if request.method == 'POST':
        form = StockTransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Transfer Updated Successfully!')
            return redirect(
                reverse(stock_item_details, args=[form.instance.item.id])
            )
        else:
            messages.error(
                request, 'Error Updating Stock Transfer! Please Try Again'
            )
    else:
        form = StockTransferForm(instance=transfer)

    context = {
        'form': form,
        'action': reverse(edit_stock_transfer, args=[transfer.id]),
        'header': 'Edit Stock Transfer',
        'submit_text': 'Update Stock Transfer',
        'cancel': reverse(stock_item_details, args=[transfer.item.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


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


@login_required
def user_assigned_stock(request):
    """ View to list assigned stock items. """
    transfers = StockTransfer.objects.filter(
        user=request.user,
        job__isnull=False,
    )
    context = {
        'transfers': transfers,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/stock_transfer_table.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def supplier_list(request):
    """ View to list suppliers. """
    suppliers = Suppliers.objects.all()
    for supplier in suppliers:
        supplier.stock_receipts = StockReceipts.objects.filter(
            supplier=supplier,
        ).count()
        supplier.assets = Assets.objects.filter(
            supplier=supplier,
        ).count()

    context = {
        'suppliers': suppliers,
    }
    context = {**context, **app_context}

    return render(request, 'stocks/supplier_table.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def supplier_details(request, supplier_id):
    """ View to show supplier details. """
    supplier = get_object_or_404(Suppliers, pk=supplier_id)
    stock_receipts = StockReceipts.objects.filter(
        supplier=supplier,
    )
    assets = Assets.objects.filter(
        supplier=supplier,
    )

    context = {
        'supplier': supplier,
        'stock_receipts': stock_receipts,
        'assets': assets,
        'card_tabs': [
            {
                'header': f'Supplier #{supplier.id}',
                'template': 'stocks/supplier_details_card.html'
            },
            {
                'header': 'Stock Receipts',
                'template': 'stocks/stock_receipts_table.html'
            },
            {
                'header': 'Assets',
                'template': 'stocks/supplier_assets_table.html'
            },
        ],
        'actions': 'stocks/supplier_details_actions.html',
    }
    context = {**context, **app_context}

    return render(request, 'includes/details.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def create_supplier(request):
    """ View to create supplier. """
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Supplier Created Successfully!')
            return redirect(reverse(supplier_details, args=[supplier.id]))
        else:
            messages.error(
                request, 'Error Creating Supplier! Please Try Again'
            )
    else:
        form = SupplierForm()

    context = {
        'form': form,
        'action': reverse(create_supplier),
        'header': 'Create Supplier',
        'submit_text': 'Create Supplier',
        'cancel': reverse(supplier_list),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def create_supplier_stock_receipt(request, supplier_id):
    """ View to create stock receipt for a stock item. """
    supplier = get_object_or_404(Suppliers, pk=supplier_id)
    form = StockReceiptsForm(initial={'supplier': supplier})

    context = {
        'form': form,
        'action': reverse(create_stock_receipt),
        'header': 'Receive Stock',
        'submit_text': 'Receive Stock',
        'cancel': reverse(supplier_details, args=[supplier.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(stock_test, login_url='/stocks/',
                  redirect_field_name=None)
def edit_supplier(request, supplier_id):
    """ View to edit stock transfer """
    supplier = get_object_or_404(Suppliers, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier Successfully Updated!')
            return redirect(reverse(supplier_details, args=[supplier.id]))
        else:
            messages.error(
                request, 'Error Updating Supplier! Please Try Again'
            )
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'form': form,
        'action': reverse(edit_supplier, args=[supplier.id]),
        'header': 'Edit Supplier',
        'submit_text': 'Update Supplier',
        'cancel': reverse(supplier_details, args=[supplier.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)
