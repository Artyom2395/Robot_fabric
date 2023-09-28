from django.urls import path
from . import views

urlpatterns = [
    path('create_robot/', views.create_robot),
    path('list/', views.list_robots, name='list_robots'),
]
