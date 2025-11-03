"""
Vistas Base - Sistema de Catalogación MARC21 Musical
====================================================

Vistas generales de navegación y páginas principales.
No están relacionadas directamente con bloques MARC específicos.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse

from ..models import ObraGeneral
from ..models.obra_general import TONALIDADES

# Importar funciones de procesamiento desde sus módulos específicos
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


def crear_obra(request):
    """
    Vista para crear una nueva obra general
    
    Renderiza el formulario completo para catalogar una obra musical
    incluyendo cabecera, campos 0XX y 1XX con sus subcampos repetibles.
    
    Maneja tanto GET (mostrar formulario) como POST (guardar datos).
    """
    if request.method == 'POST':
        try:
            # Usar transacción atómica para garantizar integridad
            with transaction.atomic():
                # ========================================
                # PASO 1: Crear ObraGeneral (Cabecera)
                # ========================================
                obra = ObraGeneral()
                
                # Cabecera - Líder
                obra.tipo_registro = request.POST.get('tipo_registro', 'd')
                obra.nivel_bibliografico = request.POST.get('nivel_bibliografico', 'm')
                # num_control se autogenera en el save()
                
                # ========================================
                # PASO 2: Bloque 0XX - Campos no repetibles
                # ========================================
                
                # 040 - Fuente de catalogación
                obra.centro_catalogador = request.POST.get('centro_catalogador', 'UNL')
                
                # Guardar obra primero para tener el ID
                obra.save()
                
                # ========================================
                # PASO 3: Bloque 0XX - Campos repetibles
                # ========================================
                
                # 020 - ISBN (Repetible)
                procesar_isbn(request, obra)
                
                # 024 - ISMN (Repetible)
                procesar_ismn(request, obra)
                
                # 028 - Número de Editor (Repetible)
                procesar_numero_editor(request, obra)
                
                # 031 - Incipit Musical (Repetible con URLs anidadas)
                procesar_incipit(request, obra)
                
                # 041 - Código de Lengua (Repetible con idiomas anidados)
                procesar_codigo_lengua(request, obra)
                
                # 044 - Código de País (Repetible)
                procesar_codigo_pais(request, obra)
                
                # ========================================
                # PASO 4: Bloque 1XX - Compositor y Título Uniforme
                # ========================================
                
                # 100 - Compositor
                procesar_compositor(request, obra)
                
                # 130 - Título Uniforme (si no hay compositor)
                procesar_titulo_uniforme_130(request, obra)
                
                # 240 - Título Uniforme con Compositor
                procesar_titulo_uniforme_240(request, obra)
                
                # Regenerar clasificación 092 con los datos completos
                obra.generar_clasificacion_092()
                obra.save()
                
                messages.success(
                    request, 
                    f'✅ Obra creada exitosamente. Número de control: {obra.num_control}'
                )
                return redirect('crear_obra')
                
        except Exception as e:
            messages.error(request, f'❌ Error al guardar la obra: {str(e)}')
            return redirect('crear_obra')
    
    # GET - Mostrar formulario vacío
    context = {
        'tonalidades': TONALIDADES
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
