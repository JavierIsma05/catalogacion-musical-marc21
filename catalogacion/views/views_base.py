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
from django.http import JsonResponse
import json

# =========================
# 🔍 Depuración y modelos
# =========================
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

# =========================
# 🔧 Importación modular de vistas MARC
# =========================
from .views_0xx import (
    procesar_isbn, procesar_ismn, procesar_numero_editor,
    procesar_incipit, procesar_codigo_lengua, procesar_codigo_pais
)
from .views_1xx import (
    procesar_compositor, procesar_titulo_uniforme_130, procesar_titulo_uniforme_240
)
from .views_2xx import (
    procesar_titulo_alternativo, procesar_edicion, procesar_produccion_publicacion
)
from .views_3xx import (
    procesar_descripcion_fisica_300, procesar_medio_fisico_340,
    procesar_caracteristica_musica_348, procesar_medio_interpretacion_382,
    procesar_designacion_numerica_383
)
from .views_4xx import procesar_mencion_serie_490
from .views_5xx import (
    procesar_nota_general_500, procesar_contenido_505,
    procesar_sumario_520, procesar_datos_biograficos_545
)
from .views_6xx import procesar_materia_650, procesar_genero_forma_655
from .views_7xx import (
    procesar_nombre_relacionado_700, procesar_entidad_relacionada_710,
    procesar_enlace_fuente_773, procesar_enlace_unidad_774,
    procesar_otras_relaciones_787
)
from .views_8xx import procesar_ubicaciones_852, procesar_disponibles_856

logger = logging.getLogger(__name__)

# ======================================================
# 🏠 VISTAS GENERALES DE NAVEGACIÓN
# ======================================================

def index(request):
    """Página principal del sistema MARC21."""
    return render(request, 'index.html')


def plantillas(request):
    """Visualiza las plantillas MARC21 disponibles."""
    return render(request, 'plantillas.html')


# ======================================================
# 🎼 CREACIÓN DE OBRA GENERAL
# ======================================================

@transaction.atomic
def crear_obra(request):
    """Vista principal para crear una obra musical."""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                obra = ObraGeneral()
                obra.tipo_registro = request.POST.get('tipo_registro', 'd')
                obra.nivel_bibliografico = request.POST.get('nivel_bibliografico', 'm')
                obra.centro_catalogador = request.POST.get('centro_catalogador', 'UNL')
                obra.save()

                # ========================================
                # Bloques MARC21 (0XX → 8XX)
                # ========================================
                procesar_isbn(request, obra)
                procesar_ismn(request, obra)
                procesar_numero_editor(request, obra)
                procesar_incipit(request, obra)
                procesar_codigo_lengua(request, obra)
                procesar_codigo_pais(request, obra)

                procesar_compositor(request, obra)
                procesar_titulo_uniforme_130(request, obra)
                procesar_titulo_uniforme_240(request, obra)

                obra.titulo_principal = request.POST.get('titulo_principal', '')
                obra.subtitulo = request.POST.get('subtitulo', '')
                obra.mencion_responsabilidad = request.POST.get('mencion_responsabilidad', '')
                procesar_titulo_alternativo(request, obra)
                procesar_edicion(request, obra)
                procesar_produccion_publicacion(request, obra)

                procesar_descripcion_fisica_300(request, obra)
                procesar_medio_fisico_340(request, obra)
                procesar_caracteristica_musica_348(request, obra)
                procesar_medio_interpretacion_382(request, obra)
                procesar_designacion_numerica_383(request, obra)
                obra.tonalidad_384 = request.POST.get('tonalidad_384', '')

                procesar_mencion_serie_490(request, obra)
                procesar_nota_general_500(request, obra)
                procesar_contenido_505(request, obra)
                procesar_sumario_520(request, obra)
                procesar_datos_biograficos_545(request, obra)

                procesar_materia_650(request, obra)
                procesar_genero_forma_655(request, obra)

                procesar_nombre_relacionado_700(request, obra)
                procesar_entidad_relacionada_710(request, obra)
                procesar_enlace_fuente_773(request, obra)
                procesar_enlace_unidad_774(request, obra)
                procesar_otras_relaciones_787(request, obra)

                procesar_ubicaciones_852(request, obra)
                procesar_disponibles_856(request, obra)

                # ========================================
                # Guardado y depuración final
                # ========================================
                obra.generar_clasificacion_092()
                obra.save()

                # 👇 Imprimir estructura completa de la obra
                debug_obra_datos(obra)

                logger.info(f"✅ Obra '{obra.titulo_principal or 'Sin título'}' creada correctamente (ID: {obra.id})")
                messages.success(request, f'✅ Obra creada exitosamente. Número de control: {obra.num_control}')
                return redirect('crear_obra')

        # ======================================================
        # MANEJO DE ERRORES
        # ======================================================
        except ValidationError as ve:
            _log_error("ValidationError", ve)
            messages.error(request, f'❌ Error de validación: {str(ve)}')
        except IntegrityError as ie:
            _log_error("IntegrityError", ie)
            messages.error(request, f'❌ Error de integridad: {str(ie)}')
        except ValueError as ve:
            _log_error("ValueError", ve)
            messages.error(request, f'❌ Error de valor: {str(ve)}')
        except Exception as e:
            _log_error("Exception", e)
            messages.error(request, f'❌ Error al guardar la obra: {str(e)}')

        return redirect('crear_obra')

    # ========================================
    # GET - Mostrar formulario vacío
    # ========================================
    context = _generar_contexto_json()
    return render(request, 'ObraGeneral/obra_general_modular.html', context)


# ======================================================
# 🧩 FUNCIONES AUXILIARES
# ======================================================

def _log_error(tipo, ex):
    """Centraliza el manejo de errores y logs."""
    print("\n" + "❌" * 60)
    print(f"❌ ERROR ({tipo})")
    print("❌" * 60)
    print(f"\n🔴 Mensaje: {str(ex)}")
    print("\n🔗 Traceback completo:")
    print(traceback.format_exc())
    print("❌" * 60 + "\n")
    logger.exception(f"Error tipo {tipo}: {str(ex)}")


def _generar_contexto_json():
    """Genera el contexto para cargar en el template (solo para GET)."""
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

    incipit_defaults = {
        'numero_obra': IncipitMusical._meta.get_field('numero_obra').default,
        'numero_movimiento': IncipitMusical._meta.get_field('numero_movimiento').default,
        'numero_pasaje': IncipitMusical._meta.get_field('numero_pasaje').default,
        'voz_instrumento': IncipitMusical._meta.get_field('voz_instrumento').default,
    }

    return {
        'tonalidades': TONALIDADES,
        'codigos_pais_json': codigos_pais_json,
        'codigos_idioma_json': codigos_idioma_json,
        'tipo_numero_editor_json': tipo_numero_editor_json,
        'control_nota_editor_json': control_nota_editor_json,
        'indicacion_traduccion_json': indicacion_traduccion_json,
        'fuente_codigo_json': fuente_codigo_json,
        'incipit_defaults': incipit_defaults,
    }


# ======================================================
# 📂 VISTAS DE COLECCIONES Y LISTADOS
# ======================================================

def coleccion_manuscrita(request):
    return render(request, 'ColeccionManuscrita/col_man.html')

def obra_individual_manuscrita(request):
    return render(request, 'ColeccionManuscrita/obra_in_man.html')

def coleccion_impresa(request):
    return render(request, 'ColeccionImpresa/col_imp.html')

def obra_individual_impresa(request):
    return render(request, 'ColeccionImpresa/obra_in_imp.html')

def listar_obras(request):
    obras = ObraGeneral.objects.all().select_related(
        'compositor', 'titulo_uniforme', 'titulo_240'
    ).order_by('-fecha_creacion_sistema')
    context = {'obras': obras, 'total_obras': obras.count()}
    return render(request, 'ObraGeneral/listar_obras.html', context)

# ======================================================
# ⚙️ VISTAS DE ACCIONES SOBRE OBRAS
# ======================================================

from django.urls import reverse

# ============================================
# 👁 VER OBRA (solo lectura)
# ============================================
def ver_obra(request, obra_id):
    """
    Muestra los datos completos de una obra en modo solo lectura.
    Se utiliza para revisión o consulta sin permitir edición.
    """
    obra = get_object_or_404(ObraGeneral, id=obra_id)

    # Reutiliza relaciones si las tienes definidas
    contexto = {
        'obra': obra,
        'isbn': obra.isbns.all(),
        'ismn': obra.ismns.all(),
        'numero_editor': obra.numeros_editor.all(),
        'incipits': obra.incipits_musicales.all(),
        'codigo_lengua': obra.codigos_lengua.all(),
        'compositor': obra.compositor,
        'nombres_relacionados': obra.nombres_relacionados_700.all(),
        'entidades_relacionadas': obra.entidades_relacionadas_710.all(),
        'enlaces_773': obra.enlaces_documento_fuente_773.all(),
        'enlaces_774': obra.enlaces_unidades_774.all(),
        'otras_relaciones': obra.otras_relaciones_787.all(),
        'ubicaciones': obra.ubicaciones_852.all(),
        'recursos': obra.disponibles_856.all(),
    }

    return render(request, 'ObraGeneral/ver_obra.html', contexto)



def editar_obra(request, obra_id):
    """
    Permite editar los datos principales de una obra ya catalogada.
    (Prototipo inicial: solo para mostrar el flujo)
    """
    obra = get_object_or_404(ObraGeneral, id=obra_id)

    if request.method == 'POST':
        # En un futuro, aquí actualizaremos los bloques específicos.
        obra.titulo_principal = request.POST.get('titulo_principal', obra.titulo_principal)
        obra.subtitulo = request.POST.get('subtitulo', obra.subtitulo)
        obra.save()
        messages.success(request, '✅ Obra actualizada correctamente.')
        return redirect('listar_obras')

    return render(request, 'ObraGeneral/obra_general_modular.html', {'obra': obra})


def eliminar_obra(request, obra_id):
    """
    Elimina una obra y todas sus relaciones dependientes (seguro y reversible).
    """
    obra = get_object_or_404(ObraGeneral, id=obra_id)

    if request.method == 'POST':
        try:
            obra.delete()
            messages.success(request, f'🗑️ Obra {obra.num_control} eliminada correctamente.')
            return redirect('listar_obras')
        except Exception as e:
            logger.exception("Error al eliminar obra")
            messages.error(request, f'❌ No se pudo eliminar la obra: {str(e)}')
            return redirect('listar_obras')

    return render(request, 'ObraGeneral/confirmar_eliminar.html', {'obra': obra})
