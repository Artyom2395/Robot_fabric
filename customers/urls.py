from django.urls import path
from . import views

urlpatterns = [
    path('register-director/', views.register_director, name='register_director'),
    path('login-director/', views.login_director, name='login_director'),
    path('logout-director/', views.logout_director, name='logout_director'),
]