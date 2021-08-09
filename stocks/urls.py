from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inventory_view, name='inventory_view'),
    path('<int:stock_id>/', views.stock_item_details, name='stock_item_details'),
    path('create_item/', views.create_stock_item, name='create_stock_item'),
    path('edit_item/<int:stock_id>/', views.edit_stock_item, name='edit_stock_item'),
    path('receive_stock/', views.create_stock_receipt, name='create_stock_receipt'),
    path('receive_stock/item/<int:stock_id>/', views.create_item_stock_receipt, name='create_item_stock_receipt'),
    path('receive_stock/edit/<int:receipt_id>/', views.edit_stock_receipt, name='edit_stock_receipt'),
    path('transfer_stock/', views.create_stock_transfer, name='create_stock_transfer'),
    path('transfer_stock/item/<int:stock_id>/', views.create_item_stock_transfer, name='create_item_stock_transfer'),
    path('transfer_stock/edit/<int:transfer_id>/', views.edit_stock_transfer, name='edit_stock_transfer'),
    path('my_unassigned_stock/', views.user_unassigned_stock, name='user_unassigned_stock'),
]