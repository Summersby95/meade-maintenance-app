from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ongoing_projects, name='ongoing_projects'),
