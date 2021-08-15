import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum

from jobs.models import Job, JobStatus, JobTimes
from projects.models import Project, ProjectStatus


app_context = {
    'nbar': 'dashboard',
    'links': [
        {
            'href': 'dashboard',
            'text': 'Dashboard',
        },
    ],
}


@login_required
def dashboard(request):
    """Returns dashboard home"""
    context = app_context
    return render(request, 'dashboard/dashboard.html', context)