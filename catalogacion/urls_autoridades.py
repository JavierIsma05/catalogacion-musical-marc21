"""
URLs para gestión de autoridades
"""
from django.urls import path
from catalogacion.views import api_views
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
    # Formas musicales
    ListaFormasMusicalesView,
    CrearFormaMusicalView,
    EditarFormaMusicalView,
    EliminarFormaMusicalView,
    # Materias
    ListaMateriasView,
    CrearMateriaView,
    EditarMateriaView,
    EliminarMateriaView,
    # Títulos uniformes
    ListaTitulosUniformesView,
    CrearTituloUniformeView,
    EditarTituloUniformeView,
    EliminarTituloUniformeView,
    # Autocomplete APIs
    AutocompletarPersonaView,
    AutocompletarEntidadView,
    AutocompletarTituloUniformeView,
    AutocompletarMateriaView,
)
from catalogacion.views.utils import autocompletar_forma_musical

app_name = 'autoridades'

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

    # Formas musicales
    path('formas-musicales/', ListaFormasMusicalesView.as_view(), name='lista_formas_musicales'),
    path('formas-musicales/crear/', CrearFormaMusicalView.as_view(), name='crear_forma_musical'),
    path('formas-musicales/<int:pk>/editar/', EditarFormaMusicalView.as_view(), name='editar_forma_musical'),
    path('formas-musicales/<int:pk>/eliminar/', EliminarFormaMusicalView.as_view(), name='eliminar_forma_musical'),

    # Materias
    path('materias/', ListaMateriasView.as_view(), name='lista_materias'),
    path('materias/crear/', CrearMateriaView.as_view(), name='crear_materia'),
    path('materias/<int:pk>/editar/', EditarMateriaView.as_view(), name='editar_materia'),
    path('materias/<int:pk>/eliminar/', EliminarMateriaView.as_view(), name='eliminar_materia'),

    # Títulos uniformes
    path('titulos-uniformes/', ListaTitulosUniformesView.as_view(), name='lista_titulos_uniformes'),
    path('titulos-uniformes/crear/', CrearTituloUniformeView.as_view(), name='crear_titulo_uniforme'),
    path('titulos-uniformes/<int:pk>/editar/', EditarTituloUniformeView.as_view(), name='editar_titulo_uniforme'),
    path('titulos-uniformes/<int:pk>/eliminar/', EliminarTituloUniformeView.as_view(), name='eliminar_titulo_uniforme'),
    
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
    # AUTOCOMPLETE PARA MATERIAS 650
    path(
        'api/autocompletar/materia/',
        AutocompletarMateriaView.as_view(),
        name='autocompletar_materia'
    ),
    path('api/buscar-obras/', api_views.buscar_obras, name='buscar_obras'),
]
