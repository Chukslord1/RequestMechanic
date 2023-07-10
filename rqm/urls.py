"""rqm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# API VERSION
"""Multiple API VERSIONS can be defined here and called in the urls patterns"""
api_version = 'v1'

schema_view = get_schema_view(
    openapi.Info(
        title="RQM API",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ipeluwa@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name="schema"),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path(api_version + '/user/', include('userauth.urls')),
    # path(api_version + '/social_auth/', include('social_auth.urls')),
    # path(api_version + '/profile/', include('userprofile.urls')),
    path('sentry-debug/', trigger_error),


]
