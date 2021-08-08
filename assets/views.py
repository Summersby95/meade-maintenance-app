from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Assets, AssetTypes, PPM
from jobs.models import Job

app_context = {
    'nbar': 'assets',
    'links': [
        {
            'href': 'active_assets',
            'text': 'Active Assets',
        },
        {
        {
            'href': 'inactive_assets',
            'text': 'Inactive Assets',
        },
    ]
}


@login_required
def active_assets(request):
    """ View to see active assets """
    assets = Assets.objects.filter(active=True)

    context = {
        'assets': assets,
    }
    context = {**app_context, **context}

    return render(request, 'assets/assets_table.html', context)


@login_required
def inactive_assets(request):
    """ View to see inactive assets """
    assets = Assets.objects.filter(active=False)

    context = {
        'assets': assets,
    }
    context = {**app_context, **context}

    return render(request, 'assets/assets_table.html', context)


@login_required
def asset_details(request, asset_id):
    """ View to see details of a specific asset """
    asset = get_object_or_404(Assets, pk=asset_id)
    ppms = PPM.objects.filter(asset=asset)
    jobs = Job.objects.filter(asset=asset)
    
    context = {
        'asset': asset,
        'ppms': ppms,
        'jobs': jobs,
    }
    context = {**app_context, **context}

    return render(request, 'assets/asset_details.html', context)

