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
    Estructura HTML/JS:
        - mencion_serie_relacion_{idx}
        - titulo_serie_490_a_{idx_padre}_{idx}
        - volumen_serie_490_v_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        relacion = request.POST.get(f'mencion_serie_relacion_{indice}', '').strip()
        
        # Verificar si hay títulos o volúmenes
        tiene_datos = bool(relacion)
        
        if not tiene_datos:
            # Verificar títulos
            tit_idx = 0
            while True:
                val = request.POST.get(f'titulo_serie_490_a_{indice}_{tit_idx}', '').strip()
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
                val = request.POST.get(f'volumen_serie_490_v_{indice}_{vol_idx}', '').strip()
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
            titulo_texto = request.POST.get(f'titulo_serie_490_a_{indice}_{sub_idx}', '').strip()
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
            volumen_texto = request.POST.get(f'volumen_serie_490_v_{indice}_{sub_idx}', '').strip()
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
