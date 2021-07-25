from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.outstanding_jobs, name='outstanding_jobs'),
