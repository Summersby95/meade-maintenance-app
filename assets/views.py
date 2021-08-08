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

    total_time = datetime.timedelta()
    users = []
    for job in jobs:
        job_times = JobTimes.objects.filter(job=job)
        for job_time in job_times:
            total_time += job_time.time_end - job_time.time_start
            if job_time.user.username not in users:
                users.append(job_time.user.username)
    
    completed = sum(job.status.status == 'Completed' for job in jobs)
    distinct_users = len(users)
    
    context = {
        'asset': asset,
        'ppms': ppms,
        'jobs': jobs,
        'total_time': total_time,
        'completed': completed,
        'distinct_users': distinct_users,
    }
    context = {**app_context, **context}

    return render(request, 'assets/asset_details.html', context)

