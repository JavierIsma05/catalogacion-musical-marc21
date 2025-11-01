"""
Vistas Bloque 3XX - Descripción Física y Características
========================================================

Gestión de campos MARC21 del bloque 3XX (Descripción física y técnica).

Campos incluidos:
- 300: Descripción física
- 340: Medio físico
- 348: Características de música notada
- 382: Medio de interpretación
- 383: Designación numérica de obra musical
- 384: Tonalidad

Estos campos contienen subcampos repetibles anidados y siguen el patrón
establecido en views_pruebas.py para manejo de campos complejos.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    DescripcionFisica,
    Extension300,
    Dimension300,
    MedioFisico,
    Tecnica340,
    CaracteristicaMusicaNotada,
    Formato348,
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    Solista382,
    NumeroInterpretes382,
    DesignacionNumericaObra,
    NumeroObra383,
    Opus383,
)

from ..forms import (
    DescripcionFisicaFormSet,
    Extension300FormSet,
    Dimension300FormSet,
    MedioFisicoFormSet,
    Tecnica340FormSet,
)


def gestionar_descripcion_fisica(request, obra_id):
    """
    Gestionar Descripción Física (300) con subcampos repetibles anidados
    
    Campo 300 - Descripción física (Repetible)
    Estructura:
    - Campo 300 (R)
        - $a Extensión (R)
        - $b Otras características físicas (NR)
        - $c Dimensión (R)
        - $e Material acompañante (NR)
    
    Esta vista maneja campos repetibles con subcampos repetibles anidados,
    siguiendo el patrón establecido en views_pruebas.py.
    
    Args:
        obra_id: ID de la obra a gestionar
    
    Returns:
        Render del formulario o redirect después de guardar
    
    Ejemplo de uso:
        GET: Muestra formulario con campos 300 existentes
        POST: Procesa y guarda cambios en campos 300 y subcampos
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Contar cuántas descripciones físicas hay
                total_forms_key = 'descripcion_fisica_TOTAL_FORMS'
                total_descripciones = int(request.POST.get(total_forms_key, 0))
                
                for desc_idx in range(total_descripciones):
                    # Verificar si el formulario está marcado para eliminación
                    delete_key = f'descripcion_fisica_{desc_idx}_DELETE'
                    if request.POST.get(delete_key):
                        # Si tiene ID, eliminar de la base de datos
                        desc_id_key = f'descripcion_fisica_{desc_idx}_id'
                        desc_id = request.POST.get(desc_id_key)
                        if desc_id:
                            DescripcionFisica.objects.filter(pk=desc_id).delete()
                        continue
                    
                    # Obtener datos de la descripción física
                    otras_caract_key = f'descripcion_fisica_{desc_idx}_otras_caracteristicas_fisicas'
                    material_acomp_key = f'descripcion_fisica_{desc_idx}_material_acompanante'
                    desc_id_key = f'descripcion_fisica_{desc_idx}_id'
                    
                    otras_caract = request.POST.get(otras_caract_key, '').strip()
                    material_acomp = request.POST.get(material_acomp_key, '').strip()
                    desc_id = request.POST.get(desc_id_key)
                    
                    # Obtener o crear descripción física
                    if desc_id:
                        desc_fisica = DescripcionFisica.objects.get(pk=desc_id)
                        desc_fisica.otras_caracteristicas_fisicas = otras_caract
                        desc_fisica.material_acompanante = material_acomp
                        desc_fisica.save()
                    else:
                        desc_fisica = DescripcionFisica.objects.create(
                            obra=obra,
                            otras_caracteristicas_fisicas=otras_caract,
                            material_acompanante=material_acomp
                        )
                    
                    # Procesar extensiones ($a) para esta descripción
                    total_ext_key = f'extension_{desc_idx}_TOTAL_FORMS'
                    total_extensiones = int(request.POST.get(total_ext_key, 0))
                    
                    extensiones_procesadas = []
                    
                    for ext_idx in range(total_extensiones):
                        delete_ext_key = f'extension_{desc_idx}_{ext_idx}_DELETE'
                        if request.POST.get(delete_ext_key):
                            ext_id_key = f'extension_{desc_idx}_{ext_idx}_id'
                            ext_id = request.POST.get(ext_id_key)
                            if ext_id:
                                Extension300.objects.filter(pk=ext_id).delete()
                            continue
                        
                        ext_key = f'extension_{desc_idx}_{ext_idx}_extension'
                        ext_id_key = f'extension_{desc_idx}_{ext_idx}_id'
                        
                        extension_texto = request.POST.get(ext_key, '').strip()
                        ext_id = request.POST.get(ext_id_key)
                        
                        if extension_texto:
                            if ext_id:
                                ext_obj = Extension300.objects.get(pk=ext_id)
                                ext_obj.extension = extension_texto
                                ext_obj.save()
                                extensiones_procesadas.append(int(ext_id))
                            else:
                                ext_obj = Extension300.objects.create(
                                    descripcion_fisica=desc_fisica,
                                    extension=extension_texto
                                )
                                extensiones_procesadas.append(ext_obj.id)
                    
                    # Procesar dimensiones ($c) para esta descripción
                    total_dim_key = f'dimension_{desc_idx}_TOTAL_FORMS'
                    total_dimensiones = int(request.POST.get(total_dim_key, 0))
                    
                    dimensiones_procesadas = []
                    
                    for dim_idx in range(total_dimensiones):
                        delete_dim_key = f'dimension_{desc_idx}_{dim_idx}_DELETE'
                        if request.POST.get(delete_dim_key):
                            dim_id_key = f'dimension_{desc_idx}_{dim_idx}_id'
                            dim_id = request.POST.get(dim_id_key)
                            if dim_id:
                                Dimension300.objects.filter(pk=dim_id).delete()
                            continue
                        
                        dim_key = f'dimension_{desc_idx}_{dim_idx}_dimension'
                        dim_id_key = f'dimension_{desc_idx}_{dim_idx}_id'
                        
                        dimension_texto = request.POST.get(dim_key, '').strip()
                        dim_id = request.POST.get(dim_id_key)
                        
                        if dimension_texto:
                            if dim_id:
                                dim_obj = Dimension300.objects.get(pk=dim_id)
                                dim_obj.dimension = dimension_texto
                                dim_obj.save()
                                dimensiones_procesadas.append(int(dim_id))
                            else:
                                dim_obj = Dimension300.objects.create(
                                    descripcion_fisica=desc_fisica,
                                    dimension=dimension_texto
                                )
                                dimensiones_procesadas.append(dim_obj.id)
                
                messages.success(request, '✅ Descripción física guardada correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
                
        except Exception as e:
            messages.error(request, f'❌ Error al guardar descripción física: {str(e)}')
    
    # Preparar datos para el template
    descripciones = obra.descripciones_fisicas.all().order_by('id')
    
    # Preparar datos estructurados para el template
    descripciones_data = []
    for desc in descripciones:
        descripciones_data.append({
            'id': desc.id,
            'otras_caracteristicas': desc.otras_caracteristicas_fisicas,
            'material_acompanante': desc.material_acompanante,
            'extensiones': desc.extensiones.all().order_by('id'),
            'dimensiones': desc.dimensiones_set.all().order_by('id'),
            'marc_format': desc.get_marc_format()
        })
    
    contexto = {
        'obra': obra,
        'descripciones': descripciones_data,
        'total_descripciones': len(descripciones_data),
    }
    
    return render(request, 'catalogacion/3xx/descripcion_fisica.html', contexto)


def gestionar_medio_fisico(request, obra_id):
    """
    Gestionar Medio Físico (340) con técnicas anidadas
    
    Campo 340 - Medio físico (Repetible)
    Subcampos:
    - $d Técnica (R)
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = MedioFisicoFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Medio físico guardado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar medio físico: {str(e)}')
    else:
        formset = MedioFisicoFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/3xx/medio_fisico.html', contexto)


def gestionar_caracteristicas_musica_notada(request, obra_id):
    """
    Gestionar Características de Música Notada (348)
    
    Campo 348 - Características de música notada (Repetible)
    Subcampos:
    - $a Formato de la música notada (R)
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # TODO: Implementar lógica similar a gestionar_descripcion_fisica
    # para manejar campos repetibles anidados
    
    contexto = {
        'obra': obra,
        'caracteristicas': obra.caracteristicas_musica_notada.all(),
    }
    return render(request, 'catalogacion/3xx/caracteristicas_musica_notada.html', contexto)


def gestionar_medio_interpretacion_382(request, obra_id):
    """
    Gestionar Medio de Interpretación (382)
    
    Campo 382 - Medio de interpretación (Repetible)
    Subcampos repetibles:
    - $a Medio de interpretación (R)
    - $b Solista (R)
    - $n Número de intérpretes (R)
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # TODO: Implementar lógica similar a gestionar_descripcion_fisica
    # para manejar campos repetibles anidados
    
    contexto = {
        'obra': obra,
        'medios_interpretacion': obra.medios_interpretacion_382.all(),
    }
    return render(request, 'catalogacion/3xx/medio_interpretacion_382.html', contexto)


def gestionar_designacion_numerica_383(request, obra_id):
    """
    Gestionar Designación Numérica de Obra Musical (383)
    
    Campo 383 - Designación numérica de obra musical (Repetible)
    Subcampos repetibles:
    - $a Número de serie (R)
    - $b Número de opus (R)
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # TODO: Implementar lógica similar a gestionar_descripcion_fisica
    # para manejar campos repetibles anidados
    
    contexto = {
        'obra': obra,
        'designaciones': obra.designaciones_numericas.all(),
    }
    return render(request, 'catalogacion/3xx/designacion_numerica_383.html', contexto)


def listar_campos_3xx(request, obra_id):
    """
    Vista resumen de todos los campos 3XX de una obra
    
    Muestra descripción física, características técnicas y musicales.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render con todos los campos 3XX
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    # Preparar datos de descripciones físicas
    descripciones_data = []
    for desc in obra.descripciones_fisicas.all():
        descripciones_data.append({
            'id': desc.id,
            'otras_caracteristicas': desc.otras_caracteristicas_fisicas,
            'material_acompanante': desc.material_acompanante,
            'extensiones': desc.extensiones.all(),
            'dimensiones': desc.dimensiones_set.all(),
            'marc_format': desc.get_marc_format()
        })
    
    contexto = {
        'obra': obra,
        'descripciones_fisicas': descripciones_data,
        'medios_fisicos': obra.medios_fisicos.all(),
        'caracteristicas_musica': obra.caracteristicas_musica_notada.all(),
        'medios_interpretacion': obra.medios_interpretacion_382.all(),
        'designaciones_numericas': obra.designaciones_numericas.all(),
        'tonalidad': obra.tonalidad_384,
    }
    return render(request, 'catalogacion/3xx/lista_campos_3xx.html', contexto)
