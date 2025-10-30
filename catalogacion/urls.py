from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plantillas/', views.plantillas, name='plantillas'),
    path('crear_obra/', views.crear_obra, name='crear_obra'),
    # obra general
    path('obra_general/', views.obra_general, name='obra_general'),
    path('coleccion_manuscrita/', views.coleccion_manuscrita, name='coleccion_manuscrita'),
    path('obra_individual_manuscrita/', views.obra_individual_manuscrita, name='obra_individual_manuscrita'),
    path('coleccion_impresa/', views.coleccion_impresa, name='coleccion_impresa'),
    path('obra_individual_impresa/', views.obra_individual_impresa, name='obra_individual_impresa'),
]
