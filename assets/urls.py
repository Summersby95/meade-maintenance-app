from django.contrib import admin
from django.urls import path, include
from . import views

""" Url Patterns For Assets App """
urlpatterns = [
    path('', views.active_assets, name='active_assets'),
    path('inactive/', views.inactive_assets, name='inactive_assets'),
    path('<int:asset_id>/', views.asset_details, name='asset_details'),
    path('create_asset/', views.create_asset, name='create_asset'),
    path('edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('edit_asset/inactive/<int:asset_id>/', views.make_asset_inactive,
         name='make_asset_inactive'),
    path('edit_asset/active/<int:asset_id>/', views.make_asset_active,
         name='make_asset_active'),
    path('add_ppm/<int:asset_id>/', views.add_ppm, name='add_ppm'),
    path('ppm/<int:ppm_id>/', views.ppm_details, name='ppm_details'),
]
