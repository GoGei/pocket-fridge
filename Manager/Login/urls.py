from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/$', views.login_view, name='manager-login'),
    url(r'logout/$', views.logout_view, name='manager-logout'),
]
