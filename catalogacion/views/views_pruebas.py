"""
Vistas de Pruebas y Desarrollo
==============================

Vistas para testing, desarrollo y pruebas de funcionalidad.

Incluye:
- Pruebas de campos repetibles anidados
- Datos de ejemplo y testing
- Limpieza de datos de prueba
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    DescripcionFisica,
    Extension300,
    Dimension300,
)


def prueba_campo_300(request, obra_id=None):
    """
    Vista de prueba para manejar el campo 300 con subcampos repetibles
    
    Campo 300 - Descripción física (Repetible)
    Estructura:
    - Campo 300 (R)
        - $a Extensión (R)
        - $b Otras características físicas (NR)
        - $c Dimensión (R)
        - $e Material acompañante (NR)
    
    Esta vista demuestra el patrón para manejar campos repetibles
    con subcampos repetibles anidados.
    
    Args:
        obra_id: ID de la obra (opcional, crea obra de prueba si no se especifica)
    
    Returns:
        Render del formulario de prueba
    """
    
    # Obtener o crear obra de prueba
    if obra_id:
        obra = get_object_or_404(ObraGeneral, pk=obra_id)
    else:
        # Buscar si existe una obra de prueba
        obra = ObraGeneral.objects.filter(
            titulo_principal='OBRA DE PRUEBA - Campo 300'
        ).first()
        
        if not obra:
            # Crear obra de prueba
            obra = ObraGeneral.objects.create(
                titulo_principal='OBRA DE PRUEBA - Campo 300',
                subtitulo='Prueba de campos repetibles anidados'
            )
            messages.success(request, f'✅ Obra de prueba creada (ID: {obra.id})')
    
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
                
                messages.success(request, '✅ Campo 300 guardado correctamente')
                return redirect('prueba_campo_300')
                
        except Exception as e:
            messages.error(request, f'❌ Error al guardar: {str(e)}')
    
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
    
    return render(request, 'catalogacion/prueba_campo_300.html', contexto)


def limpiar_prueba_300(request):
    """
    Elimina todas las obras de prueba del campo 300
    
    Útil para limpiar datos de testing y desarrollo.
    
    Returns:
        Redirect a la página de prueba con mensaje de confirmación
    """
    obras_prueba = ObraGeneral.objects.filter(
        titulo_principal__icontains='OBRA DE PRUEBA'
    )
    cantidad = obras_prueba.count()
    obras_prueba.delete()
    
    messages.success(request, f'✅ Se eliminaron {cantidad} obra(s) de prueba')
    return redirect('prueba_campo_300')
