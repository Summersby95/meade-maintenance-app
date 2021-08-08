from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Assets, AssetTypes, PPM

app_context = {
    'nbar': 'assets',
    'links': [
        {
            'href': 'active_assets',
            'text': 'Active Assets',
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