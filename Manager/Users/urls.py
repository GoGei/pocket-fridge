from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.users_list, name='manager-users-list'),
    path(r'<int:user_id>/', views.users_view, name='manager-users-view'),
]
