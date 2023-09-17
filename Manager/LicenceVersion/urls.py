from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.licence_version_list, name='manager-licence-version-list'),
    url(r'add/$', views.licence_version_add, name='manager-licence-version-add'),
    path(r'<int:licence_version_id>/', views.licence_version_view, name='manager-licence-version-view'),
    path(r'<int:licence_version_id>/edit/', views.licence_version_edit, name='manager-licence-version-edit'),
    path(r'<int:licence_version_id>/archive/', views.licence_version_archive, name='manager-licence-version-archive'),
    path(r'<int:licence_version_id>/restore/', views.licence_version_restore, name='manager-licence-version-restore'),
    path(r'<int:licence_version_id>/set-default/', views.licence_version_set_default,
         name='manager-licence-version-set-default'),
]
