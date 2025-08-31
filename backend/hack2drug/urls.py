"""
URL configuration for hack2drug project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api-info/', views.api_info, name='api_info'),
    path('health/', views.health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('api.rest_urls')),
    path('users/', include('users.urls')),
    path('detection/', include('detection.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('analytics/', include('analytics.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
