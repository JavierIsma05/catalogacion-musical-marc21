"""
Exportación centralizada de views
"""

# Views base
from .base import IndexView

# Views de obras
from .obras import (
    SeleccionarTipoObraView,
    CrearObraView,
    EditarObraView,
    DetalleObraView,
    ListaObrasView,
    EliminarObraView,
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
