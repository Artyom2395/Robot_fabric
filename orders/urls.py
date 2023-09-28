from django.urls import path
from . import views

urlpatterns = [
    path('make_order/', views.make_order, name='make-order'),
]