"""
Vistas Base - Sistema de Catalogación MARC21 Musical
====================================================

Vistas generales de navegación y páginas principales.
No están relacionadas directamente con bloques MARC específicos.
"""

import logging
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
import json

from .debug_datos import debug_obra_datos


from ..models import ObraGeneral
from ..models.obra_general import TONALIDADES
from ..models.bloque_0xx import (
    CodigoPaisEntidad,
    CodigoLengua,
    NumeroEditor,
    IncipitMusical,
    CODIGOS_LENGUAJE
)

from .views_0xx import (
    procesar_isbn,
    procesar_ismn,
    procesar_numero_editor,
    procesar_incipit,
    procesar_codigo_lengua,
    procesar_codigo_pais,
)

from .views_1xx import (
    procesar_compositor,
    procesar_titulo_uniforme_130,
    procesar_titulo_uniforme_240,
)

from .views_2xx import (
    procesar_titulo_alternativo,
    procesar_edicion,
    procesar_produccion_publicacion,
)

from .views_3xx import (
    procesar_descripcion_fisica_300,
    procesar_medio_fisico_340,
    procesar_caracteristica_musica_348,
    procesar_medio_interpretacion_382,
    procesar_designacion_numerica_383,
)

from .views_4xx import (
    procesar_mencion_serie_490,
)

logger = logging.getLogger(__name__)



def index(request):
    """
    Vista principal del sistema - Página de inicio
    
    Muestra enlaces a las diferentes secciones del sistema de catalogación.
    """
    return render(request, 'index.html')


def plantillas(request):
    """
    Vista de plantillas de catalogación
    
    Muestra las diferentes plantillas MARC21 disponibles para catalogación.
    """
    return render(request, 'plantillas.html')


def _debug_datos_ordenados(request):
    print("\n" + "="*80)
    print("📋 DATOS RECIBIDOS DEL FORMULARIO".center(80))
    print("="*80 + "\n")
    
    # Agrupar datos por prefijo
    grupos = {
        'CABECERA': ['tipo_registro', 'nivel_bibliografico'],
        'ISBN (020)': ['isbn_'],
        'ISMN (024)': ['ismn_'],
        'NÚMERO EDITOR (028)': ['numero_editor_'],
        'INCIPIT (031)': ['incipit_'],
        'FUENTE CAT. (040)': ['centro_catalogador'],
        'CÓDIGO LENGUA (041)': ['codigo_lengua_'],
        'CÓDIGO PAÍS (044)': ['codigo_pais_'],
        'COMPOSITOR (100)': ['compositor_', 'funcion_compositor_', 'atribucion_compositor_'],
        'TÍTULO UNIFORME 130': ['titulo_uniforme_130', 'forma_130_', 'medio_130_', 'numero_130_', 'nombre_130_'],
        'TÍTULO UNIFORME 240': ['titulo_uniforme_240', 'forma_240_', 'medio_240_', 'numero_240_', 'nombre_240_'],
        'TÍTULO PRINCIPAL (245)': ['titulo_principal', 'subtitulo', 'mencion_responsabilidad'],
        'TÍTULO ALTERNATIVO (246)': ['titulo_alternativo_'],
        'EDICIÓN (250)': ['edicion_'],
        'PRODUCCIÓN (264)': ['produccion_'],
        'DESC. FÍSICA (300)': ['descripcion_fisica_'],
        'MEDIO FÍSICO (340)': ['medio_fisico_', 'tecnica_340_'],
        'CARACT. MÚSICA (348)': ['caracteristica_musica_'],
        'MEDIO INTERP. (382)': ['medio_interpretacion_382_', 'instrumento_382_'],
        'DESIG. NUMÉRICA (383)': ['designacion_numerica_', 'numero_serial_383_', 'numero_opus_383_'],
        'TONALIDAD (384)': ['tonalidad_384'],
        'SERIE (490)': ['mencion_serie_', 'titulo_serie_490_', 'volumen_serie_490_'],
    }
    
    # Contar total de campos
    total_campos = len(request.POST)
    campos_mostrados = 0
    
    for titulo, prefijos in grupos.items():
        campos = {}
        for key, value in request.POST.items():
            if any(key.startswith(prefijo) if prefijo.endswith('_') else key == prefijo for prefijo in prefijos):
                # Mostrar TODOS los campos (con o sin valor)
                campos[key] = value if value.strip() else '(vacío)'
                campos_mostrados += 1
        
        if campos:
            print(f"\n🔹 {titulo}")
            print("-" * 80)
            for key, value in sorted(campos.items()):
                # Truncar valores muy largos
                valor_mostrar = value if len(value) <= 60 else value[:57] + "..."
                # Colorear campos vacíos
                if value == '(vacío)':
                    print(f"  {key:40} = {valor_mostrar}")
                else:
                    print(f"  {key:40} = {valor_mostrar}")
    
    # Mostrar campos no categorizados
    campos_no_categorizados = {}
    for key, value in request.POST.items():
        if key not in ['csrfmiddlewaretoken']:  # Ignorar CSRF
            categorizado = False
            for prefijos in grupos.values():
                if any(key.startswith(prefijo) if prefijo.endswith('_') else key == prefijo for prefijo in prefijos):
                    categorizado = True
                    break
            if not categorizado:
                campos_no_categorizados[key] = value if value.strip() else '(vacío)'
    
    if campos_no_categorizados:
        print(f"\n🔹 CAMPOS NO CATEGORIZADOS")
        print("-" * 80)
        for key, value in sorted(campos_no_categorizados.items()):
            valor_mostrar = value if len(value) <= 60 else value[:57] + "..."
            print(f"  {key:40} = {valor_mostrar}")
    
    print("\n" + "="*80)
    print(f"📊 RESUMEN: {total_campos} campos totales | {campos_mostrados} categorizados | {len(campos_no_categorizados)} no categorizados")
    print("="*80 + "\n")


@transaction.atomic
def crear_obra(request):
    """
    Vista para crear una nueva obra general
    
    Renderiza el formulario completo para catalogar una obra musical
    Maneja tanto GET (mostrar formulario) como POST (guardar datos).
    """
    if request.method == 'POST':
        # MOSTRAR DATOS ANTES DE GUARDAR
        print("\n" + "="*110)
        print("🚀 INICIANDO GUARDADO DE OBRA")
        print("="*110)
        # debug_obra_datos(request)
        _debug_datos_ordenados(request)
        
        try:
            with transaction.atomic():
                print("\n📌 PASO 1: Creando ObraGeneral...")
                obra = ObraGeneral()
                
                #* Cabecera
                obra.tipo_registro = request.POST.get('tipo_registro', 'd')
                obra.nivel_bibliografico = request.POST.get('nivel_bibliografico', 'm')
                
                #* Bloque 0XX - Campos fijos no repetibles
                # 040 - Fuente de catalogación
                obra.centro_catalogador = request.POST.get('centro_catalogador', 'UNL')
                
                # Guardar obra primero para tener el ID
                print("  ✓ Guardando ObraGeneral (para obtener ID)...")
                obra.save()
                print(f"  ✓ ObraGeneral guardada con ID: {obra.id}")
                
                # ========================================
                # PASO 2: Bloque 0XX - Campos repetibles
                # ========================================
                print("\n📌 PASO 2: Procesando Bloque 0XX...")
                
                print("  • Procesando ISBN...")
                procesar_isbn(request, obra)
                
                print("  • Procesando ISMN...")
                procesar_ismn(request, obra)
                
                print("  • Procesando Número de Editor...")
                procesar_numero_editor(request, obra)
                
                print("  • Procesando Incipit Musical...")
                procesar_incipit(request, obra)
                
                print("  • Procesando Código de Lengua...")
                procesar_codigo_lengua(request, obra)
                
                print("  • Procesando Código de País...")
                procesar_codigo_pais(request, obra)
                
                # ========================================
                # PASO 3: Bloque 1XX
                # ========================================
                print("\n📌 PASO 3: Procesando Bloque 1XX...")
                
                print("  • Procesando Compositor...")
                procesar_compositor(request, obra)
                
                print("  • Procesando Título Uniforme (130)...")
                procesar_titulo_uniforme_130(request, obra)
                
                print("  • Procesando Título Uniforme (240)...")
                procesar_titulo_uniforme_240(request, obra)
                
                # ========================================
                # PASO 4: Bloque 2XX
                # ========================================
                print("\n📌 PASO 4: Procesando Bloque 2XX...")
                
                print("  • Asignando Título Principal...")
                obra.titulo_principal = request.POST.get('titulo_principal', '')
                obra.subtitulo = request.POST.get('subtitulo', '')
                obra.mencion_responsabilidad = request.POST.get('mencion_responsabilidad', '')
                
                print("  • Procesando Título Alternativo...")
                procesar_titulo_alternativo(request, obra)
                
                print("  • Procesando Edición...")
                procesar_edicion(request, obra)
                
                print("  • Procesando Producción/Publicación...")
                procesar_produccion_publicacion(request, obra)
                
                # ========================================
                # PASO 5: Bloque 3XX
                # ========================================
                print("\n📌 PASO 5: Procesando Bloque 3XX...")
                
                print("  • Procesando Descripción Física...")
                procesar_descripcion_fisica_300(request, obra)
                
                print("  • Procesando Medio Físico...")
                procesar_medio_fisico_340(request, obra)
                
                print("  • Procesando Características de Música Notada...")
                procesar_caracteristica_musica_348(request, obra)
                
                print("  • Procesando Medio de Interpretación...")
                procesar_medio_interpretacion_382(request, obra)
                
                print("  • Procesando Designación Numérica...")
                procesar_designacion_numerica_383(request, obra)
                
                print("  • Asignando Tonalidad...")
                obra.tonalidad_384 = request.POST.get('tonalidad_384', '')
                
                # ========================================
                # PASO 6: Bloque 4XX
                # ========================================
                print("\n📌 PASO 6: Procesando Bloque 4XX...")
                
                print("  • Procesando Mención de Serie...")
                procesar_mencion_serie_490(request, obra)
                
                # ========================================
                # PASO 7: Generación de datos automáticos
                # ========================================
                print("\n📌 PASO 7: Generando datos automáticos...")
                
                print("  • Generando clasificación 092...")
                obra.generar_clasificacion_092()
                
                print("  • Guardando obra completa...")
                obra.save()
                
                print("\n" + "="*110)
                print("✅ ÉXITO: Obra guardada exitosamente")
                print("="*110)
                print(f"  📄 Número de control: {obra.num_control}")
                print(f"  🆔 ID: {obra.id}")
                print(f"  📅 Fecha creación: {obra.fecha_creacion_sistema}")
                print("="*110 + "\n")
                
                messages.success(
                    request, 
                    f'✅ Obra creada exitosamente. Número de control: {obra.num_control}'
                )
                return redirect('crear_obra')
        
        # ========================================
        # MANEJO DE ERRORES ESPECÍFICOS
        # ========================================
        except ValidationError as ve:
            """Error de validación de campos"""
            print("\n" + "❌"*55)
            print("❌ ERROR DE VALIDACIÓN (ValidationError)")
            print("❌"*55)
            print(f"\n🔴 Mensaje: {str(ve)}")
            if hasattr(ve, 'error_dict'):
                print("\n📋 Errores por campo:")
                for campo, errores in ve.error_dict.items():
                    print(f"  • {campo}: {errores}")
            elif hasattr(ve, 'error_list'):
                print("\n📋 Errores:")
                for error in ve.error_list:
                    print(f"  • {error}")
            print("\n🔗 Traceback:")
            print(traceback.format_exc())
            print("❌"*55 + "\n")
            
            messages.error(request, f'❌ Error de validación: {str(ve)}')
            return redirect('crear_obra')
        
        except IntegrityError as ie:
            """Error de integridad de base de datos (ForeignKey, constraint, etc)"""
            print("\n" + "❌"*55)
            print("❌ ERROR DE INTEGRIDAD DE BASE DE DATOS (IntegrityError)")
            print("❌"*55)
            print(f"\n🔴 Mensaje: {str(ie)}")
            print("\nℹ️  Esto puede ser causado por:")
            print("  • Campo ForeignKey que no existe")
            print("  • Violación de restricción UNIQUE")
            print("  • Violación de NOT NULL")
            print("  • Valores inválidos para el campo")
            print("\n🔗 Traceback:")
            print(traceback.format_exc())
            print("❌"*55 + "\n")
            
            messages.error(request, f'❌ Error de integridad de datos: {str(ie)}')
            return redirect('crear_obra')
        
        except ValueError as ve:
            """Error de conversión de tipo o valor inválido"""
            print("\n" + "❌"*55)
            print("❌ ERROR DE VALOR (ValueError)")
            print("❌"*55)
            print(f"\n🔴 Mensaje: {str(ve)}")
            print("\nℹ️  Esto puede ser causado por:")
            print("  • Valor que no se puede convertir al tipo esperado")
            print("  • Campo numérico con valor no numérico")
            print("  • Fecha inválida")
            print("\n🔗 Traceback:")
            print(traceback.format_exc())
            print("❌"*55 + "\n")
            
            messages.error(request, f'❌ Error de valor: {str(ve)}')
            return redirect('crear_obra')
        
        except Exception as e:
            """Error genérico - captura cualquier otra excepción"""
            print("\n" + "❌"*55)
            print("❌ ERROR GENÉRICO (Exception)")
            print("❌"*55)
            print(f"\n🔴 Tipo de error: {type(e).__name__}")
            print(f"🔴 Mensaje: {str(e)}")
            print("\n🔗 Traceback completo:")
            print(traceback.format_exc())
            print("❌"*55 + "\n")
            
            # Log para archivo
            logger.exception("Error al guardar obra")
            
            messages.error(request, f'❌ Error al guardar la obra: {str(e)}')
            return redirect('crear_obra')
    
    # ========================================
    # GET - Mostrar formulario vacío
    # ========================================
    print("\n📝 Mostrando formulario para crear nueva obra\n")
    
    # Convertir listas a JSON para JavaScript
    codigos_pais_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == 'ec'}
        for codigo, nombre in CodigoPaisEntidad.CODIGOS_PAIS
    ])
    
    codigos_idioma_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == 'spa'}
        for codigo, nombre in CODIGOS_LENGUAJE
    ])
    
    tipo_numero_editor_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == '2'}
        for codigo, nombre in NumeroEditor.TIPO_NUMERO
    ])
    
    control_nota_editor_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == '0'}
        for codigo, nombre in NumeroEditor.CONTROL_NOTA
    ])
    
    indicacion_traduccion_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == '0'}
        for codigo, nombre in CodigoLengua.INDICACION_TRADUCCION
    ])
    
    fuente_codigo_json = json.dumps([
        {'value': codigo, 'text': nombre, 'selected': codigo == '#'}
        for codigo, nombre in CodigoLengua.FUENTE_CODIGO
    ])
    
    # Valores predeterminados para Incipit Musical (031)
    incipit_defaults = {
        'numero_obra': IncipitMusical._meta.get_field('numero_obra').default,
        'numero_movimiento': IncipitMusical._meta.get_field('numero_movimiento').default,
        'numero_pasaje': IncipitMusical._meta.get_field('numero_pasaje').default,
        'voz_instrumento': IncipitMusical._meta.get_field('voz_instrumento').default,
    }
    
    context = {
        'tonalidades': TONALIDADES,
        'codigos_pais': CodigoPaisEntidad.CODIGOS_PAIS,
        'codigos_pais_json': codigos_pais_json,
        'codigos_idioma': CODIGOS_LENGUAJE,
        'codigos_idioma_json': codigos_idioma_json,
        'tipo_numero_editor': NumeroEditor.TIPO_NUMERO,
        'tipo_numero_editor_json': tipo_numero_editor_json,
        'control_nota_editor': NumeroEditor.CONTROL_NOTA,
        'control_nota_editor_json': control_nota_editor_json,
        'indicacion_traduccion': CodigoLengua.INDICACION_TRADUCCION,
        'indicacion_traduccion_json': indicacion_traduccion_json,
        'fuente_codigo': CodigoLengua.FUENTE_CODIGO,
        'fuente_codigo_json': fuente_codigo_json,
        'incipit_defaults': incipit_defaults,
    }
    return render(request, 'ObraGeneral/obra_general_modular.html', context)


def coleccion_manuscrita(request):
    """
    Vista para gestión de colecciones manuscritas
    
    Lista y gestiona obras musicales manuscritas catalogadas.
    """
    return render(request, 'ColeccionManuscrita/col_man.html')


def obra_individual_manuscrita(request):
    """
    Vista de detalle para obra manuscrita individual
    
    Muestra el detalle completo de una obra musical manuscrita.
    """
    return render(request, 'ColeccionManuscrita/obra_in_man.html')


def coleccion_impresa(request):
    """
    Vista para gestión de colecciones impresas
    
    Lista y gestiona obras musicales impresas catalogadas.
    """
    return render(request, 'ColeccionImpresa/col_imp.html')


def obra_individual_impresa(request):
    """
    Vista de detalle para obra impresa individual
    
    Muestra el detalle completo de una obra musical impresa.
    """
    return render(request, 'ColeccionImpresa/obra_in_imp.html')


def listar_obras(request):
    """
    Vista para listar todas las obras catalogadas
    
    Muestra un listado de todas las obras con información básica
    ordenadas por fecha de creación (más recientes primero).
    """
    obras = ObraGeneral.objects.all().select_related(
        'compositor',
        'titulo_uniforme',
        'titulo_240'
    ).order_by('-fecha_creacion_sistema')
    
    context = {
        'obras': obras,
        'total_obras': obras.count()
    }
    
    return render(request, 'ObraGeneral/listar_obras.html', context)
