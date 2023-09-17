from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.fridge_type_list, name='manager-fridge-type-list'),
    url(r'add/$', views.fridge_type_add, name='manager-fridge-type-add'),
    path(r'<int:fridge_type_id>/', views.fridge_type_view, name='manager-fridge-type-view'),
    path(r'<int:fridge_type_id>/edit/', views.fridge_type_edit, name='manager-fridge-type-edit'),
    path(r'<int:fridge_type_id>/archive/', views.fridge_type_archive, name='manager-fridge-type-archive'),
    path(r'<int:fridge_type_id>/restore/', views.fridge_type_restore, name='manager-fridge-type-restore'),

    url(r'view-fixture/$', views.fridge_type_view_fixture, name='manager-fridge-type-view-fixture'),
    url(r'load-fixture/$', views.fridge_type_load_fixture, name='manager-fridge-type-load-fixture'),
    url(r'export-to-fixture/$', views.fridge_type_export_to_fixture,
        name='manager-fridge-type-export-to-fixture'),
    url(r'load-default-fixture/$', views.fridge_type_load_default_fixture,
        name='manager-fridge-type-load-default-fixture'),
]
