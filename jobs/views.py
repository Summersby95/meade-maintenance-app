from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Job, JobStatus, JobSteps, JobTimes
from .forms import JobForm, JobStepsForm, JobTimesForm
from .decorators import custom_user_test, job_cancel_check, job_edit_check

from profiles.models import UserProfile
from projects.models import Project
from stocks.models import StockTransfer
from projects.views import project_details

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
            'href': 'create_job',
            'text': 'Create Job',
        },
    ],
}


@login_required
def outstanding_jobs(request):
    """ View to see outstanding jobs for user """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            (Q(status=JobStatus.objects.get(status='Not Started')) | Q(status=JobStatus.objects.get(status='Started')))
            & Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None)) &
            (Q(status=JobStatus.objects.get(status='Not Started')) | Q(status=JobStatus.objects.get(status='Started')))
            & Q(ppm=None)
        )

    context = {
        'jobs': jobs,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_table.html', context)


@login_required
def outstanding_ppms(request):
    """ View to see outstanding ppms for user """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if str(profile.user_type).lower() in ("admin", "manager"):
        jobs = Job.objects.filter(
            (Q(status=JobStatus.objects.get(status='Not Started')) | Q(status=JobStatus.objects.get(status='Started')))
            & ~Q(ppm=None)
        )
    else:
        jobs = Job.objects.filter(
            (Q(assigned_to=request.user) | Q(assigned_to=None)) &
            (Q(status=JobStatus.objects.get(status='Not Started')) | Q(status=JobStatus.objects.get(status='Started')))
            & ~Q(ppm=None)
        )

    context = {
        'jobs': jobs,
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

    context = {
        'job': job,
        'job_steps': job_steps,
        'job_times': job_times,
        'job_transfers': job_transfers,
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
    job=get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = JobTimesForm(request.POST)
        if form.is_valid():
            job_time = JobTimes(job=job, **form.cleaned_data)
            job_time.save()
            messages.success(request, "Time Log Successfully Created!")
            return redirect(reverse(job_details, args=[job_id]))
        else:
            messages.error(request, "Error Creating Time Log! Please Try Again")
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
@custom_user_test(job_cancel_check, login_url='/jobs/', redirect_field_name=None)
def reopen_job(request, job_id):
    """ View to reopen job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Started')
    job.save()
    messages.success(request, "Job Successfully Reopened!")
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_cancel_check, login_url='/jobs/', redirect_field_name=None)
def cancel_job(request, job_id):
    """ View to cancel job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Cancelled')
    job.save()
    messages.success(request, "Job Successfully Cancelled!")
    return redirect(reverse(job_details, args=[job_id]))