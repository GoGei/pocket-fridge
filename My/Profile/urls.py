from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.profile, name='profile'),
    url(r'export/$', views.profile_export, name='profile-export'),
    url(r'import/$', views.profile_import, name='profile-import'),
    url(r'subscribe/$', views.profile_subscribe, name='profile-subscribe'),
    url(r'cancel-subscription/$', views.profile_cancel_subscription, name='profile-cancel-subscription'),
    url(r'add-payment-method/$', views.profile_add_payment_method, name='profile-add-payment-method'),
]
