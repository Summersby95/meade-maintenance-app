from django.shortcuts import get_object_or_404, render, redirect, reverse
from .models import Job, JobStatus, JobSteps, JobTimes
from .forms import JobForm, JobStepsForm, JobTimesForm


def outstanding_jobs(request):
    """ View to see outstanding jobs for user """
    
    jobs = Job.objects.filter()

    context = {
        'jobs': jobs,
    }

    return render(request, 'jobs/job_table.html', context)


def job_details(request, job_id):
    """ View to see details of a job """
    
    job = get_object_or_404(Job, pk=job_id)

    job_steps = JobSteps.objects.filter(job=job_id)

    job_times = JobTimes.objects.filter(job=job_id)

    context = {
        'job': job,
        'job_steps': job_steps,
        'job_times': job_times,
    }

    return render(request, 'jobs/job_details.html', context)


def create_job(request):
    """ View to create job """
    if request.method == 'POST':
        form = JobForm(request.POST)
        
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
        form = JobForm()
    
    context = {
        'form': form,
    }

    return render(request, 'jobs/create_job.html', context)


def edit_job(request, job_id):
    """ View to edit job """
    job = get_object_or_404(Job, pk=job_id)
    job_steps = JobSteps.objects.filter(job=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
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
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'job_steps': job_steps,
    }

    return render(request, 'jobs/edit_job.html', context)


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

    return render(request, 'jobs/create_time_log.html', context)


def mark_completed(request, job_id):
    """ View to mark job as completed """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Completed')
    job.save()
    return redirect(reverse(job_details, args=[job_id]))


def reopen_job(request, job_id):
    """ View to reopen job """
    job = get_object_or_404(Job, pk=job_id)
    job.status = get_object_or_404(JobStatus, status='Started')
    job.save()
    return redirect(reverse(job_details, args=[job_id]))

