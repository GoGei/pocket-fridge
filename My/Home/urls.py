from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'test/$', views.test_view, name='home-test-me'),
]
