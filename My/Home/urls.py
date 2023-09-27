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

    path(r'shopping-list/', views.shopping_list, name='shopping-list'),
]
