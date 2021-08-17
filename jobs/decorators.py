from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from jobs.models import Job


def job_edit_check(request):
    """
    Custom decorator test function that checks if the user is an admin,
    manager or creator of the job or the job is unassigned and the user's
    department is the same as the job's department.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    job_id = request.build_absolute_uri().split('/')[-2]
    job = get_object_or_404(Job, id=job_id)

    res = False

    if str(profile.user_type).lower() in ('admin', 'manager'):
        res = True
    elif job.created_by == request.user:
        res = True
    elif request.user in job.assigned_to.all():
        res = True
    elif job.assigned_to.count() == 0:
        res = True

    return res


def job_cancel_check(request):
    """
    Custom decorator test function that checks if the user is an
    admin, manager or creator of the job
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    job_id = request.build_absolute_uri().split('/')[-2]
    job = get_object_or_404(Job, id=job_id)

    res = False

    if str(profile.user_type).lower() in ('admin', 'manager'):
        res = True
    elif job.created_by == request.user:
        res = True
    elif request.user in job.assigned_to.all():
        res = True

    return res
