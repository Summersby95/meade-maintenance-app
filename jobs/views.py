from django.shortcuts import get_object_or_404, render
from .models import Job, JobSteps, JobTimes
from .forms import JobForm, JobStepsForm


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
            form.save()
            return outstanding_jobs(request)
        else:
            print(form.errors)
    else:
        form = JobForm()
        stepsForm = JobStepsForm()
    
    context = {
        'form': form,
        'stepsForm': stepsForm,
    }

    return render(request, 'jobs/create_job.html', context)


def edit_job(request, job_id):
    """ View to edit job """
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return outstanding_jobs(request)
        else:
            print(form.errors)
    else:
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
    }

    return render(request, 'jobs/edit_job.html', context)