from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from jobs.decorators import custom_user_test, job_cancel_check, job_edit_check
from .models import Job, JobStatus, JobSteps, JobTimes
from .forms import JobForm, JobStepsForm, JobTimesForm
from profiles.models import UserProfile
from projects.models import Project
from stocks.models import StockTransfer

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
    }
    context = {**context, **app_context}

    return render(request, 'jobs/job_details.html', context)


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

            return redirect(reverse(job_details, args=[job.id]))
        else:
            print(form.errors)
    else:
        form = JobForm(profile=profile)
    
    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/create_job.html', context)


@login_required
def create_project_job(request, project_id):
    """ View to create job for project """
    project = get_object_or_404(Project, pk=project_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, profile=profile, initial={'project': project})
        
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

            return redirect(reverse(job_details, args=[job.id]))
        else:
            print(form.errors)
    else:
        form = JobForm(profile=profile, initial={'project': project})
    
    context = {
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/create_job.html', context)


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
            return redirect(reverse(job_details, args=[job.id]))
        else:
            print(form.errors)
    else:
        form = JobForm(instance=job, profile=profile)
    
    context = {
        'form': form,
        'job': job,
        'job_steps': job_steps,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/edit_job.html', context)


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
            return redirect(reverse(job_details, args=[job_id]))
        else:
            print(form.errors)
    else:
        form = JobTimesForm()

    context = {
        'job_id': job_id,
        'form': form,
    }
    context = {**context, **app_context}

    return render(request, 'jobs/create_time_log.html', context)


@login_required
@custom_user_test(job_edit_check, login_url='/jobs/', redirect_field_name=None)
def mark_completed(request, job_id):
    """ View to mark job as completed """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Completed')
    job.save()
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_cancel_check, login_url='/jobs/', redirect_field_name=None)
def reopen_job(request, job_id):
    """ View to reopen job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Started')
    job.save()
    return redirect(reverse(job_details, args=[job_id]))


@login_required
@custom_user_test(job_cancel_check, login_url='/jobs/', redirect_field_name=None)
def cancel_job(request, job_id):
    """ View to cancel job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Cancelled')
    job.save()
    return redirect(reverse(job_details, args=[job_id]))