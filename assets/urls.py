from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.active_assets, name='active_assets'),
]