from django.shortcuts import render


app_context = {
    'nbar': 'dashboard',
    'links': [
        {
            'href': 'outstanding_jobs',
            'text': 'Dashboard',
        },
        {
            'href': 'create_job',
            'text': 'Reports',
        },
    ],
}


def dashboard(request):
    """Returns dashboard home"""
    return render(request, 'dashboard/dashboard.html')