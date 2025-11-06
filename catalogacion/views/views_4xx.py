"""
Vistas Bloque 4XX - Series
===========================
Gestión de campos MARC21 del bloque 4XX (Mención de serie).

Campos incluidos:
- 490: Mención de serie

Subcampos relacionados:
  - $a Título de serie (R)
  - $v Volumen/número de serie (R)
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


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_mencion_serie_490(request, obra):
    """
    Procesar Mención de Serie (490) con subcampos anidados
    Estructura: mencion_serie_<idx>_relacion
              titulo_serie_490_<idx_padre>_<idx>_titulo
              volumen_serie_490_<idx_padre>_<idx>_volumen
    """
    indice = 0
    while True:
        relacion = request.POST.get(f'mencion_serie_{indice}_relacion', '').strip()
        
        # Verificar si hay títulos o volúmenes
        tiene_datos = bool(relacion)
        
        if not tiene_datos:
            # Verificar títulos
            tit_idx = 0
            while True:
                val = request.POST.get(f'titulo_serie_490_{indice}_{tit_idx}_titulo', '').strip()
                if val:
                    tiene_datos = True
                    break
                tit_idx += 1
                if tit_idx > 20:
                    break
        
        if not tiene_datos:
            # Verificar volúmenes
            vol_idx = 0
            while True:
                val = request.POST.get(f'volumen_serie_490_{indice}_{vol_idx}_volumen', '').strip()
                if val:
                    tiene_datos = True
                    break
                vol_idx += 1
                if vol_idx > 20:
                    break
        
        if not tiene_datos:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear mención de serie
        mencion = MencionSerie490.objects.create(
            obra=obra,
            relacion=relacion or '0'
        )
        
        # Procesar títulos de serie ($a)
        sub_idx = 0
        while True:
            titulo_texto = request.POST.get(f'titulo_serie_490_{indice}_{sub_idx}_titulo', '').strip()
            if not titulo_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            TituloSerie490.objects.create(
                mencion_serie=mencion,
                titulo_serie=titulo_texto
            )
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        # Procesar volúmenes ($v)
        sub_idx = 0
        while True:
            volumen_texto = request.POST.get(f'volumen_serie_490_{indice}_{sub_idx}_volumen', '').strip()
            if not volumen_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            VolumenSerie490.objects.create(
                mencion_serie=mencion,
                volumen=volumen_texto
            )
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        indice += 1
        if indice > 50:
            break


# ================================================
# VISTAS DE GESTIÓN (Para edición posterior)
# ================================================

def gestionar_mencion_serie_490(request, obra_id):
    """
    Gestionar Mención de Serie (490)
    Campo 490 - Mención de serie (Repetible)
    
    Subcampos repetibles:
      - $a Título de serie (R)
      - $v Volumen/número (R)
    
    Patrón de campos repetibles anidados.
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                procesar_mencion_serie_490(request, obra)
                messages.success(request, '✅ Mención de serie guardada correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar mención de serie: {str(e)}')
    
    # Preparar datos para el template
    series_data = []
    for serie in obra.menciones_serie.all():
        series_data.append({
            'id': serie.id,
            'relacion': serie.get_relacion_display(),
            'titulos': serie.titulos.all().order_by('id'),
            'volumenes': serie.volumenes.all().order_by('id'),
            'marc_format': serie.get_marc_format()
        })
    
    contexto = {
        'obra': obra,
        'menciones_serie': series_data,
    }
    
    return render(request, 'catalogacion/4xx/mencion_serie_490.html', contexto)


def listar_campos_4xx(request, obra_id):
    """
    Vista resumen de todos los campos 4XX de una obra
    Muestra información de series.
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # Preparar datos de menciones de serie con subcampos
    series_data = []
    for serie in obra.menciones_serie.all():
        series_data.append({
            'id': serie.id,
            'relacion': serie.get_relacion_display(),
            'titulos': serie.titulos.all(),
            'volumenes': serie.volumenes.all(),
            'marc_format': serie.get_marc_format()
        })
    
    contexto = {
        'obra': obra,
        'series': series_data,
    }
    
    return render(request, 'catalogacion/4xx/lista_campos_4xx.html', contexto)
