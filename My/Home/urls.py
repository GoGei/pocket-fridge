from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'profile/export/$', views.profile_export, name='profile-export'),
    url(r'profile/import/$', views.profile_import, name='profile-import'),

    url(r'notifications/$', views.notifications, name='notifications'),
    path(r'notifications-remove/<str:notification_id>/', views.notifications_remove, name='notifications-remove'),
]
