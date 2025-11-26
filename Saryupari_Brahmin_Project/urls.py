"""
URL configuration for Saryupari_Brahmin_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from .views import serve_media
# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('firebase-messaging-sw.js/', serve, {'document_root': settings.BASE_DIR, 'path': 'firebase-messaging-sw.js'}),
    path('', include('administration.urls')),
    path('dashboard/', include('dashboard.urls')),
    # S3 media serving using boto3 - serves images directly from S3
    re_path(r'^media/(?P<file_path>.*)$', serve_media, name='serve_media'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Media files are now served through S3 via boto3, not from local filesystem
