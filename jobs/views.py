import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Job, JobStatus, JobSteps, JobTimes
from .forms import JobForm, JobStepsForm, JobTimesForm
from .decorators import job_cancel_check, job_edit_check

from ancillaries.decorators import custom_user_test, manager_test
from profiles.models import UserProfile
from projects.models import Project
from stocks.models import StockTransfer
from projects.views import project_details

"""
The app context dictionary tells the template
which app is active and which links to show
in the sidebar
"""
app_context = {
    'nbar': 'jobs',
    'links': [
        {
            'href': 'outstanding_jobs',
            'text': 'Outstanding Jobs',
        },
        {
            'href': 'outstanding_ppms',
            'text': 'Outstanding PPMs',
        },
        {
            'href': 'completed_jobs',
            'text': 'Completed Jobs',
        },
        {
            'href': 'completed_ppms',
            'text': 'Completed PPMs',
        },
        {
            'href': 'create_job',
            'text': 'Create Job',
        },
        {
            'href': 'user_started_logs',
            'text': 'My Started Time Logs',
        },
        {
            'href': 'user_completed_logs',
            'text': 'My Time Logs',
        }
    ],
}


@login_required
def outstanding_jobs(request):
    """ View to see outstanding jobs for user """
    profile = get_object_or_404(UserProfile, user=request.user)

    """
    For manager/admin users we want to show all the jobs,
    regardless of who is assigned or who created it.
    For regular users we only want to show them jobs that are
    applicable to them
    """
    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            ~Q(status=JobStatus.objects.get(status='Completed')) &
            ~Q(status=JobStatus.objects.get(status='Cancelled'))
            & Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None) |
             Q(created_by=request.user)) &
            ~Q(status=JobStatus.objects.get(status='Completed')) &
            ~Q(status=JobStatus.objects.get(status='Cancelled'))
            & Q(ppm=None)
        )

    context = {
        'jobs': jobs,
        'table_header': 'Outstanding Jobs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
def outstanding_ppms(request):
    """ View to see outstanding ppms for user """
    profile = get_object_or_404(UserProfile, user=request.user)

    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            ~Q(status=JobStatus.objects.get(status='Completed')) &
            ~Q(status=JobStatus.objects.get(status='Cancelled'))
            & ~Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None) |
             Q(created_by=request.user)) &
            ~Q(status=JobStatus.objects.get(status='Completed')) &
            ~Q(status=JobStatus.objects.get(status='Cancelled'))
            & ~Q(ppm=None)
        )

    context = {
        'jobs': jobs,
        'table_header': 'Outstanding PPMs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
def completed_jobs(request):
    """ View to see completed jobs for user """
    profile = get_object_or_404(UserProfile, user=request.user)

    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            Q(status=JobStatus.objects.get(status='Completed'))
            & Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None) |
             Q(created_by=request.user)) &
            Q(status=JobStatus.objects.get(status='Completed'))
            & Q(ppm=None)
        )

    context = {
        'jobs': jobs,
        'table_header': 'Completed Jobs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
def completed_ppms(request):
    """ View to see completed ppms for user """
    profile = get_object_or_404(UserProfile, user=request.user)

    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            Q(status=JobStatus.objects.get(status='Completed'))
            & ~Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None)) &
            Q(status=JobStatus.objects.get(status='Completed'))
            & ~Q(ppm=None)
        )

    context = {
        'jobs': jobs,
        'table_header': 'Completed PPMs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/', redirect_field_name=None)
def user_jobs(request, user_id):
    """ View to see jobs for user """
    employee = get_object_or_404(UserProfile, id=user_id)

    jobs = Job.objects.filter(
        Q(assigned_to__in=[employee.user]) | Q(created_by=employee.user)
    ).distinct().order_by('-created_on')

    context = {
        'jobs': jobs,
        'table_header': f'{employee.get_full_name()}\'s Jobs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
def job_details(request, job_id):
    """ View to see details of a job """
    job = get_object_or_404(Job, pk=job_id)

    job_steps = JobSteps.objects.filter(job=job_id)
    job_times = JobTimes.objects.filter(job=job_id)
    job_transfers = StockTransfer.objects.filter(job=job_id)

    user_started = JobTimes.objects.filter(
        job=job_id,
        user=request.user,
        time_end__isnull=True
    ).count()

    """
    The card tabs context variable tells the details template
    which card tabs to render.
    """
    context = {
        'job': job,
        'job_steps': job_steps,
        'job_times': job_times,
        'job_transfers': job_transfers,
        'user_started': user_started,
        'card_tabs': [
            {
                'header': f'Job #{job.id}',
                'template': 'jobs/job_details_card.html'
            },
            {
                'header': 'Job Steps',
                'template': 'jobs/job_steps_table.html'
            },
            {
                'header': 'Parts Used',
                'template': 'projects/parts_used_card.html'
            },
            {
                'header': 'Job Times',
                'template': 'jobs/job_times_table.html'
            },
        ],
        'actions': 'jobs/job_details_actions.html',
    }
    context = {**context, **app_context}

    return render(request, 'includes/details.html', context)


@login_required
def create_job(request):
    """ View to create job """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, profile=profile)

        if form.is_valid():
            job = form.save()
            for key, value in request.POST.items():
                if 'step' in key:
                    step_form = JobStepsForm({
                        'job': job.id,
                        'step_number': key.split('_')[1],
                        'step': value,
                    })
                    if step_form.is_valid():
                        step_form.save()
                    else:
                        print(step_form.errors)

            messages.success(request, "Job Successfully Created!")
            return redirect(reverse(job_details, args=[job.id]))
        else:
            messages.error(request, "Error Creating Job! Please Try Again")
            print(form.errors)
    else:
        form = JobForm(profile=profile)

    context = {
        'form': form,
        'action': reverse(create_job),
        'header': 'Create Job',
        'submit_text': 'Create Job',
        'cancel': reverse(outstanding_jobs),
        'extra_form': 'jobs/steps_template.html',
        'extra_form_header': 'Steps (Optional)',
        'form_js': 'js/steps.js',
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
def create_project_job(request, project_id):
    """ View to create job for project """
    project = get_object_or_404(Project, pk=project_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    form = JobForm(profile=profile, initial={'project': project})

    context = {
        'form': form,
        'action': reverse(create_job),
        'header': 'Create Job',
        'submit_text': 'Create Job',
        'cancel': reverse(project_details, args=[project.id]),
        'extra_form': 'jobs/steps_template.html',
        'extra_form_header': 'Steps (Optional)',
        'form_js': 'js/steps.js',
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/', redirect_field_name=None)
def edit_job(request, job_id):
    """ View to edit job """
    job = get_object_or_404(Job, pk=job_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    job_steps = JobSteps.objects.filter(job=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job, profile=profile)
        if form.is_valid():
            job = form.save()
            job_steps.delete()
            for key, value in request.POST.items():
                if 'step' in key:
                    step_form = JobStepsForm({
                        'job': job.id,
                        'step_number': key.split('_')[1],
                        'step': value,
                    })
                    if step_form.is_valid():
                        step_form.save()
                    else:
                        print(step_form.errors)

            messages.success(request, "Job Successfully Updated!")
            return redirect(reverse(job_details, args=[job.id]))
        else:
            messages.error(request, "Error Updating Job! Please Try Again")
            print(form.errors)
    else:
        form = JobForm(instance=job, profile=profile)

    context = {
        'form': form,
        'job_steps': job_steps,
        'action': reverse(edit_job, args=[job.id]),
        'header': 'Edit Job',
        'submit_text': 'Update Job',
        'cancel': reverse(job_details, args=[job.id]),
        'extra_form': 'jobs/steps_template.html',
        'extra_form_header': 'Steps (Optional)',
        'form_js': 'js/steps.js',
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/', redirect_field_name=None)
def create_time_log(request, job_id):
    """ View to create time log """
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = JobTimesForm(request.POST)
        if form.is_valid():
            time_log = form.save(commit=False)
            time_log.job = job
            time_log.user = request.user
            time_log.save()
            messages.success(request, "Time Log Successfully Created!")
            return redirect(reverse(job_details, args=[job_id]))
        else:
            messages.error(
                request, "Error Creating Time Log! Please Try Again"
            )
            print(form.errors)
    else:
        form = JobTimesForm()

    context = {
        'form': form,
        'action': reverse(create_time_log, args=[job_id]),
        'header': 'Create Time Log',
        'submit_text': 'Log Time',
        'cancel': reverse(job_details, args=[job_id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/', redirect_field_name=None)
def mark_completed(request, job_id):
    """ View to mark job as completed """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Completed')
    job.save()
    messages.success(request, "Job Successfully Marked Completed!")
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/',
                  redirect_field_name=None)
def reopen_job(request, job_id):
    """ View to reopen job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Started')
    job.save()
    messages.success(request, "Job Successfully Reopened!")
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_cancel_check, login_url='/jobs/',
                  redirect_field_name=None)
def cancel_job(request, job_id):
    """ View to cancel job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Cancelled')
    job.save()
    messages.success(request, "Job Successfully Cancelled!")
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/',
                  redirect_field_name=None)
def start_job_log(request, job_id):
    """ View to create inital time_log """
    job = get_object_or_404(Job, pk=job_id)
    """
    we check if the user has any open time logs
    for this job, we don't want multiple open time logs
    for the same job running at the same time
    """
    start_check = JobTimes.objects.filter(
        job=job,
        user=request.user,
        time_start__isnull=False,
        time_end__isnull=True
    ).count()

    if start_check > 0:
        messages.error(request, "You already have a start time"
                       " log for this job!")
        return redirect(reverse(job_details, args=[job_id]))

    job_time = JobTimes(
        job=job,
        time_start=datetime.datetime.now(),
        user=request.user,
    )
    job_time.save()
    messages.success(request, "Time Log Successfully Started!")
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/',
                  redirect_field_name=None)
def stop_job_log(request, job_id):
    """ View to stop time log """
    job = get_object_or_404(Job, pk=job_id)
    job_time = get_object_or_404(JobTimes, job=job, user=request.user,
                                 time_end__isnull=True)
    job_time.time_end = datetime.datetime.now()
    job_time.save()
    messages.success(request, "Time Log Successfully Stopped!")
    return redirect(reverse(job_details, args=[job_time.job.id]))


@login_required
def user_started_logs(request):
    """ View to show logs that the user started """
    time_logs = JobTimes.objects.filter(
        user=request.user,
        time_start__isnull=False,
        time_end__isnull=True
    ).order_by('-time_start')

    context = {
        'time_logs': time_logs,
        'table_title': 'My Started Logs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/user_time_logs_table.html', context)


@login_required
def user_completed_logs(request):
    """ View to show logs that the user completed """
    time_logs = JobTimes.objects.filter(
        user=request.user,
        time_start__isnull=False,
        time_end__isnull=False
    ).order_by('-time_end')

    context = {
        'time_logs': time_logs,
        'table_title': 'My Completed Logs',
    }
    context = {**context, **app_context}

    return render(request, 'jobs/user_time_logs_table.html', context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def user_logs(request, user_id):
    """ View to show logs that the user completed """
    employee = get_object_or_404(UserProfile, pk=user_id)
    time_logs = JobTimes.objects.filter(
        user=employee.user,
        time_start__isnull=False,
        time_end__isnull=False
    ).order_by('-time_start')

    context = {
        'time_logs': time_logs,
        'table_title': '{}\'s Time Logs'.format(employee.get_full_name())
    }
    context = {**context, **app_context}

    return render(request, 'jobs/user_time_logs_table.html', context)


@login_required
def edit_time_log(request, time_log_id):
    """ View to edit time log """
    time_log = get_object_or_404(JobTimes, pk=time_log_id)
    job = time_log.job
    if request.method == 'POST':
        form = JobTimesForm(request.POST, instance=time_log)
        if form.is_valid():
            time_log = form.save(commit=False)
            time_log.save()
            messages.success(request, "Time Log Successfully Updated!")
            return redirect(reverse(job_details, args=[job.id]))
        else:
            messages.error(
                request, "Error Updating Time Log! Please Try Again"
            )
            print(form.errors)
    else:
        form = JobTimesForm(instance=time_log)

    context = {
        'form': form,
        'action': reverse(edit_time_log, args=[time_log_id]),
        'header': 'Edit Time Log',
        'submit_text': 'Save Time Log',
        'cancel': reverse(job_details, args=[job.id]),
    }
    context = {**context, **app_context}

    return render(request, 'includes/form.html', context)


@login_required
def delete_time_log(request, time_log_id):
    """ View to delete time log """
    time_log = get_object_or_404(JobTimes, pk=time_log_id)
    job = time_log.job
    time_log.delete()
    messages.success(request, "Time Log Successfully Deleted!")
    return redirect(reverse(job_details, args=[job.id]))


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/',
                  redirect_field_name=None)
def complete_job_steps(request, job_id):
    """ View to complete job steps """
    job = get_object_or_404(Job, pk=job_id)
    job_steps = JobSteps.objects.filter(job=job)
    if request.method == 'POST':
        for job_step in job_steps:
            if request.POST.get(
                f"step_{job_step.step_number}_checkbox"
            ) == 'on':
                job_step.completed = True
            else:
                job_step.completed = False
            job_step.save()
        messages.success(request, "Job Steps Updated Successfully!")
        return redirect(reverse(job_details, args=[job_id]))

    context = {
        'job_steps': job_steps,
        'job': job,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_steps_form_table.html', context)
