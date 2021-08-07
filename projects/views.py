import datetime
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectStatus
from jobs.models import Job, JobTimes
from profiles.models import UserProfile
from .forms import ProjectForm

app_context = {
    'nbar': 'projects',
    'links': [
        {
            'href': 'ongoing_projects',
            'text': 'Ongoing Projects',
        },
        {
            'href': 'create_project',
            'text': 'Create New Project',
        }
    ]
}


@login_required
def ongoing_projects(request):
    """ View to see ongoing projects. """
    projects = Project.objects.filter(status=ProjectStatus.objects.get(status='Pending')).order_by('-due_date')

    context = {
        'projects': projects,
    }
    context = {**app_context, **context}

    return render(request, 'projects/projects_table.html', context)


@login_required
def project_details(request, project_id):
    """ View to see project details. """
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    context = {**app_context, **context}
    return render(request, 'projects/project_details.html', context)
