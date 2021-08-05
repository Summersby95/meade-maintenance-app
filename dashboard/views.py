from django.shortcuts import render
from django.contrib.auth.decorators import login_required


app_context = {
    'nbar': 'dashboard',
    'links': [
        {
            'href': 'dashboard',
            'text': 'Dashboard',
        },
        # {
        #     'href': 'create_job',
        #     'text': 'Reports',
        # },
    ],
}


@login_required
def dashboard(request):
    """Returns dashboard home"""
    context = app_context
    return render(request, 'dashboard/dashboard.html', context)