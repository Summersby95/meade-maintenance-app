from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('jobs/', include('jobs.urls')),
    path('projects/', include('projects.urls')),
    path('assets/', include('assets.urls')),
    path('stocks/', include('stocks.urls')),
    path('people/', include('profiles.urls')),
    path('notifications/', include('notifications.urls')),
]
