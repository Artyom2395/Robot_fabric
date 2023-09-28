from django.urls import path
from . import views

urlpatterns = [
    path('create_robot/', views.create_robot),
    path('list/', views.list_robots, name='list_robots'),
    path('download-summary/', views.download_summary, name='download_summary'),
]
