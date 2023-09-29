from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'profile/$', views.profile, name='profile'),

    path(r'fridge/add/', views.fridge_add, name='fridge-add'),
    path(r'fridge/<uuid:fridge_id>/', views.fridge_view, name='fridge-view'),
    path(r'fridge/<uuid:fridge_id>/product/<uuid:product_id>/', views.product_view, name='product-view'),
    path(r'fridge/<uuid:fridge_id>/product/<uuid:product_id>/edit/', views.product_edit, name='product-edit'),
    path(r'fridge/<uuid:fridge_id>/product/<uuid:product_id>/delete/', views.product_delete, name='product-delete'),

    path(r'shopping-list/', views.shopping_list_view, name='shopping-list'),
    path(r'shopping-list/add/', views.shopping_list_add_product, name='shopping-list-add-product'),
    path(r'shopping-list/<uuid:product_id>/edit/', views.shopping_list_edit_product, name='shopping-list-edit-product'),
    path(r'shopping-list/<uuid:product_id>/check/', views.shopping_list_check_product,
         name='shopping-list-check-product'),
    path(r'shopping-list/<uuid:product_id>/uncheck/', views.shopping_list_uncheck_product,
         name='shopping-list-uncheck-product'),
    path(r'shopping-list/<uuid:product_id>/delete/', views.shopping_list_delete_product,
         name='shopping-list-delete-product'),

    url(r'test/$', views.test_view, name='home-test-me'),
]
