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
from catalogacion.views.utils import (
    autocompletar_persona,
    autocompletar_entidad,
    autocompletar_titulo_uniforme,
    autocompletar_materia,
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
    
    # APIs de autocompletado
    path('api/', include([
        path('autocompletar/persona/', autocompletar_persona, name='autocompletar_persona'),
        path('autocompletar/entidad/', autocompletar_entidad, name='autocompletar_entidad'),
        path('autocompletar/titulo-uniforme/', autocompletar_titulo_uniforme, name='autocompletar_titulo'),
        path('autocompletar/materia/', autocompletar_materia, name='autocompletar_materia'),
    ])),
    
    # Autoridades (sub-app)
    path('autoridades/', include(('catalogacion.urls_autoridades', 'autoridades'))),
]
