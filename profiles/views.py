import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.conf import settings

from .models import UserBonusOrder, UserProfile
from .forms import BonusOrderForm
from jobs.models import Job, JobStatus, JobTimes
from stocks.models import StockTransfer
from ancillaries.decorators import custom_user_test, manager_test

import stripe


app_context = {
    'nbar': 'people',
    'links': [
        {
            'href': 'staff_list',
            'text': 'Staff List',
        }
    ]
}

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def staff_list(request):
    staff_list = UserProfile.objects.all()

    context = {
        'staff_list': staff_list,
    }
    context = {**app_context, **context}

    return render(request, 'profiles/staff_list.html', context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def staff_detail(request, staff_id):
    employee = UserProfile.objects.get(id=staff_id)
    jobs = Job.objects.filter(
        Q(assigned_to__in=[employee.user]) | Q(created_by=employee.user)
    ).distinct().order_by('-created_on')[:10]
    total_jobs = Job.objects.filter(
        Q(assigned_to__in=[employee.user]) | Q(created_by=employee.user)
    ).distinct().count()
    stock_withdrawls = StockTransfer.objects.filter(user=employee.user)[:10]
    total_stock_withdrawls = StockTransfer.objects.filter(
        user=employee.user
    ).count()
    time_logs_list = JobTimes.objects.filter(
        ~Q(time_end=None), user=employee.user
    ).order_by('-time_start')[:10]
    time_logs = JobTimes.objects.filter(~Q(time_end=None), user=employee.user)

    cancelled_jobs = jobs.filter(
        Q(assigned_to__in=[employee.user]) | Q(created_by=employee.user)
    ).count()
    completed_jobs = jobs.filter(
        status=JobStatus.objects.get(status='Completed')
    ).count()
    started_jobs = jobs.filter(
        status=JobStatus.objects.get(status='Started')
    ).count()
    outstanding_jobs = jobs.filter(
        ~Q(status=JobStatus.objects.get(status='Completed'))
    ).count()

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
    hours_all = sum(
        [time.time_diff() for time in time_logs], datetime.timedelta()
    )

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
        'card_tabs': [
            {
                'header': f'Employee #{employee.id}',
                'template': 'profiles/employee_details_card.html'
            },
            {
                'header': 'Job Statistics',
                'template': 'profiles/employee_job_statistics_card.html',
                'card': 'includes/card-6.html',
            },
            {
                'header': 'Hours Logged',
                'template': 'profiles/employee_hours_logged_card.html',
                'card': 'includes/card-6.html',
            },
            {
                'header': 'Jobs',
                'template': 'profiles/employee_jobs_table_card.html',
            },
            {
                'header': 'Stock Withdrawls',
                'template': ('profiles/'
                             'employee_stock_withdrawls_table_card.html'),
            },
            {
                'header': 'Time Logs',
                'template': 'profiles/employee_time_logs_table_card.html',
            },
        ],
        'actions': 'profiles/staff_detail_actions.html',
    }
    context = {**app_context, **context}

    return render(request, 'includes/details.html', context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def user_bonus(request, staff_id):
    employee = UserProfile.objects.get(id=staff_id)

    bonus_form = BonusOrderForm()

    context = {
        'employee': employee,
        'form': bonus_form,
    }
    context = {**app_context, **context}

    return render(request, 'profiles/user_bonus.html', context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
@require_http_methods(['POST'])
def create_checkout_session(request, staff_id):
    employee = UserProfile.objects.get(id=staff_id)
    url_vars = [
        "http://",
        str(request.get_host()),
        "/people/bonus/",
        str(employee.id),
        "/success/{CHECKOUT_SESSION_ID}/"
    ]
    checkout_success_url = ''.join(url_vars)
    bonus_amount = int(request.POST.get('bonus')) * 100
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f'Bonus for {employee.get_full_name()}',
                },
                'unit_amount': bonus_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=checkout_success_url,
        cancel_url=request.build_absolute_uri(
            reverse(bonus_cancel, args=[staff_id])
        ),
    )
    print(request.get_host())

    return redirect(checkout_session.url, code=303)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def bonus_success(request, staff_id, checkout_session_id):
    employee = get_object_or_404(UserProfile, id=staff_id)
    if stripe.checkout.Session.retrieve(checkout_session_id):
        session = stripe.checkout.Session.retrieve(checkout_session_id)
    else:
        messages.error(request, "Something went wrong. Please try again.")
        return redirect(reverse(staff_detail, args=[staff_id]))

    customer = stripe.Customer.retrieve(session.customer)
    amount_total = format((int(session.amount_total)/100), '.2f')

    UserBonusOrder.objects.create(
        user=request.user,
        bonus=amount_total,
    )

    context = {
        'session': session,
        'customer': customer,
        'employee': employee,
        'amount_total': amount_total,
        'card_tabs': [
            {
                'header': 'Employee Bonus',
                'template': 'profiles/employee_bonus_card.html',
            }
        ],
        'actions': 'profiles/bonus_success_actions.html',
    }
    context = {**app_context, **context}
    messages.success(request, f'Bonus Payment Success For {customer.name}!')
    return render(request, "includes/details.html", context)


@login_required
@custom_user_test(manager_test, login_url='/jobs/',
                  redirect_field_name=None)
def bonus_cancel(request, staff_id):
    employee = get_object_or_404(UserProfile, id=staff_id)
    messages.error(
        request, f'Bonus Payment Cancelled For {employee.get_full_name()}!'
    )
    return redirect(reverse(staff_detail, args=[staff_id]))
