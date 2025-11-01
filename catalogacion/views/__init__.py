"""
Views Package - Sistema de Catalogación MARC21 Musical
========================================================

Organización de vistas por bloques MARC bibliográficos.

Estructura:
- views_base.py: Vistas generales de navegación
- views_autoridades.py: Endpoints JSON para autocompletado
- views_0xx.py: Campos de control (ISBN, ISMN, Íncipit, etc.)
- views_1xx.py: Puntos de acceso (Compositor, Títulos uniformes)
- views_2xx.py: Títulos y publicación
- views_3xx.py: Descripción física
- views_4xx.py: Series
- views_pruebas.py: Vistas de testing/desarrollo
"""

# Importar vistas base
from .views_base import (
    index,
    plantillas,
    crear_obra,
    coleccion_manuscrita,
    obra_individual_manuscrita,
    coleccion_impresa,
    obra_individual_impresa,
)

# Importar vistas de autoridades
from .views_autoridades import (
    get_autoridades_json,
)

# Importar vistas de pruebas
from .views_pruebas import (
    prueba_campo_300,
    limpiar_prueba_300,
)

# Exportar todas las vistas
__all__ = [
    # Vistas base
    'index',
    'plantillas',
    'crear_obra',
    'coleccion_manuscrita',
    'obra_individual_manuscrita',
    'coleccion_impresa',
    'obra_individual_impresa',
    
    # Autoridades
    'get_autoridades_json',
    
    # Pruebas
    'prueba_campo_300',
    'limpiar_prueba_300',
]
