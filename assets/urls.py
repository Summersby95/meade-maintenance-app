from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.active_assets, name='active_assets'),
    path('inactive/', views.inactive_assets, name='inactive_assets'),
    path('<int:asset_id>/', views.asset_details, name='asset_details'),
    path('edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
]