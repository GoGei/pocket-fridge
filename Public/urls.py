from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('urls')),
    url(r'^', include('Public.Home.urls')),
]
