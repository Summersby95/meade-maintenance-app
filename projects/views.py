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
    jobs = Job.objects.filter(project=project)

    total_time = datetime.timedelta()
    users = []
    for job in jobs:
        job_times = JobTimes.objects.filter(job=job)
        for job_time in job_times:
            total_time += job_time.time_end - job_time.time_start
            if job_time.user.username not in users:
                users.append(job_time.user.username)
    
    completed = sum(job.status.status == 'Completed' for job in jobs)
    average_time = total_time / len(jobs) if len(jobs) > 0 else 0
    distinct_users = len(users)

    context = {
        'project': project,
        'jobs': jobs,
        'total_time': total_time,
        'completed': completed,
        'average_time': average_time,
        'distinct_users': distinct_users,
    }
    context = {**app_context, **context}
    return render(request, 'projects/project_details.html', context)
