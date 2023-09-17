from django.conf import settings
from django.conf.urls import include, url

from .routers import router_v1, documentation

app_name = 'api'

urlpatterns = [
    url(r'^', include('urls')),
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/', include((router_v1.router_v1.urls, 'api'), namespace='api-v1')),
]

if settings.API_DOCUMENTATION:
    urlpatterns += documentation.urlpatterns
