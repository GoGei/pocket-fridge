from django.conf.urls import url, include
from Manager.Api.urls import urlpatterns as api_urls

urlpatterns = [
    url(r'', include('urls')),
    url(r'^', include('Manager.Login.urls')),
    url(r'^', include('Manager.Home.urls')),
    url(r'^users/', include('Manager.Users.urls')),
    url(r'^admins/', include('Manager.Admins.urls')),

    url(r'^api/', include((api_urls, 'manager-api-v1'), namespace='manager-api-v1')),
]
