"""
Vistas Bloque 2XX - Títulos y Publicación
=========================================

Gestión de campos MARC21 del bloque 2XX (Títulos, edición y publicación).

Campos incluidos:
- 245: Mención de título (campo principal en ObraGeneral)
- 246: Título alternativo
- 250: Mención de edición
- 264: Producción, publicación, distribución, fabricación y copyright

Todos estos campos son repetibles y algunos tienen subcampos repetibles.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
)

from ..forms import (
    TituloAlternativoFormSet,
    EdicionFormSet,
    ProduccionPublicacionFormSet,
)


def gestionar_titulos_alternativos(request, obra_id):
    """
    Gestionar Títulos Alternativos (246)
    
    Campo 246 - Título alternativo (Repetible)
    Permite registrar variantes del título de la obra.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = TituloAlternativoFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Títulos alternativos guardados correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar títulos alternativos: {str(e)}')
    else:
        formset = TituloAlternativoFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/2xx/titulos_alternativos.html', contexto)


def gestionar_ediciones(request, obra_id):
    """
    Gestionar Ediciones (250)
    
    Campo 250 - Mención de edición (Repetible)
    Registra información sobre la edición de la obra.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = EdicionFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Ediciones guardadas correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar ediciones: {str(e)}')
    else:
        formset = EdicionFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/2xx/ediciones.html', contexto)


def gestionar_produccion_publicacion(request, obra_id):
    """
    Gestionar Producción/Publicación (264)
    
    Campo 264 - Producción, publicación, distribución, fabricación y copyright (Repetible)
    
    Incluye:
    - Lugar de publicación
    - Editorial/Productor
    - Fecha de publicación
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = ProduccionPublicacionFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Datos de producción/publicación guardados correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar producción/publicación: {str(e)}')
    else:
        formset = ProduccionPublicacionFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/2xx/produccion_publicacion.html', contexto)


def listar_campos_2xx(request, obra_id):
    """
    Vista resumen de todos los campos 2XX de una obra
    
    Muestra información de títulos, edición y publicación.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render con todos los campos 2XX
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    contexto = {
        'obra': obra,
        'titulo_principal': obra.titulo_principal,
        'subtitulo': obra.subtitulo,
        'mencion_responsabilidad': obra.mencion_responsabilidad,
        'titulos_alternativos': obra.titulos_alternativos.all(),
        'ediciones': obra.ediciones.all(),
        'producciones_publicaciones': obra.producciones_publicaciones.all(),
    }
    return render(request, 'catalogacion/2xx/lista_campos_2xx.html', contexto)
