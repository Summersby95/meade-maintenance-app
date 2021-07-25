from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.outstanding_jobs, name='outstanding_jobs'),
    path('<int:job_id>', views.job_details, name='job_detail'),
]