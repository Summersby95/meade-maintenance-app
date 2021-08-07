from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ongoing_projects, name='ongoing_projects'),
    path('<int:project_id>/', views.project_details, name='project_details'),
    path('create_project/', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('mark_completed/<int:project_id>/', views.mark_project_completed, name='mark_project_completed'),
    path('reopen/<int:project_id>/', views.reopen_project, name='reopen_project'),
    path('cancel/<int:project_id>', views.cancel_project, name='cancel_project'),
]