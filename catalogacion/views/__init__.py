"""
Exportación centralizada de views
"""

# Views base
from .base import IndexView

# Views de obras (refactorizadas)
from .obra_views import (
    SeleccionarTipoObraView,
    CrearObraView,
    EditarObraView,
    DetalleObraView,
    ListaObrasView,
    EliminarObraView,
    PapeleraObrasView,
    RestaurarObraView,
    PurgarObraView,
    PurgarTodoView,
    PublicarObraView,
    DespublicarObraView,
)

# Views de autoridades
from .autoridades import (
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
)

__all__ = [
    # Base
    'IndexView',
    
    # Obras
    'SeleccionarTipoObraView',
    'CrearObraView',
    'EditarObraView',
    'DetalleObraView',
    'ListaObrasView',
    'EliminarObraView',
    'PapeleraObrasView',
    'RestaurarObraView',
    'PurgarObraView',
    'PurgarTodoView',
    'PublicarObraView',
    'DespublicarObraView',
    
    # Autoridades - Personas
    'ListaPersonasView',
    'CrearPersonaView',
    'EditarPersonaView',
    'VerPersonaView',
    'EliminarPersonaView',
    
    # Autoridades - Entidades
    'ListaEntidadesView',
    'CrearEntidadView',
    'EditarEntidadView',
    'VerEntidadView',
    'EliminarEntidadView',
]
