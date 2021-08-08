from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.active_assets, name='active_assets'),
    path('inactive/', views.inactive_assets, name='inactive_assets'),
    path('<int:asset_id>/', views.asset_details, name='asset_details'),
    path('create_asset/', views.create_asset, name='create_asset'),
    path('edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('add_ppm/<int:asset_id>/', views.add_ppm, name='add_ppm'),
]