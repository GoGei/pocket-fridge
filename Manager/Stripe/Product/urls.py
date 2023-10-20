from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.product_list, name='manager-stripe-product-list'),
    url(r'sync/$', views.product_sync, name='manager-stripe-product-sync'),
    path(r'<uuid:product_id>/', views.product_view, name='manager-stripe-product-view'),
    path(r'<uuid:product_id>/archive/', views.product_archive, name='manager-stripe-product-archive'),
    path(r'<uuid:product_id>/set-as-default/', views.product_set_as_default,
         name='manager-stripe-product-set-as-default'),
]
