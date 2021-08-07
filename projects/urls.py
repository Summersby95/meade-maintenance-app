from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ongoing_projects, name='ongoing_projects'),
    path('<int:project_id>/', views.project_details, name='project_details'),
