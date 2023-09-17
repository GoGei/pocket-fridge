from django.conf.urls import include, url
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from django.conf import settings

from Api.routers.router_v1 import router_v1

api_urlpatterns = [
    url(r'^v1/', include((router_v1.urls, 'Api'), namespace='api')),
]
api_url = '%s://api%s' % (settings.SITE_SCHEME, settings.PARENT_HOST)

if settings.HOST_PORT:
    api_url = '%s://api%s:%s' % (settings.SITE_SCHEME, settings.PARENT_HOST, settings.HOST_PORT)

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
    ),
    url=api_url,
    patterns=api_urlpatterns,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    url(r'^swagger(?P<format>\.json|\.yaml)/v1/$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json-v1'),
    url(r'^swagger/v1/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v1'),
    url(r'^redoc/v1/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
