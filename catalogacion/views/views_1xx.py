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


# =============================================================================
# FUNCIONES DE PROCESAMIENTO MASIVO (para formulario principal de obra_general)
# =============================================================================

def procesar_compositor(request, obra):
    """
    Procesa todos los campos 100 - Compositor desde el formulario principal
    
    Maneja:
    - Compositor con AutoridadPersona ($a y $d)
    - Funciones de compositor ($e) - repetibles
    - Atribuciones ($j) - repetibles
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    from ..models.autoridades import AutoridadPersona
    
    # Obtener datos del compositor
    apellidos_nombres = request.POST.get('compositor_apellidos_nombres', '').strip()
    fechas = request.POST.get('compositor_fechas', '').strip()
    
    if apellidos_nombres:
        # Crear o recuperar la autoridad de persona
        persona, created = AutoridadPersona.objects.get_or_create(
            apellidos_nombres=apellidos_nombres,
            defaults={'fechas': fechas}
        )
        
        # Si ya existe pero tiene fechas diferentes, actualizar
        if not created and fechas and persona.fechas != fechas:
            persona.fechas = fechas
            persona.save()
        
        # Asignar compositor a la obra
        obra.compositor = persona
        obra.save()
        
        # Procesar funciones del compositor ($e) - repetibles
        idx = 0
        while True:
            funcion = request.POST.get(f'funcion_compositor_e_{idx}')
            if funcion is None:
                break
            if funcion.strip():
                FuncionCompositor.objects.create(
                    obra=obra,
                    funcion=funcion.strip()
                )
            idx += 1
        
        # Procesar atribuciones ($j) - repetibles
        idx = 0
        while True:
            atribucion = request.POST.get(f'atribucion_compositor_j_{idx}')
            if atribucion is None:
                break
            if atribucion.strip():
                AtribucionCompositor.objects.create(
                    obra=obra,
                    atribucion=atribucion.strip()
                )
            idx += 1


def procesar_titulo_uniforme_130(request, obra):
    """
    Procesa el campo 130 - Título Uniforme Musical (solo si NO hay compositor)
    
    Maneja:
    - Título uniforme base
    - Tonalidad ($r)
    - Subcampos $k, $m, $n, $p (procesados por procesar_subcampos_130)
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    from ..models.autoridades import AutoridadTituloUniforme
    
    titulo_130 = request.POST.get('titulo_uniforme_130')
    tonalidad_130 = request.POST.get('titulo_uniforme_tonalidad')
    
    if titulo_130 and titulo_130.strip():
        # Crear o recuperar autoridad de título uniforme
        titulo_autoridad, created = AutoridadTituloUniforme.objects.get_or_create(
            titulo=titulo_130.strip()
        )
        
        # Asignar a la obra
        obra.titulo_uniforme = titulo_autoridad
        
        # Asignar tonalidad si existe
        if tonalidad_130:
            obra.titulo_uniforme_tonalidad = tonalidad_130
            
        obra.save()
        
        # Procesar subcampos $k, $m, $n, $p
        procesar_subcampos_130(request, obra)


def procesar_subcampos_130(request, obra):
    """
    Procesa los subcampos del campo 130 - Título Uniforme
    
    Maneja:
    - $k Forma musical (ForeignKey a AutoridadFormaMusical) - repetible
    - $m Medio de interpretación - repetible
    - $n Número de parte/sección - repetible
    - $p Nombre de parte/sección - repetible
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    from ..models.autoridades import AutoridadFormaMusical
    
    # Procesar $k - Forma musical (repetible, con autoridad)
    formas_130 = request.POST.getlist('forma_130')
    for forma_nombre in formas_130:
        if forma_nombre.strip():
            # Crear o recuperar autoridad de forma musical
            forma_autoridad, created = AutoridadFormaMusical.objects.get_or_create(
                nombre=forma_nombre.strip()
            )
            Forma130.objects.create(
                obra=obra,
                forma=forma_autoridad
            )
    
    # Procesar $m - Medio de interpretación (repetible)
    medios_130 = request.POST.getlist('medio_130')
    for medio in medios_130:
        if medio.strip():
            MedioInterpretacion130.objects.create(
                obra=obra,
                medio=medio.strip()
            )
    
    # Procesar $n - Número de parte/sección (repetible)
    numeros_130 = request.POST.getlist('numero_130')
    for numero in numeros_130:
        if numero.strip():
            NumeroParteSección130.objects.create(
                obra=obra,
                numero=numero.strip()
            )
    
    # Procesar $p - Nombre de parte/sección (repetible)
    nombres_130 = request.POST.getlist('nombre_130')
    for nombre in nombres_130:
        if nombre.strip():
            NombreParteSección130.objects.create(
                obra=obra,
                nombre=nombre.strip()
            )


def procesar_titulo_uniforme_240(request, obra):
    """
    Procesa el campo 240 - Título Uniforme con Compositor (solo si HAY compositor)
    
    Maneja:
    - Título uniforme base
    - Tonalidad ($r)
    - Subcampos $k, $m, $n, $p (procesados por procesar_subcampos_240)
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    from ..models.autoridades import AutoridadTituloUniforme
    
    titulo_240 = request.POST.get('titulo_240')
    tonalidad_240 = request.POST.get('titulo_240_tonalidad')
    
    if titulo_240 and titulo_240.strip():
        # Crear o recuperar autoridad de título uniforme
        titulo_autoridad, created = AutoridadTituloUniforme.objects.get_or_create(
            titulo=titulo_240.strip()
        )
        
        # Asignar a la obra
        obra.titulo_240 = titulo_autoridad
        
        # Asignar tonalidad si existe
        if tonalidad_240:
            obra.titulo_240_tonalidad = tonalidad_240
            
        obra.save()
        
        # Procesar subcampos $k, $m, $n, $p
        procesar_subcampos_240(request, obra)


def procesar_subcampos_240(request, obra):
    """
    Procesa los subcampos del campo 240 - Título Uniforme con Compositor
    
    Maneja:
    - $k Forma musical (CharField con choices) - repetible
    - $m Medio de interpretación - repetible
    - $n Número de parte/sección - repetible
    - $p Nombre de parte/sección - repetible
    
    Args:
        request: HttpRequest con datos POST
        obra: Instancia de ObraGeneral
    """
    # Procesar $k - Forma musical (repetible, choices directas)
    formas_240 = request.POST.getlist('forma_240')
    for forma_valor in formas_240:
        if forma_valor.strip():
            Forma240.objects.create(
                obra=obra,
                forma=forma_valor.strip()
            )
    
    # Procesar $m - Medio de interpretación (repetible)
    medios_240 = request.POST.getlist('medio_240')
    for medio in medios_240:
        if medio.strip():
            MedioInterpretacion240.objects.create(
                obra=obra,
                medio=medio.strip()
            )
    
    # Procesar $n - Número de parte/sección (repetible)
    numeros_240 = request.POST.getlist('numero_240')
    for numero in numeros_240:
        if numero.strip():
            NumeroParteSección240.objects.create(
                obra=obra,
                numero=numero.strip()
            )
    
    # Procesar $p - Nombre de parte/sección (repetible)
    nombres_240 = request.POST.getlist('nombre_240')
    for nombre in nombres_240:
        if nombre.strip():
            NombreParteSección240.objects.create(
                obra=obra,
                nombre=nombre.strip()
            )
