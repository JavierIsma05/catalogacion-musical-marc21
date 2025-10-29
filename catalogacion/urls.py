from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plantillas/', views.plantillas, name='plantillas'),
    path('crear_obra/', views.crear_obra, name='crear_obra'),
]
