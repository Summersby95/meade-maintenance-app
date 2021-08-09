from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inventory_view, name='inventory_view'),
]