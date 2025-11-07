from django.urls import path
from .views import (
    # Vistas base
    index,
    plantillas,
    crear_obra,
    listar_obras,
    coleccion_manuscrita,
    obra_individual_manuscrita,
    coleccion_impresa,
    obra_individual_impresa,
    # Autoridades
    get_autoridades_json,
)
from .views import views_base as vb

urlpatterns = [
    # Rutas base
    path('', index, name='index'),
    path('plantillas/', plantillas, name='plantillas'),
    path('crear_obra/', crear_obra, name='crear_obra'),
    path('obras/', listar_obras, name='listar_obras'),
    
    # Colecciones
    path('coleccion_manuscrita/', coleccion_manuscrita, name='coleccion_manuscrita'),
    path('obra_individual_manuscrita/', obra_individual_manuscrita, name='obra_individual_manuscrita'),
    path('coleccion_impresa/', coleccion_impresa, name='coleccion_impresa'),
    path('obra_individual_impresa/', obra_individual_impresa, name='obra_individual_impresa'),
    
    # API - Autoridades
    path('api/autoridades/', get_autoridades_json, name='get_autoridades_json'),

    # 👇 nuevas rutas
    path('obra/<int:obra_id>/ver/', vb.ver_obra, name='ver_obra'),
    path('obra/<int:obra_id>/editar/', vb.editar_obra, name='editar_obra'),
    path('obra/<int:obra_id>/eliminar/', vb.eliminar_obra, name='eliminar_obra'),
    
]
