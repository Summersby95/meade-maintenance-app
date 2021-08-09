from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inventory_view, name='inventory_view'),
    path('<int:stock_id>/', views.stock_item_details, name='stock_item_details'),
    path('create_item/', views.create_stock_item, name='create_stock_item'),
    path('receive_stock/', views.create_stock_receipt, name='create_stock_receipt'),
]