from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'register/$', views.register, name='register'),
    url(r'register-success/$', views.register_success, name='register-success'),
    url(r'login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'forgot-password/$', views.forgot_password, name='forgot-password'),
    url(r'licences/$', views.licences, name='licences'),
]
