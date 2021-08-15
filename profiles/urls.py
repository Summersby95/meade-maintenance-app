from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('bonus/<int:staff_id>', views.user_bonus, name='user_bonus'),
    path('bonus/<int:staff_id>/checkout_session/',
         views.create_checkout_session, name='create_checkout_session'),
    path('bonus/<int:staff_id>/success/<slug:checkout_session_id>/',
         views.bonus_success, name='bonus_success'),
    path('bonus/<int:staff_id>/cancel/', views.bonus_cancel,
         name='bonus_cancel'),
]
