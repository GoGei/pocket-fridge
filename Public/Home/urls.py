from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.login, name='login'),
    url(r'forgot-password/$', views.forgot_password, name='forgot-password'),
    url(r'licences/$', views.licences, name='licences'),
]
