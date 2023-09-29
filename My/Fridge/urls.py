from django.urls import path

from . import views

urlpatterns = [
    path(r'add/', views.fridge_add, name='fridge-add'),
    path(r'<uuid:fridge_id>/', views.fridge_view, name='fridge-view'),
    path(r'<uuid:fridge_id>/product/<uuid:product_id>/', views.product_view, name='product-view'),
    path(r'<uuid:fridge_id>/product/<uuid:product_id>/edit/', views.product_edit, name='product-edit'),
    path(r'<uuid:fridge_id>/product/<uuid:product_id>/delete/', views.product_delete, name='product-delete'),
]
