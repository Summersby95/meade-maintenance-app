from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.outstanding_jobs, name='outstanding_jobs'),
    path('<int:job_id>/', views.job_details, name='job_detail'),
    path('create_job/', views.create_job, name='create_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
]