"""
Vistas Bloque 1XX - Puntos de Acceso Principal
==============================================

Gestión de campos MARC21 del bloque 1XX (Puntos de acceso principal).

Campos incluidos:
- 100: Punto de acceso principal - Nombre de persona (Compositor)
- 130: Punto de acceso principal - Título uniforme
- 240: Título uniforme

Subcampos relacionados:
- Funciones del compositor
- Atribuciones del compositor
- Formas musicales (130/240)
- Medio de interpretación (130/240)
- Número de parte/sección (130/240)
- Nombre de parte/sección (130/240)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from ..models import (
    ObraGeneral,
    FuncionCompositor,
    AtribucionCompositor,
    Forma130,
    MedioInterpretacion130,
    NumeroParteSección130,
    NombreParteSección130,
    Forma240,
    MedioInterpretacion240,
    NumeroParteSección240,
    NombreParteSección240,
)

from ..forms import (
    FuncionCompositorFormSet,
    AtribucionCompositorFormSet,
    Forma130FormSet,
    MedioInterpretacion130FormSet,
    NumeroParteSección130FormSet,
    NombreParteSección130FormSet,
    Forma240FormSet,
    MedioInterpretacion240FormSet,
    NumeroParteSección240FormSet,
    NombreParteSección240FormSet,
)


def gestionar_funciones_compositor(request, obra_id):
    """
    Gestionar Funciones del Compositor (100 $e)
    
    Campo 100 $e - Término de función (Repetible)
    Especifica el rol del compositor (compositor, arreglista, etc.)
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = FuncionCompositorFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Funciones del compositor guardadas correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar funciones: {str(e)}')
    else:
        formset = FuncionCompositorFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/1xx/funciones_compositor.html', contexto)


def gestionar_atribuciones_compositor(request, obra_id):
    """
    Gestionar Atribuciones del Compositor (100 $j)
    
    Campo 100 $j - Término de atribución (Repetible)
    Indica atribuciones o calificativos del compositor.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        formset = AtribucionCompositorFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Atribuciones guardadas correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error al guardar atribuciones: {str(e)}')
    else:
        formset = AtribucionCompositorFormSet(instance=obra)
    
    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/1xx/atribuciones_compositor.html', contexto)


def gestionar_titulo_uniforme_130(request, obra_id):
    """
    Gestionar Título Uniforme - Campo 130
    
    Campo 130 - Punto de acceso principal - Título uniforme
    Incluye subcampos repetibles:
    - $r: Forma musical (R)
    - $m: Medio de interpretación (R)
    - $n: Número de parte/sección (R)
    - $p: Nombre de parte/sección (R)
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Guardar formas musicales
                formset_formas = Forma130FormSet(request.POST, instance=obra, prefix='formas')
                if formset_formas.is_valid():
                    formset_formas.save()
                
                # Guardar medios de interpretación
                formset_medios = MedioInterpretacion130FormSet(request.POST, instance=obra, prefix='medios')
                if formset_medios.is_valid():
                    formset_medios.save()
                
                # Guardar números de parte/sección
                formset_numeros = NumeroParteSección130FormSet(request.POST, instance=obra, prefix='numeros')
                if formset_numeros.is_valid():
                    formset_numeros.save()
                
                # Guardar nombres de parte/sección
                formset_nombres = NombreParteSección130FormSet(request.POST, instance=obra, prefix='nombres')
                if formset_nombres.is_valid():
                    formset_nombres.save()
                
                messages.success(request, '✅ Título uniforme 130 guardado correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar título uniforme: {str(e)}')
    else:
        formset_formas = Forma130FormSet(instance=obra, prefix='formas')
        formset_medios = MedioInterpretacion130FormSet(instance=obra, prefix='medios')
        formset_numeros = NumeroParteSección130FormSet(instance=obra, prefix='numeros')
        formset_nombres = NombreParteSección130FormSet(instance=obra, prefix='nombres')
    
    contexto = {
        'obra': obra,
        'formset_formas': formset_formas,
        'formset_medios': formset_medios,
        'formset_numeros': formset_numeros,
        'formset_nombres': formset_nombres,
    }
    return render(request, 'catalogacion/1xx/titulo_uniforme_130.html', contexto)


def gestionar_titulo_uniforme_240(request, obra_id):
    """
    Gestionar Título Uniforme - Campo 240
    
    Campo 240 - Título uniforme
    Incluye subcampos repetibles:
    - $r: Forma musical (R)
    - $m: Medio de interpretación (R)
    - $n: Número de parte/sección (R)
    - $p: Nombre de parte/sección (R)
    
    Patrón de campos repetibles anidados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render del formulario o redirect después de guardar
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Guardar formas musicales
                formset_formas = Forma240FormSet(request.POST, instance=obra, prefix='formas')
                if formset_formas.is_valid():
                    formset_formas.save()
                
                # Guardar medios de interpretación
                formset_medios = MedioInterpretacion240FormSet(request.POST, instance=obra, prefix='medios')
                if formset_medios.is_valid():
                    formset_medios.save()
                
                # Guardar números de parte/sección
                formset_numeros = NumeroParteSección240FormSet(request.POST, instance=obra, prefix='numeros')
                if formset_numeros.is_valid():
                    formset_numeros.save()
                
                # Guardar nombres de parte/sección
                formset_nombres = NombreParteSección240FormSet(request.POST, instance=obra, prefix='nombres')
                if formset_nombres.is_valid():
                    formset_nombres.save()
                
                messages.success(request, '✅ Título uniforme 240 guardado correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar título uniforme: {str(e)}')
    else:
        formset_formas = Forma240FormSet(instance=obra, prefix='formas')
        formset_medios = MedioInterpretacion240FormSet(instance=obra, prefix='medios')
        formset_numeros = NumeroParteSección240FormSet(instance=obra, prefix='numeros')
        formset_nombres = NombreParteSección240FormSet(instance=obra, prefix='nombres')
    
    contexto = {
        'obra': obra,
        'formset_formas': formset_formas,
        'formset_medios': formset_medios,
        'formset_numeros': formset_numeros,
        'formset_nombres': formset_nombres,
    }
    return render(request, 'catalogacion/1xx/titulo_uniforme_240.html', contexto)


def listar_campos_1xx(request, obra_id):
    """
    Vista resumen de todos los campos 1XX de una obra
    
    Muestra todos los puntos de acceso principal registrados.
    
    Args:
        obra_id: ID de la obra
    
    Returns:
        Render con todos los campos 1XX
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    contexto = {
        'obra': obra,
        'funciones_compositor': obra.funciones_compositor.all(),
        'atribuciones_compositor': obra.atribuciones_compositor.all(),
        'formas_130': obra.formas_130.all(),
        'medios_130': obra.medios_interpretacion_130.all(),
        'numeros_130': obra.numeros_parte_130.all(),
        'nombres_130': obra.nombres_parte_130.all(),
        'formas_240': obra.formas_240.all(),
        'medios_240': obra.medios_interpretacion_240.all(),
        'numeros_240': obra.numeros_parte_240.all(),
        'nombres_240': obra.nombres_parte_240.all(),
    }
    return render(request, 'catalogacion/1xx/lista_campos_1xx.html', contexto)
