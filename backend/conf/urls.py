import json

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from rest_framework.schemas.openapi import SchemaGenerator

from core.views import React
from core.viewsets import UserViewSet, ParserViewSet


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('text', ParserViewSet, basename='text')

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^.*', React.as_view(), name='index'),
]


# Generate schema file on reload in development (it must be in urls.py to run once per reload)
if settings.DEBUG:
    with open('/code/conf/openapi_schema.json', 'w') as f:
        json.dump(
            SchemaGenerator(patterns=urlpatterns).get_schema(request=None, public=True),
            f,
            indent=2,
        )
