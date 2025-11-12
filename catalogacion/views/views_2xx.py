"""
Vistas Bloque 2XX - Títulos y Publicación
=========================================

Gestión de campos MARC21 del bloque 2XX (Títulos, edición y publicación).

Campos incluidos:
- 245: Mención de título (campo principal en ObraGeneral)
- 246: Título alternativo
- 250: Mención de edición
- 264: Producción, publicación, distribución, fabricación y copyright

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

def procesar_titulo_alternativo(request, obra):
    """
    Procesar Títulos Alternativos (246) desde el formulario
    Campo repetible: titulo_alternativo_a_<indice>, titulo_alternativo_b_<indice>
    """
    from ..models.bloque_2xx import TituloAlternativo
    
    indice = 0
    while True:
        titulo = request.POST.get(f'titulo_alternativo_a_{indice}', '').strip()
        
        if not titulo:
            indice += 1
            if indice > 50:  # Límite de seguridad
                break
            continue
        
        resto_titulo = request.POST.get(f'titulo_alternativo_b_{indice}', '').strip()
        
        TituloAlternativo.objects.create(
            obra=obra,
            titulo=titulo,
            resto_titulo=resto_titulo
        )
        
        indice += 1
        if indice > 50:
            break

def procesar_edicion(request, obra):
    """
    Procesar Ediciones (250) desde el formulario
    Campo repetible: edicion_a_<indice>
    """
    from ..models.bloque_2xx import Edicion
    
    indice = 0
    while True:
        edicion_texto = request.POST.get(f'edicion_a_{indice}', '').strip()
        
        if not edicion_texto:
            indice += 1
            if indice > 50:
                break
            continue
        
        Edicion.objects.create(
            obra=obra,
            edicion=edicion_texto
        )
        
        indice += 1
        if indice > 50:
            break

def procesar_produccion_publicacion(request, obra):
    """
    Procesar Producción/Publicación (264) desde el formulario
    Campo repetible: produccion_publicacion_funcion_<indice>, produccion_publicacion_a_<indice>, etc.
    """
    from ..models.bloque_2xx import ProduccionPublicacion
    
    indice = 0
    while True:
        funcion = request.POST.get(f'produccion_publicacion_funcion_{indice}', '').strip()
        
        if not funcion:
            indice += 1
            if indice > 50:
                break
            continue
        
        lugar = request.POST.get(f'produccion_publicacion_a_{indice}', '').strip()
        nombre = request.POST.get(f'produccion_publicacion_b_{indice}', '').strip()
        fecha = request.POST.get(f'produccion_publicacion_c_{indice}', '').strip()
        
        ProduccionPublicacion.objects.create(
            obra=obra,
            funcion=funcion,
            lugar=lugar,
            nombre_entidad=nombre,
            fecha=fecha
        )
        
        indice += 1
        if indice > 50:
            break
