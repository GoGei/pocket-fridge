from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.invoice_list, name='manager-stripe-invoice-list'),
    url(r'sync/$', views.invoice_sync, name='manager-stripe-invoice-sync'),
    path(r'<uuid:invoice_id>/', views.invoice_view, name='manager-stripe-invoice-view'),
]
