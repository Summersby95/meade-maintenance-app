from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.outstanding_jobs, name='outstanding_jobs'),
    path('ppms/', views.outstanding_ppms, name='outstanding_ppms'),
    path('completed/', views.completed_jobs, name='completed_jobs'),
    path('ppms/completed/', views.completed_ppms, name='completed_ppms'),
    path('<int:job_id>/', views.job_details, name='job_detail'),
    path('create_job/', views.create_job, name='create_job'),
    path('create_job/project/<int:project_id>/', views.create_project_job,
         name='create_project_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('log_time/<int:job_id>/', views.create_time_log,
         name='create_time_log'),
    path('mark_completed/<int:job_id>/', views.mark_completed,
         name='mark_completed'),
    path('reopen/<int:job_id>/', views.reopen_job, name='reopen_job'),
    path('cancel/<int:job_id>/', views.cancel_job, name='cancel_job'),
]
