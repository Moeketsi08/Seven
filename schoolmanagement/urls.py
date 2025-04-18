"""schoolmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView  # Add this import
from .views import home_page
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('', include('center_manager.urls')),
    # path('center_manager/', include('center_manager.urls')),
    path('teacher/', include('teacher.urls')),
    path('learner/', include('learner.urls')),
    path('academic/', include('academic.urls')),
    path('employee/', include('employee.urls')),
    # path('result/', include('result.urls')),
    path('address/', include('address.urls')),
    # path('account/', include('account.urls')),
    path('attendance/', include('attendance.urls')),
    # path('advanced_filters/', include('advanced_filters.urls'))
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("select2/", include("django_select2.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
