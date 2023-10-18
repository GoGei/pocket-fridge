from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.payment_list, name='manager-stripe-payment-list'),
    path(r'<uuid:payment_id>/', views.payment_view, name='manager-stripe-payment-view'),
]
