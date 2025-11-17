"""
URLs para gestión de autoridades
"""
from django.urls import path
from catalogacion.views.autoridades import (
    # Personas
    ListaPersonasView,
    CrearPersonaView,
    EditarPersonaView,
    VerPersonaView,
    EliminarPersonaView,
    # Entidades
    ListaEntidadesView,
    CrearEntidadView,
    EditarEntidadView,
    VerEntidadView,
    EliminarEntidadView,
    AutocompletarPersonaView,
    AutocompletarEntidadView,
    AutocompletarTituloUniformeView,
)
from catalogacion.views.utils import autocompletar_forma_musical

urlpatterns = [
    # Personas
    path('personas/', ListaPersonasView.as_view(), name='lista_personas'),
    path('personas/crear/', CrearPersonaView.as_view(), name='crear_persona'),
    path('personas/<int:pk>/', VerPersonaView.as_view(), name='ver_persona'),
    path('personas/<int:pk>/editar/', EditarPersonaView.as_view(), name='editar_persona'),
    path('personas/<int:pk>/eliminar/', EliminarPersonaView.as_view(), name='eliminar_persona'),
    
    # Entidades
    path('entidades/', ListaEntidadesView.as_view(), name='lista_entidades'),
    path('entidades/crear/', CrearEntidadView.as_view(), name='crear_entidad'),
    path('entidades/<int:pk>/', VerEntidadView.as_view(), name='ver_entidad'),
    path('entidades/<int:pk>/editar/', EditarEntidadView.as_view(), name='editar_entidad'),
    path('entidades/<int:pk>/eliminar/', EliminarEntidadView.as_view(), name='eliminar_entidad'),
    
    # APIs de autocomplete
    path(
        'api/autocompletar/persona/',
        AutocompletarPersonaView.as_view(),
        name='autocompletar_persona'
    ),
    path(
        'api/autocompletar/entidad/',
        AutocompletarEntidadView.as_view(),
        name='autocompletar_entidad'
    ),
    path(
        'api/autocompletar/titulo/',
        AutocompletarTituloUniformeView.as_view(),
        name='autocompletar_titulo'
    ),
    path(
        'api/autocompletar/forma-musical/',
        autocompletar_forma_musical,
        name='autocompletar_forma_musical'
    ),
]
