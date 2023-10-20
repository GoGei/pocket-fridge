from django.urls import path
from . import views

urlpatterns = [
    path(r'<uuid:price_id>/', views.price_view, name='manager-stripe-product-price-view'),
    path(r'<uuid:product_id>/sync/', views.price_sync, name='manager-stripe-product-price-sync'),
    path(r'<uuid:price_id>/archive/', views.price_archive, name='manager-stripe-product-price-archive'),
    path(r'<uuid:price_id>/set-as-default/', views.price_set_as_default,
         name='manager-stripe-product-price-set-as-default'),
]
