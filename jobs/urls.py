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
    path('start/<int:job_id>/', views.start_job_log, name='start_job_log'),
    path('stop/<int:job_id>/', views.stop_job_log, name='stop_job_log'),
    path('started/', views.user_started_logs, name='user_started_logs'),
    path('my_logs/', views.user_completed_logs, name='user_completed_logs'),
    path('time_log/edit/<int:time_log_id>/', views.edit_time_log,
         name='edit_time_log'),
    path('time_log/delete/<int:time_log_id>', views.delete_time_log,
         name='delete_time_log'),
    path('complete_steps/<int:job_id>/', views.complete_job_steps,
         name='complete_job_steps'),
]
