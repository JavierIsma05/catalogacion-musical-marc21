"""
Vistas Bloque 0XX - Campos de Control
=====================================

Gestión de campos MARC21 del bloque 0XX (Campos de control e identificadores).

Campos incluidos:
- 020: ISBN (International Standard Book Number)
- 024: ISMN (International Standard Music Number)
- 028: Número de editor
- 031: Íncipit musical
- 041: Código de lengua
- 044: Código de país de entidad publicadora

Patrón de implementación:
Cada vista maneja campos repetibles con posibles subcampos repetibles anidados,
siguiendo el patrón establecido en views_pruebas.py (campo 300).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    ISBN,
    ISMN,
    NumeroEditor,
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
)

# ============================================================
# FUNCIONES DE PROCESAMIENTO MASIVO - GUARDADO DE OBRA
# ============================================================

def procesar_isbn(request, obra):
    """
    Procesa múltiples ISBN del formulario
    
    Formato de campos: isbn_a_0, isbn_a_1, isbn_a_2, ...
                       isbn_q_0, isbn_q_1, isbn_q_2, ...
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral donde se agregarán los ISBN
    """
    index = 0
    while True:
        isbn_value = request.POST.get(f'isbn_a_{index}')
        if not isbn_value:
            break
        
        if isbn_value.strip():
            ISBN.objects.create(
                obra=obra,
                isbn=isbn_value.strip()
            )
        index += 1


def procesar_ismn(request, obra):
    """
    Procesa múltiples ISMN del formulario
    
    Formato: ismn_a_0, ismn_a_1, ...
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral donde se agregarán los ISMN
    """
    index = 0
    while True:
        ismn_value = request.POST.get(f'ismn_a_{index}')
        if not ismn_value:
            break
        
        if ismn_value.strip():
            ISMN.objects.create(
                obra=obra,
                ismn=ismn_value.strip()
            )
        index += 1


def procesar_numero_editor(request, obra):
    """
    Procesa múltiples Números de Editor
    
    Formato: numero_editor_a_0, numero_editor_tipo_0, numero_editor_control_0
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    index = 0
    while True:
        numero = request.POST.get(f'numero_editor_a_{index}')
        if not numero:
            break
        
        if numero.strip():
            tipo = request.POST.get(f'numero_editor_tipo_{index}', '2')
            control = request.POST.get(f'numero_editor_control_{index}', '0')
            
            NumeroEditor.objects.create(
                obra=obra,
                numero_editor=numero.strip(),
                tipo_numero=tipo,
                control_nota=control
            )
        index += 1


def procesar_incipit(request, obra):
    """
    Procesa múltiples Incipits Musicales con URLs anidadas
    
    Formato: incipit_a_0, incipit_b_0, incipit_c_0, incipit_d_0, incipit_m_0, incipit_p_0
             incipit_u_0_0, incipit_u_0_1, ... (URLs para incipit 0)
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    index = 0
    while True:
        num_obra = request.POST.get(f'incipit_a_{index}')
        if not num_obra:
            break
        
        num_movimiento = request.POST.get(f'incipit_b_{index}', '1')
        num_pasaje = request.POST.get(f'incipit_c_{index}', '1')
        titulo = request.POST.get(f'incipit_d_{index}', '')
        instrumento = request.POST.get(f'incipit_m_{index}', '')
        notacion = request.POST.get(f'incipit_p_{index}', '')
        
        incipit = IncipitMusical.objects.create(
            obra=obra,
            numero_obra=num_obra,
            numero_movimiento=num_movimiento,
            numero_pasaje=num_pasaje,
            titulo_encabezamiento=titulo if titulo else None,
            voz_instrumento=instrumento if instrumento else None,
            notacion_musical=notacion if notacion else None
        )
        
        # Procesar URLs para este incipit
        url_index = 0
        while True:
            url = request.POST.get(f'incipit_u_{index}_{url_index}')
            if not url:
                break
            
            if url.strip():
                IncipitURL.objects.create(
                    incipit=incipit,
                    url=url.strip()
                )
            url_index += 1
        
        index += 1


def procesar_codigo_lengua(request, obra):
    """
    Procesa múltiples Códigos de Lengua con idiomas anidados
    
    Formato: codigo_lengua_ind1_0, codigo_lengua_ind2_0
             codigo_lengua_a_0_0, codigo_lengua_a_0_1, ... (idiomas para lengua 0)
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    index = 0
    while True:
        ind1 = request.POST.get(f'codigo_lengua_ind1_{index}')
        if ind1 is None:
            break
        
        ind2 = request.POST.get(f'codigo_lengua_ind2_{index}', '#')
        
        codigo_lengua = CodigoLengua.objects.create(
            obra=obra,
            indicacion_traduccion=ind1,
            fuente_codigo=ind2
        )
        
        # Procesar idiomas para este código de lengua
        idioma_index = 0
        while True:
            idioma = request.POST.get(f'codigo_lengua_a_{index}_{idioma_index}')
            if not idioma:
                break
            
            if idioma.strip():
                IdiomaObra.objects.create(
                    codigo_lengua=codigo_lengua,
                    codigo_idioma=idioma.strip()
                )
            idioma_index += 1
        
        index += 1


def procesar_codigo_pais(request, obra):
    """
    Procesa múltiples Códigos de País
    
    Formato: codigo_pais_a_0, codigo_pais_a_1, ...
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    index = 0
    while True:
        codigo = request.POST.get(f'codigo_pais_a_{index}')
        if not codigo:
            break
        
        if codigo.strip():
            CodigoPaisEntidad.objects.create(
                obra=obra,
                codigo_pais=codigo.strip()
            )
        index += 1
