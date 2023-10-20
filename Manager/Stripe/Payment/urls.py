from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.payment_list, name='manager-stripe-payment-list'),
    url(r'sync/$', views.payment_sync, name='manager-stripe-payment-sync'),
    url(r'sync-all/$', views.payment_sync_all, name='manager-stripe-payment-sync-all'),
    path(r'<uuid:payment_id>/', views.payment_view, name='manager-stripe-payment-view'),
]
