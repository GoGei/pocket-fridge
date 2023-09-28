from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.home_index, name='home-index'),
    url(r'register/$', views.register, name='register'),
    url(r'register-success/$', views.register_success, name='register-success'),
    path('register-activate/<str:key>/', views.register_activate, name='register-activate'),

    url(r'forgot-password/$', views.forgot_password, name='forgot-password'),
    url(r'forgot-password-success/$', views.forgot_password_success, name='forgot-password-success'),
    path('forgot-password-reset/<str:key>/', views.forgot_password_reset, name='forgot-password-reset'),

    url(r'licences/$', views.licences, name='licences'),

    url(r'login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'go-to-fridge/$', views.go_to_fridge_view, name='go-to-fridge'),
]
