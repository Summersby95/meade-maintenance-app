from django.shortcuts import get_object_or_404, render
from .models import Job, JobSteps, JobTimes


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