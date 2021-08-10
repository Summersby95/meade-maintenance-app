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


# Create your views here.
