from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_table, name='notification_table'),
    path('read/', views.read_notifications, name='read_notifications'),
]
