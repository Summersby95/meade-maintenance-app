from django.shortcuts import get_object_or_404, render
from .models import Job, JobSteps, JobTimes


def outstanding_jobs(request):
    """ View to see outstanding jobs for user """
    
    jobs = Job.objects.filter()

    context = {
        'jobs': jobs,
    }

    return render(request, 'jobs/job_table.html', context)


# Create your views here.
