import datetime

from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from stocks.models import StockTransfer
from .models import Assets, PPM
from .forms import AssetForm, PPMForm
from jobs.models import Job, JobStatus, JobTimes

app_context = {
    'nbar': 'assets',
    'links': [
        {
            'href': 'active_assets',
            'text': 'Active Assets',
        },
        {
            'href': 'create_asset',
            'text': 'Create New Asset',
            'test': 'is_manager'
        },
        {
            'href': 'inactive_assets',
            'text': 'Inactive Assets',
            'test': 'is_manager'
        },
    ]
}


@login_required
def active_assets(request):
    """ View to see active assets """
    assets = Assets.objects.filter(active=True)

    context = {
        'assets': assets,
        'table_title': 'Active Assets',
    }
    context = {**app_context, **context}

    return render(request, 'assets/assets_table.html', context)


@login_required
def inactive_assets(request):
    """ View to see inactive assets """
    assets = Assets.objects.filter(active=False)

    context = {
        'assets': assets,
        'table_title': 'Inactive Assets',
    }
    context = {**app_context, **context}

    return render(request, 'assets/assets_table.html', context)


@login_required
def asset_details(request, asset_id):
    """ View to see details of a specific asset """
    asset = get_object_or_404(Assets, pk=asset_id)
    ppms = PPM.objects.filter(asset=asset)
    jobs = Job.objects.filter(asset=asset)

    total_time = sum(
        [time.time_diff() for time in JobTimes.objects.filter(
            job__asset=asset,
            time_end__isnull=False
        )],
        datetime.timedelta()
    )

    completed = Job.objects.filter(
        Q(status=JobStatus.objects.get(status='Completed')) &
        Q(asset=asset)
    ).distinct().count()

    distinct_users = JobTimes.objects.filter(
        job__asset=asset,
        time_end__isnull=False
    ).values('user').distinct().count()

    job_transfers = StockTransfer.objects.filter(
        job__asset=asset
    )

    context = {
        'asset': asset,
        'ppms': ppms,
        'jobs': jobs,
        'total_time': total_time,
        'completed': completed,
        'distinct_users': distinct_users,
        'job_transfers': job_transfers,
    }
    context = {**app_context, **context}

    return render(request, 'assets/asset_details.html', context)


@login_required
def create_asset(request):
    """ View to create a new asset """
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            messages.success(request, 'Asset Created Successfully')
            return redirect(reverse('asset_details', args=(asset.id,)))
        else:
            messages.error(request, 'Error Creating Asset! Please Try Again')
    else:
        form = AssetForm()

    context = {
        'form': form,
        'action': reverse(create_asset),
        'header': 'Create Asset',
        'submit_text': 'Create Asset',
        'cancel': reverse(active_assets),
    }
    context = {**app_context, **context}

    return render(request, 'includes/form.html', context)


@login_required
def edit_asset(request, asset_id):
    """ View to edit an existing asset """
    asset = get_object_or_404(Assets, pk=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            messages.success(request, 'Asset Updated Successfully')
            return redirect(reverse('asset_details', args=(asset.id,)))
        else:
            messages.error(request, 'Error Updating Asset! Please Try Again')
    else:
        form = AssetForm(instance=asset)

    context = {
        'form': form,
        'action': reverse(edit_asset, args=(asset.id,)),
        'header': 'Edit Stock Item',
        'submit_text': 'Update Item',
        'cancel': reverse(asset_details, args=(asset.id,)),
    }
    context = {**app_context, **context}

    return render(request, 'includes/form.html', context)


@login_required
def make_asset_inactive(request, asset_id):
    """ View to make an asset inactive """
    asset = get_object_or_404(Assets, pk=asset_id)
    asset.active = False
    asset.save()
    messages.success(request, 'Asset Made Inactive Successfully')
    return redirect(reverse('asset_details', args=(asset.id,)))


@login_required
def make_asset_active(request, asset_id):
    """ View to make an asset active """
    asset = get_object_or_404(Assets, pk=asset_id)
    asset.active = True
    asset.save()
    messages.success(request, 'Asset Made Active Successfully')
    return redirect(reverse('asset_details', args=(asset.id,)))


@login_required
def add_ppm(request, asset_id):
    """ View to add a new PPM to an existing asset """
    asset = get_object_or_404(Assets, pk=asset_id)
    if request.method == 'POST':
        form = PPMForm(request.POST)
        if form.is_valid():
            ppm = form.save(commit=False)
            ppm.asset = asset
            ppm.created_by = request.user
            ppm.save()

            messages.success(request, 'PPM Created Successfully')
            return redirect(reverse('asset_details', args=(asset.id,)))
        else:
            messages.error(request, 'Error Creating PPM! Please Try Again')
    else:
        form = PPMForm()

    context = {
        'form': form,
        'action': reverse(add_ppm, args=(asset.id,)),
        'header': 'Create Stock Item',
        'submit_text': 'Create Item',
        'cancel': reverse(asset_details, args=(asset.id,)),
    }
    context = {**app_context, **context}

    return render(request, 'includes/form.html', context)


@login_required
def ppm_details(request, ppm_id):
    """ View to see details of a specific PPM """
    ppm = get_object_or_404(PPM, pk=ppm_id)
    jobs = Job.objects.filter(ppm=ppm)

    context = {
        'ppm': ppm,
        'jobs': jobs,
    }
    context = {**app_context, **context}

    return render(request, 'assets/ppm_details.html', context)
