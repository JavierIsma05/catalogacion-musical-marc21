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
from catalogacion.views.borradores import (
    guardar_borrador_ajax,
    obtener_borrador_ajax,
    verificar_borrador_ajax,
    eliminar_borrador_ajax,
    listar_borradores_ajax,
    autoguardar_borrador_ajax,
)

app_name = 'catalogacion'

urlpatterns = [
    # Página principal
    path('', IndexView.as_view(), name='index'),
    
    # Obras
    path('obras/', include([
        path('', ListaObrasView.as_view(), name='lista_obras'),
        path('seleccionar-tipo/', SeleccionarTipoObraView.as_view(), name='seleccionar_tipo'),
        path('crear/<str:tipo>/', CrearObraView.as_view(), name='crear_obra'),
        path('<int:pk>/', DetalleObraView.as_view(), name='detalle_obra'),
        path('<int:pk>/editar/', EditarObraView.as_view(), name='editar_obra'),
        path('<int:pk>/eliminar/', EliminarObraView.as_view(), name='eliminar_obra'),
    ])),
    
    # API de Borradores (AJAX)
    path('api/borradores/', include([
        path('guardar/', guardar_borrador_ajax, name='api_guardar_borrador'),
        path('autoguardar/', autoguardar_borrador_ajax, name='api_autoguardar_borrador'),
        path('verificar/', verificar_borrador_ajax, name='api_verificar_borrador'),
        path('listar/', listar_borradores_ajax, name='api_listar_borradores'),
        path('<int:borrador_id>/', obtener_borrador_ajax, name='api_obtener_borrador'),
        path('<int:borrador_id>/eliminar/', eliminar_borrador_ajax, name='api_eliminar_borrador'),
    ])),
]
