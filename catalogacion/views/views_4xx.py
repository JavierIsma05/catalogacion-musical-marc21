"""
Vistas Bloque 4XX - Series
===========================

Gestión de campos MARC21 del bloque 4XX (Mención de serie).

Campos incluidos:
- 490: Mención de serie

Subcampos relacionados:
- Mención de serie
- Título de serie
- Volumen/número de serie
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
)

# from ..forms import (
#     # TODO: Crear formsets para 490
# )


def gestionar_mencion_serie_490(request, obra_id):
    """
    Gestionar Mención de Serie (490)
    
    Campo 490 - Mención de serie (Repetible)
    Subcampos repetibles:
    - Título de serie (R)
    - Volumen/número (R)
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # TODO: Implementar lógica similar a gestionar_descripcion_fisica (views_3xx.py)
    # para manejar campos repetibles anidados del campo 490
    
    contexto = {
        'obra': obra,
        'menciones_serie': obra.menciones_serie.all(),
    }
    return render(request, 'catalogacion/4xx/mencion_serie_490.html', contexto)


def listar_campos_4xx(request, obra_id):
    """
    Vista resumen de todos los campos 4XX de una obra
    
    Muestra información de series.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render con todos los campos 4XX
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # Preparar datos de menciones de serie con subcampos
    series_data = []
    for serie in obra.menciones_serie.all():
        series_data.append({
            'id': serie.id,
            'titulos': serie.titulos_serie.all() if hasattr(serie, 'titulos_serie') else [],
            'volumenes': serie.volumenes_serie.all() if hasattr(serie, 'volumenes_serie') else [],
        })
    
    contexto = {
        'obra': obra,
        'series': series_data,
    }
    return render(request, 'catalogacion/4xx/lista_campos_4xx.html', contexto)
