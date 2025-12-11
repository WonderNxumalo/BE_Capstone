"""
URL configuration for event_management_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from events.views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny

# User Registration (Stretch Goal - simple view)
from rest_framework import generics
from events.serializers import UserRegistrationSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    # DRF Login/Logout (Built-in Auth)
    path('api-auth/', include('rest_framework.urls')), 
    # API Endpoints
    path('api/v1/', include('events.urls')),
    # User Registration Endpoint
    path('api/v1/register/', RegisterUser.as_view(), name='register'),
    # Custom User Detail Endpoints (e.g., api/v1/users/1/)
    path('api/v1/', include(router.urls)),
]
