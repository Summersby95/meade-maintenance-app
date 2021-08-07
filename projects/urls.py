from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ongoing_projects, name='ongoing_projects'),
    path('<int:project_id>/', views.project_details, name='project_details'),
    path('create_project/', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
