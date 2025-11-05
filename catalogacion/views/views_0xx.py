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

from ..forms import (
    ISBNForm,
    ISMNFormSet,
    NumeroEditorForm,
    IncipitMusicalForm,
    IncipitURLFormSet,
    CodigoLenguaForm,
    IdiomaObraFormSet,
    CodigoPaisEntidadFormSet,
)


def crear_isbn(request, obra_id):
    """
    Gestionar ISBN (020) de una obra
    
    Campo 020 - ISBN (Repetible)
    Permite agregar múltiples ISBN a una obra musical.
    
    Args:
        obra_id: ID de la obra a la que se agregará el ISBN
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        form = ISBNForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    isbn = form.save(commit=False)
                    isbn.obra = obra
                    isbn.save()
                    messages.success(request, '✅ ISBN agregado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar ISBN: {str(e)}')
    else:
        form = ISBNForm()
    
    contexto = {
        'obra': obra,
        'form': form,
        'isbns_existentes': obra.isbns.all(),
    }
    return render(request, 'catalogacion/0xx/isbn_form.html', contexto)


def crear_ismn(request, obra_id):
    """
    Gestionar ISMN (024 $a) de una obra
    
    Campo 024 - ISMN (Repetible)
    Permite agregar múltiples ISMN a una obra musical.
    
    Args:
        obra_id: ID de la obra a la que se agregará el ISMN
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = ISMNFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ ISMN guardados correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar ISMN: {str(e)}')
    else:
        formset = ISMNFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/0xx/ismn_form.html', contexto)


def crear_numero_editor(request, obra_id):
    """
    Gestionar Número de Editor (028) de una obra
    
    Campo 028 - Número de editor (Repetible)
    Número asignado por el editor/distribuidor musical.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        form = NumeroEditorForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    numero = form.save(commit=False)
                    numero.obra = obra
                    numero.save()
                    messages.success(request, '✅ Número de editor agregado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar número de editor: {str(e)}')
    else:
        form = NumeroEditorForm()
    
    contexto = {
        'obra': obra,
        'form': form,
        'numeros_existentes': obra.numeros_editor.all(),
    }
    return render(request, 'catalogacion/0xx/numero_editor_form.html', contexto)


def crear_incipit_musical(request, obra_id):
    """
    Gestionar Íncipit Musical (031) con URLs anidadas
    
    Campo 031 - Íncipit musical (Repetible)
    Subcampos repetibles: URL de íncipit
    
    Este campo sigue el patrón de campos repetibles anidados similar al campo 300.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        form = IncipitMusicalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    incipit = form.save(commit=False)
                    incipit.obra = obra
                    incipit.save()
                    
                    # Procesar URLs asociadas
                    formset_urls = IncipitURLFormSet(request.POST, instance=incipit)
                    if formset_urls.is_valid():
                        formset_urls.save()
                    
                    messages.success(request, '✅ Íncipit musical agregado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar íncipit: {str(e)}')
    else:
        form = IncipitMusicalForm()
        formset_urls = IncipitURLFormSet()
    
    contexto = {
        'obra': obra,
        'form': form,
        'formset_urls': formset_urls,
        'incipits_existentes': obra.incipits_musicales.all(),
    }
    return render(request, 'catalogacion/0xx/incipit_form.html', contexto)


def crear_codigo_lengua(request, obra_id):
    """
    Gestionar Código de Lengua (041) con idiomas anidados
    
    Campo 041 - Código de lengua (Repetible)
    Subcampos repetibles: Idiomas de la obra
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        form = CodigoLenguaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    codigo_lengua = form.save(commit=False)
                    codigo_lengua.obra = obra
                    codigo_lengua.save()
                    
                    # Procesar idiomas asociados
                    formset_idiomas = IdiomaObraFormSet(request.POST, instance=codigo_lengua)
                    if formset_idiomas.is_valid():
                        formset_idiomas.save()
                    
                    messages.success(request, '✅ Código de lengua agregado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar código de lengua: {str(e)}')
    else:
        form = CodigoLenguaForm()
        formset_idiomas = IdiomaObraFormSet()
    
    contexto = {
        'obra': obra,
        'form': form,
        'formset_idiomas': formset_idiomas,
        'codigos_existentes': obra.codigos_lengua.all(),
    }
    return render(request, 'catalogacion/0xx/codigo_lengua_form.html', contexto)


def listar_campos_0xx(request, obra_id):
    """
    Vista resumen de todos los campos 0XX de una obra
    
    Muestra en una sola página todos los campos de control e identificadores
    registrados para la obra.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render con todos los campos 0XX
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    contexto = {
        'obra': obra,
        'isbns': obra.isbns.all(),
        'ismns': obra.ismns.all(),
        'numeros_editor': obra.numeros_editor.all(),
        'incipits': obra.incipits_musicales.all(),
        'codigos_lengua': obra.codigos_lengua.all(),
        'codigos_pais': obra.codigos_pais_entidad.all(),
    }
    return render(request, 'catalogacion/0xx/lista_campos_0xx.html', contexto)


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
    orden = 1
    while True:
        codigo = request.POST.get(f'codigo_pais_a_{index}')
        if not codigo:
            break
        
        if codigo.strip():
            CodigoPaisEntidad.objects.create(
                obra=obra,
                codigo_pais=codigo.strip(),
                orden=orden
            )
            orden += 1
        index += 1
