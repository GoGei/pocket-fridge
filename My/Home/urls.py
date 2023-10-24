from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'logout/$', views.logout_view, name='logout'),

    url(r'notifications/$', views.notifications, name='notifications'),
    url(r'notifications/clear-all/$', views.notifications_clear_all, name='notifications-clear-all'),
    path(r'notifications-remove/<str:notification_id>/', views.notifications_remove, name='notifications-remove'),
]
