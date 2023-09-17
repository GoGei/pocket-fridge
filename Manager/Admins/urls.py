from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.admins_list, name='manager-admins-list'),
    url(r'add/$', views.admins_add, name='manager-admins-add'),
    url(r'reset-password/$', views.admins_reset_password, name='manager-admins-reset-password'),
    path(r'<int:admin_id>/', views.admins_view, name='manager-admins-view'),
    path(r'<int:admin_id>/edit/', views.admins_edit, name='manager-admins-edit'),
    path(r'<int:admin_id>/set-password/', views.admins_set_password, name='manager-admins-set-password'),
]
