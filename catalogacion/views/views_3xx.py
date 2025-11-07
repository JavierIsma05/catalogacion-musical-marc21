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
establecido para manejo de campos complejos.
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


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_descripcion_fisica_300(request, obra):
    """
    Procesar Descripción Física (300) con subcampos anidados
    Estructura HTML/JS: 
        - otras_caracteristicas_300_b_{idx}
        - material_acompanante_300_e_{idx}
        - extension_300_a_{idx_padre}_{idx}
        - dimension_300_c_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        # NOTA: JavaScript genera campos con notación MARC subcampo
        otras_caract = request.POST.get(f'otras_caracteristicas_300_b_{indice}', '').strip()
        material_acomp = request.POST.get(f'material_acompanante_300_e_{indice}', '').strip()
        
        # Verificar si hay datos
        tiene_datos = otras_caract or material_acomp
        
        # Verificar si hay extensiones
        ext_idx = 0
        while True:
            ext = request.POST.get(f'extension_300_a_{indice}_{ext_idx}', '').strip()
            if ext:
                tiene_datos = True
                break
            ext_idx += 1
            if ext_idx > 20:
                break
        
        # Verificar si hay dimensiones
        if not tiene_datos:
            dim_idx = 0
            while True:
                dim = request.POST.get(f'dimension_300_c_{indice}_{dim_idx}', '').strip()
                if dim:
                    tiene_datos = True
                    break
                dim_idx += 1
                if dim_idx > 20:
                    break
        
        if not tiene_datos:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear descripción física
        desc_fisica = DescripcionFisica.objects.create(
            obra=obra,
            otras_caracteristicas_fisicas=otras_caract,
            material_acompanante=material_acomp
        )
        
        # Procesar extensiones ($a)
        ext_idx = 0
        while True:
            extension_texto = request.POST.get(f'extension_300_a_{indice}_{ext_idx}', '').strip()
            if not extension_texto:
                ext_idx += 1
                if ext_idx > 20:
                    break
                continue
            
            Extension300.objects.create(
                descripcion_fisica=desc_fisica,
                extension=extension_texto
            )
            
            ext_idx += 1
            if ext_idx > 20:
                break
        
        # Procesar dimensiones ($c)
        dim_idx = 0
        while True:
            dimension_texto = request.POST.get(f'dimension_300_c_{indice}_{dim_idx}', '').strip()
            if not dimension_texto:
                dim_idx += 1
                if dim_idx > 20:
                    break
                continue
            
            Dimension300.objects.create(
                descripcion_fisica=desc_fisica,
                dimension=dimension_texto
            )
            
            dim_idx += 1
            if dim_idx > 20:
                break
        
        indice += 1
        if indice > 50:
            break


def procesar_medio_fisico_340(request, obra):
    """
    Procesar Medio Físico (340) con técnicas anidadas
    Estructura HTML/JS: tecnica_340_d_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        # Verificar si hay técnicas
        tiene_tecnicas = False
        tec_idx = 0
        while True:
            # JavaScript genera: tecnica_340_d_{indice}_{tec_idx}
            tec = request.POST.get(f'tecnica_340_d_{indice}_{tec_idx}', '').strip()
            if tec:
                tiene_tecnicas = True
                break
            tec_idx += 1
            if tec_idx > 20:
                break
        
        if not tiene_tecnicas:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear medio físico
        medio = MedioFisico.objects.create(obra=obra)
        
        # Procesar técnicas ($d)
        tec_idx = 0
        while True:
            tecnica_texto = request.POST.get(f'tecnica_340_d_{indice}_{tec_idx}', '').strip()
            if not tecnica_texto:
                tec_idx += 1
                if tec_idx > 20:
                    break
                continue
            
            Tecnica340.objects.create(
                medio_fisico=medio,
                tecnica=tecnica_texto
            )
            
            tec_idx += 1
            if tec_idx > 20:
                break
        
        indice += 1
        if indice > 50:
            break


def procesar_caracteristica_musica_348(request, obra):
    """
    Procesar Características Música Notada (348) con formatos anidados
    Estructura HTML/JS: formato_348_a_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        # Verificar si hay formatos
        tiene_formatos = False
        fmt_idx = 0
        while True:
            # JavaScript genera: formato_348_a_{indice}_{fmt_idx}
            fmt = request.POST.get(f'formato_348_a_{indice}_{fmt_idx}', '').strip()
            if fmt:
                tiene_formatos = True
                break
            fmt_idx += 1
            if fmt_idx > 20:
                break
        
        if not tiene_formatos:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear característica
        caract = CaracteristicaMusicaNotada.objects.create(obra=obra)
        
        # Procesar formatos ($a)
        fmt_idx = 0
        while True:
            formato_texto = request.POST.get(f'formato_348_a_{indice}_{fmt_idx}', '').strip()
            if not formato_texto:
                fmt_idx += 1
                if fmt_idx > 20:
                    break
                continue
            
            Formato348.objects.create(
                caracteristica=caract,
                formato=formato_texto
            )
            
            fmt_idx += 1
            if fmt_idx > 20:
                break
        
        indice += 1
        if indice > 50:
            break


def procesar_medio_interpretacion_382(request, obra):
    """
    Procesar Medio de Interpretación (382) con subcampos anidados
    Estructura HTML/JS:
        - medio_382_a_{idx_padre}_{idx}
        - solista_382_b_{idx_padre}_{idx}
        - numero_interpretes_382_n_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        # Verificar subcampos
        tiene_datos = False
        
        # Verificar si hay medios
        sub_idx = 0
        while True:
            val = request.POST.get(f'medio_382_a_{indice}_{sub_idx}', '').strip()
            if val:
                tiene_datos = True
                break
            sub_idx += 1
            if sub_idx > 20:
                break
        
        # Verificar si hay solistas
        if not tiene_datos:
            sub_idx = 0
            while True:
                val = request.POST.get(f'solista_382_b_{indice}_{sub_idx}', '').strip()
                if val:
                    tiene_datos = True
                    break
                sub_idx += 1
                if sub_idx > 20:
                    break
        
        # Verificar si hay números de intérpretes
        if not tiene_datos:
            sub_idx = 0
            while True:
                val = request.POST.get(f'numero_interpretes_382_n_{indice}_{sub_idx}', '').strip()
                if val:
                    tiene_datos = True
                    break
                sub_idx += 1
                if sub_idx > 20:
                    break
        
        if not tiene_datos:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear medio de interpretación
        medio = MedioInterpretacion382.objects.create(obra=obra)
        
        # Procesar medios ($a)
        sub_idx = 0
        while True:
            medio_texto = request.POST.get(f'medio_382_a_{indice}_{sub_idx}', '').strip()
            if not medio_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            MedioInterpretacion382_a.objects.create(
                medio_interpretacion=medio,
                medio=medio_texto
            )
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        # Procesar solistas ($b)
        sub_idx = 0
        while True:
            solista_texto = request.POST.get(f'solista_382_b_{indice}_{sub_idx}', '').strip()
            if not solista_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            Solista382.objects.create(
                medio_interpretacion=medio,
                solista=solista_texto
            )
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        # Procesar número intérpretes ($n)
        sub_idx = 0
        while True:
            numero_texto = request.POST.get(f'numero_interpretes_382_n_{indice}_{sub_idx}', '').strip()
            if not numero_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            try:
                numero_int = int(numero_texto)
                NumeroInterpretes382.objects.create(
                    medio_interpretacion=medio,
                    numero=numero_int
                )
            except ValueError:
                pass  # Ignorar valores no numéricos
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        indice += 1
        if indice > 50:
            break


def procesar_designacion_numerica_383(request, obra):
    """
    Procesar Designación Numérica (383) con subcampos anidados
    Estructura HTML/JS:
        - numero_obra_383_a_{idx_padre}_{idx}
        - opus_383_b_{idx_padre}_{idx}
    """
    indice = 0
    while True:
        # Verificar si hay números de obra u opus
        tiene_datos = False
        
        # Verificar números de obra
        num_idx = 0
        while True:
            val = request.POST.get(f'numero_obra_383_a_{indice}_{num_idx}', '').strip()
            if val:
                tiene_datos = True
                break
            num_idx += 1
            if num_idx > 20:
                break
        
        # Verificar opus
        if not tiene_datos:
            opus_idx = 0
            while True:
                val = request.POST.get(f'opus_383_b_{indice}_{opus_idx}', '').strip()
                if val:
                    tiene_datos = True
                    break
                opus_idx += 1
                if opus_idx > 20:
                    break
        
        if not tiene_datos:
            indice += 1
            if indice > 50:
                break
            continue
        
        # Crear designación numérica
        designacion = DesignacionNumericaObra.objects.create(obra=obra)
        
        # Procesar números de obra ($a)
        sub_idx = 0
        while True:
            numero_texto = request.POST.get(f'numero_obra_383_a_{indice}_{sub_idx}', '').strip()
            if not numero_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            NumeroObra383.objects.create(
                designacion_numerica=designacion,
                numero_obra=numero_texto
            )
            
            sub_idx += 1
            if sub_idx > 20:
                break
        
        # Procesar opus ($b)
        sub_idx = 0
        while True:
            opus_texto = request.POST.get(f'opus_383_b_{indice}_{sub_idx}', '').strip()
            if not opus_texto:
                sub_idx += 1
                if sub_idx > 20:
                    break
                continue
            
            Opus383.objects.create(
                designacion_numerica=designacion,
                opus=opus_texto
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
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Procesar usando la función de procesamiento
                procesar_descripcion_fisica_300(request, obra)
                messages.success(request, '✅ Descripción física guardada correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar descripción física: {str(e)}')
    
    # Preparar datos para el template
    descripciones = obra.descripciones_fisicas.all().order_by('id')
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
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                procesar_medio_fisico_340(request, obra)
                messages.success(request, '✅ Medio físico guardado correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar medio físico: {str(e)}')
    
    contexto = {
        'obra': obra,
        'medios_fisicos': obra.medios_fisicos.all(),
    }
    
    return render(request, 'catalogacion/3xx/medio_fisico.html', contexto)


def gestionar_caracteristicas_musica_notada(request, obra_id):
    """
    Gestionar Características de Música Notada (348)
    Campo 348 - Características de música notada (Repetible)
    Subcampos:
      - $a Formato de la música notada (R)
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                procesar_caracteristica_musica_348(request, obra)
                messages.success(request, '✅ Características de música notada guardadas correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar características: {str(e)}')
    
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
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                procesar_medio_interpretacion_382(request, obra)
                messages.success(request, '✅ Medio de interpretación guardado correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar medio de interpretación: {str(e)}')
    
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
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                procesar_designacion_numerica_383(request, obra)
                messages.success(request, '✅ Designación numérica guardada correctamente')
                return redirect('detalle_obra', obra_id=obra_id)
        except Exception as e:
            messages.error(request, f'❌ Error al guardar designación numérica: {str(e)}')
    
    contexto = {
        'obra': obra,
        'designaciones': obra.designaciones_numericas.all(),
    }
    
    return render(request, 'catalogacion/3xx/designacion_numerica_383.html', contexto)


def listar_campos_3xx(request, obra_id):
    """
    Vista resumen de todos los campos 3XX de una obra
    Muestra descripción física, características técnicas y musicales.
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
