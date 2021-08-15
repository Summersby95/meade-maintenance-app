import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum

from jobs.models import Job, JobStatus, JobTimes
from projects.models import Project, ProjectStatus


app_context = {
    'nbar': 'dashboard',
    'links': [
        {
            'href': 'dashboard',
            'text': 'Dashboard',
        },
    ],
}


@login_required
def dashboard(request):
    """Returns dashboard home"""
    jobs = {
        'all': Job.objects.all().count(),
        'completed': Job.objects.filter(
            status=JobStatus.objects.get(status='Completed')
        ).count(),
        'started': Job.objects.filter(
            status=JobStatus.objects.get(status='Started')
        ).count(),
        'cancelled': Job.objects.filter(
            status=JobStatus.objects.get(status='Cancelled')
        ).count(),
    }
    jobs['outstanding'] = jobs['all'] - jobs['completed'] - jobs['cancelled']

    projects = {
        'all': Project.objects.all().count(),
        'completed': Project.objects.filter(
            status=ProjectStatus.objects.get(status='Completed')
        ).count(),
        'project_jobs': Job.objects.filter(~Q(project=None)).count(),
        'total_time_logged': sum(
            [jt.time_diff() for jt in JobTimes.objects.filter(
                ~Q(job__project=None)
            )],
            datetime.timedelta()
        ),
    }

    people = {
        'in_today': JobTimes.objects.filter(
            time_start__date=datetime.datetime.now().date()
        ).values('user').distinct().count(),
        'hours_today': sum(
            [jt.time_diff() for jt in JobTimes.objects.filter(
                time_start__date=datetime.datetime.now().date()
            )],
            datetime.timedelta()
        ),
        'hours_week': sum(
            [jt.time_diff() for jt in JobTimes.objects.filter(
                time_start__range=(
                    datetime.datetime.now() - datetime.timedelta(days=7),
                    datetime.datetime.now()
                )
            )],
            datetime.timedelta()
        ),
        'hours_month': sum(
            [jt.time_diff() for jt in JobTimes.objects.filter(
                time_start__range=(
                    datetime.datetime.now() - datetime.timedelta(days=30),
                    datetime.datetime.now()
                )
            )],
            datetime.timedelta()
        ),
    }

    charts = {
        'jobs': {
            'today': {
                'completed_today': Job.objects.filter(
                    status=JobStatus.objects.get(status='Completed'),
                    created_on__date=datetime.datetime.now().date()
                ).count(),
                'started_today': Job.objects.filter(
                    ~Q(status=JobStatus.objects.get(status='Completed')),
                    created_on__date=datetime.datetime.now().date()
                ).count(),
            },
            'week': {
                'completed_week': Job.objects.filter(
                    status=JobStatus.objects.get(status='Completed'),
                    created_on__range=(
                        datetime.datetime.now() - datetime.timedelta(days=7),
                        datetime.datetime.now()
                    )
                ).count(),
                'started_week': Job.objects.filter(
                    ~Q(status=JobStatus.objects.get(status='Completed')),
                    created_on__range=(
                        datetime.datetime.now() - datetime.timedelta(days=7),
                        datetime.datetime.now()
                    )
                ).count(),
            },
        },
        'hours': {
            'today': {
                'project_hours': sum(
                    [jt.time_diff() for jt in JobTimes.objects.filter(
                        ~Q(job__project=None),
                        time_start__date=datetime.datetime.now().date()
                    )],
                    datetime.timedelta()
                ).seconds//3600,
                'total_hours': sum(
                    [jt.time_diff() for jt in JobTimes.objects.filter(
                        time_start__date=datetime.datetime.now().date()
                    )],
                    datetime.timedelta()
                ).seconds//3600,
            },
            'week': {
                'project_hours': sum(
                    [jt.time_diff() for jt in JobTimes.objects.filter(
                        ~Q(job__project=None),
                        time_start__range=(
                            (datetime.datetime.now() -
                             datetime.timedelta(days=7)),
                            datetime.datetime.now()
                        )
                    )],
                    datetime.timedelta()
                ).seconds//3600,
                'total_hours': sum(
                    [jt.time_diff() for jt in JobTimes.objects.filter(
                        time_start__range=(
                            (datetime.datetime.now() -
                             datetime.timedelta(days=7)),
                            datetime.datetime.now()
                        )
                    )],
                    datetime.timedelta()
                ).seconds//3600,
            },
        },
    }

    context = {
        'jobs': jobs,
        'projects': projects,
        'people': people,
        'charts': charts,
    }
    context = {**context, **app_context}

    return render(request, 'dashboard/dashboard.html', context)
