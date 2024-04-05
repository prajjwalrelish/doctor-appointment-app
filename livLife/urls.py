"""livLife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from usermgmt.views import LogoutAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="LivLife Backend API",
        default_version='v1',
        description="This Page includes all the apis for backend",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^api/', include('appointment.urls')),
    url(r'^api/', include('payment.urls')),
    url(r'api/', include('healthtest.urls')),
    url(r'^api/', include('usermgmt.urls')),
    
]
urlpatterns += [
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    url(r'^admin-pannel/', admin.site.urls),
    url(r'^login$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^logout$', LogoutAPIView.as_view(), name='logout_view'),
    url(r'^token/refresh$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^token/verify$', TokenVerifyView.as_view(), name='token_verify'),
    url('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    url('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
    url('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
