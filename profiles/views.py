import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Sum
from .models import UserProfile
from jobs.models import Job, JobStatus, JobTimes
from stocks.models import StockTransfer


app_context = {
    'nbar': 'people',
    'links': [
        {
            'href': 'staff_list',
            'text': 'Staff List',
        }
    ]
}


@login_required
def staff_list(request):
    staff_list = UserProfile.objects.all()

    context = {
        'staff_list': staff_list,
    }
    context = {**app_context, **context}

    return render(request, 'profiles/staff_list.html', context)


@login_required
def staff_detail(request, staff_id):
    employee = UserProfile.objects.get(id=staff_id)
    jobs = Job.objects.filter(Q(assigned_to__in=[employee.user]) | Q(created_by=employee.user))
    stock_withdrawls = StockTransfer.objects.filter(user=employee.user)
    time_logs = JobTimes.objects.filter(user=employee.user)

    cancelled_jobs = jobs.filter(status=JobStatus.objects.get(status='Cancelled')).count()
    completed_jobs = jobs.filter(status=JobStatus.objects.get(status='Completed')).count()
    started_jobs = jobs.filter(status=JobStatus.objects.get(status='Started')).count()
    outstanding_jobs = jobs.filter(~Q(status=JobStatus.objects.get(status='Completed'))).count()

    hours_today = sum(
        [time.time_diff() for time in time_logs.filter(
            time_start__date=datetime.date.today()
        )], 
        datetime.timedelta()
    )
    hours_week = sum(
        [time.time_diff() for time in time_logs.filter(
            time_start__date__range=[
                datetime.date.today() - datetime.timedelta(days=7), 
                datetime.date.today()
            ]
        )], 
        datetime.timedelta()
    )
    hours_month = sum(
        [time.time_diff() for time in time_logs.filter(
            time_start__date__range=[
                datetime.date.today() - datetime.timedelta(days=30), 
                datetime.date.today()
            ]
        )], 
        datetime.timedelta()
    )
    hours_all = sum([time.time_diff() for time in time_logs], datetime.timedelta())

    context = {
        'employee': employee,
        'jobs': jobs,
        'stock_withdrawls': stock_withdrawls,
        'time_logs': time_logs,
        'cancelled_jobs': cancelled_jobs,
        'completed_jobs': completed_jobs,
        'started_jobs': started_jobs,
        'outstanding_jobs': outstanding_jobs,
        'hours_today': hours_today,
        'hours_week': hours_week,
        'hours_month': hours_month,
        'hours_all': hours_all,
    }
    context = {**app_context, **context}

    return render(request, 'profiles/staff_detail.html', context)


