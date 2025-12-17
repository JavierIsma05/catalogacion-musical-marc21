"""
URLs principales de catalogación
"""
from django.urls import path, include
from catalogacion.views import (
    IndexView,
    SeleccionarTipoObraView,
    CrearObraView,
    EditarObraView,
    DetalleObraView,
    ListaObrasView,
    EliminarObraView,
)
from catalogacion.views import borradores as borradores_views

app_name = 'catalogacion'

urlpatterns = [
    # Redirección inteligente según rol
    path('', IndexView.as_view(), name='index'),
    
    # Obras (protegidas - requieren ser catalogador)
    path('obras/', include([
        path('', ListaObrasView.as_view(), name='lista_obras'),
        path('seleccionar-tipo/', SeleccionarTipoObraView.as_view(), name='seleccionar_tipo'),
        path('crear/<str:tipo>/', CrearObraView.as_view(), name='crear_obra'),
        path('<int:pk>/', DetalleObraView.as_view(), name='detalle_obra'),
        path('<int:pk>/editar/', EditarObraView.as_view(), name='editar_obra'),
        path('<int:pk>/eliminar/', EliminarObraView.as_view(), name='eliminar_obra'),
    ])),

    # Interfaz de borradores
    path('borradores/', borradores_views.ListaBorradoresView.as_view(), name='lista_borradores'),
    path('borradores/<int:pk>/recuperar/', borradores_views.recuperar_borrador_view, name='recuperar_borrador'),
    path('borradores/<int:pk>/descartar/', borradores_views.DescartarBorradorView.as_view(), name='descartar_borrador'),

    # API de borradores (usado por borrador-system.js)
    path('api/borradores/guardar/', borradores_views.guardar_borrador_ajax, name='api_guardar_borrador'),
    path('api/borradores/autoguardar/', borradores_views.autoguardar_borrador_ajax, name='api_autoguardar_borrador'),
    path('api/borradores/<int:borrador_id>/', borradores_views.obtener_borrador_ajax, name='api_obtener_borrador'),
    path('api/borradores/obra/<int:obra_id>/ultimo/', borradores_views.obtener_ultimo_borrador_obra_ajax, name='api_ultimo_borrador_obra'),
    path('api/borradores/<int:borrador_id>/eliminar/', borradores_views.eliminar_borrador_ajax, name='api_eliminar_borrador'),
    path('api/borradores/verificar/', borradores_views.verificar_borrador_ajax, name='api_verificar_borrador'),
    path('api/borradores/listar/', borradores_views.listar_borradores_ajax, name='api_listar_borradores'),
    path('api/borradores/limpiar-sesion/', borradores_views.limpiar_sesion_borrador_ajax, name='api_limpiar_sesion_borrador'),
]
