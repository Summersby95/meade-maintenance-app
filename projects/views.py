import datetime
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Project, ProjectStatus
from jobs.models import Job, JobTimes
from profiles.models import UserProfile
from .forms import ProjectForm
from ancillaries.decorators import custom_user_test, manager_test

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
            'test': 'is_manager'
        },
        {
            'href': 'completed_projects',
            'text': 'Completed Projects',
        },
        {
            'href': 'cancelled_projects',
            'text': 'Cancelled Projects',
        }
    ]
}


@login_required
def ongoing_projects(request):
    """ View to see ongoing projects. """
    projects = Project.objects.filter(
        status=ProjectStatus.objects.get(status='Pending')
    ).order_by('-due_date')

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

    # FIX
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
        'card_tabs': [
            {
                'header': f'Project #{project.id}',
                'template': 'projects/project_details_card.html'
            },
            {
                'header': 'Project Time Statistics',
                'template': 'projects/project_time_statistics_card.html'
            },
            {
                'header': 'Parts Used',
                'template': 'projects/parts_used_card.html'
            },
            {
                'header': 'Project Jobs',
                'template': 'projects/project_jobs_card.html'
            }
        ],
        'actions': 'projects/project_details_actions.html',
    }
    context = {**app_context, **context}
    return render(request, 'includes/details.html', context)


@login_required
@custom_user_test(manager_test, login_url='/projects/',
                  redirect_field_name=None)
def create_project(request):
    """ View to create job """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project Created!')
            return redirect(reverse(project_details, args=[project.id]))
        else:
            messages.error(request, 'There was an error creating your project')
            print(form.errors)
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'action': reverse(create_project),
        'header': 'Create Stock Item',
        'submit_text': 'Create Item',
        'cancel': reverse(ongoing_projects),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(manager_test, login_url='/projects/',
                  redirect_field_name=None)
def edit_project(request, project_id):
    """ View to edit job """
    project = get_object_or_404(Project, pk=project_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project Updated!')
            return redirect(reverse(project_details, args=[project.id]))
        else:
            messages.error(request, 'There was an error updating your project')
            print(form.errors)
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'action': reverse(edit_project, args=[project.id]),
        'header': 'Edit Project',
        'submit_text': 'Update Project',
        'cancel': reverse(project_details, args=[project.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(manager_test, login_url='/projects/',
                  redirect_field_name=None)
def mark_project_completed(request, project_id):
    """ View to mark job as completed """
    project = get_object_or_404(Project, pk=project_id)
    project.status = get_object_or_404(ProjectStatus, status='Completed')
    project.save()
    messages.success(request, 'Project Successfully Marked Completed!')
    return redirect(reverse(project_details, args=[project_id]))


@login_required
@custom_user_test(manager_test, login_url='/projects/',
                  redirect_field_name=None)
def cancel_project(request, project_id):
    """ View to mark job as completed """
    project = get_object_or_404(Project, pk=project_id)
    project.status = get_object_or_404(ProjectStatus, status='Cancelled')
    project.save()
    messages.info(request, 'Project Successfully Cancelled')
    return redirect(reverse(project_details, args=[project_id]))


@login_required
@custom_user_test(manager_test, login_url='/projects/',
                  redirect_field_name=None)
def reopen_project(request, project_id):
    """ View to mark job as completed """
    project = get_object_or_404(Project, pk=project_id)
    project.status = get_object_or_404(ProjectStatus, status='In Progress')
    project.save()
    messages.success(request, 'Project Successfully Reopened!')
    return redirect(reverse(project_details, args=[project_id]))
