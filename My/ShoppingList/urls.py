from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.shopping_list_view, name='shopping-list'),
    path(r'add/', views.shopping_list_add_product, name='shopping-list-add-product'),
    path(r'<uuid:product_id>/edit/', views.shopping_list_edit_product, name='shopping-list-edit-product'),
    path(r'<uuid:product_id>/add-product-to-shopping-list/', views.add_product_to_shopping_list,
         name='add-product-to-shopping-list'),
    path(r'<uuid:product_id>/check/', views.shopping_list_check_product, name='shopping-list-check-product'),
    path(r'<uuid:product_id>/uncheck/', views.shopping_list_uncheck_product, name='shopping-list-uncheck-product'),
    path(r'<uuid:product_id>/delete/', views.shopping_list_delete_product, name='shopping-list-delete-product'),
]
