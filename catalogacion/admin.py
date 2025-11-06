"""
Admin unificado para modelos MARC21
====================================

Configuración completa del Django admin para toda la ficha MARC21
con soporte para campos repetibles, subcampos repetibles e inlines anidados.

Estructura de inlines:
- TabularInline: para campos simples y repetibles
- StackedInline: para contenedores principales
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from catalogacion.models.autoridades import AutoridadEntidad

# Importar todos los modelos
from .models import (
    # ObraGeneral
    ObraGeneral,
    # Bloque 0XX
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    # Bloque 1XX
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
    # Bloque 2XX
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    # Bloque 3XX
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
    # Bloque 4XX
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
    # Bloque 5XX
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
    # Bloque 6XX
    Materia650, 
    SubdivisionMateria650,
    MateriaGenero655, 
    SubdivisionGeneral655,
    # Bloque 7XX
    NombreRelacionado700, 
    TerminoAsociado700, 
    Funcion700,
    Relacion700, 
    Autoria700, 
    EntidadRelacionada710,
    EnlaceDocumentoFuente773, 
    EnlaceUnidadConstituyente774, 
    OtrasRelaciones787,
    # Bloque 8XX
    Ubicacion852, 
    Estanteria852, 
    Disponible856,

)

# ================================================
# 🔧 INLINES PARA BLOQUE 1XX - Puntos de acceso
# ================================================

class FuncionCompositorInline(admin.TabularInline):
    """100 $e - Funciones del compositor (R)"""
    model = FuncionCompositor
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['funcion']
    verbose_name = "Función"
    verbose_name_plural = "✏️ Funciones Compositor (100 $e - R)"


class AtribucionCompositorInline(admin.TabularInline):
    """100 $j - Atribuciones del compositor (R)"""
    model = AtribucionCompositor
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['atribucion']
    verbose_name = "Atribución"
    verbose_name_plural = "🏷️ Atribuciones Compositor (100 $j - R)"


class Forma130Inline(admin.TabularInline):
    """130 $k - Formas (R)"""
    model = Forma130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['forma']
    verbose_name = "Forma"
    verbose_name_plural = "📋 Formas (130 $k - R)"


class MedioInterpretacion130Inline(admin.TabularInline):
    """130 $m - Medios (R)"""
    model = MedioInterpretacion130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['medio']
    verbose_name = "Medio"
    verbose_name_plural = "🎵 Medios de Interpretación (130 $m - R)"


class NumeroParteSección130Inline(admin.TabularInline):
    """130 $n - Números de parte (R)"""
    model = NumeroParteSección130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Número"
    verbose_name_plural = "🔢 Números de Parte/Sección (130 $n - R)"


class NombreParteSección130Inline(admin.TabularInline):
    """130 $p - Nombres de parte (R)"""
    model = NombreParteSección130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['nombre']
    verbose_name = "Nombre"
    verbose_name_plural = "📝 Nombres de Parte/Sección (130 $p - R)"


class Forma240Inline(admin.TabularInline):
    """240 $k - Formas (R)"""
    model = Forma240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['forma']
    verbose_name = "Forma"
    verbose_name_plural = "📋 Formas (240 $k - R)"


class MedioInterpretacion240Inline(admin.TabularInline):
    """240 $m - Medios (R)"""
    model = MedioInterpretacion240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['medio']
    verbose_name = "Medio"
    verbose_name_plural = "🎵 Medios de Interpretación (240 $m - R)"


class NumeroParteSección240Inline(admin.TabularInline):
    """240 $n - Números de parte (R)"""
    model = NumeroParteSección240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Número"
    verbose_name_plural = "🔢 Números de Parte/Sección (240 $n - R)"


class NombreParteSección240Inline(admin.TabularInline):
    """240 $p - Nombres de parte (R)"""
    model = NombreParteSección240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['nombre']
    verbose_name = "Nombre"
    verbose_name_plural = "📝 Nombres de Parte/Sección (240 $p - R)"


# ================================================
# 🔧 INLINES PARA BLOQUE 2XX - Títulos y publicación
# ================================================

class TituloAlternativoInline(admin.TabularInline):
    """246 - Títulos alternativos (R)"""
    model = TituloAlternativo
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['titulo', 'resto_titulo']
    verbose_name = "Título Alternativo"
    verbose_name_plural = "🔤 Títulos Alternativos (246 - R)"


class EdicionInline(admin.TabularInline):
    """250 - Ediciones (R)"""
    model = Edicion
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['edicion']
    verbose_name = "Edición"
    verbose_name_plural = "📖 Ediciones (250 - R)"


class ProduccionPublicacionInline(admin.TabularInline):
    """264 - Producción/Publicación (R) - LIGADOS"""
    model = ProduccionPublicacion
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['funcion', 'lugar', 'nombre_entidad', 'fecha']
    verbose_name = "Producción/Publicación"
    verbose_name_plural = "🏭 Producciones/Publicaciones (264 - R, LIGADOS)"
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 264 es COMPLETAMENTE REPETIBLE. "
            "Los subcampos $a (lugar), $b (entidad), $c (fecha) están LIGADOS. "
            "Cada fila es una instancia de 264 con su función."
        )
        return formset


# ================================================
# 🔧 INLINES PARA BLOQUE 3XX - Descripción física
# ================================================

class Extension300Inline(admin.TabularInline):
    """300 $a - Extensiones (R) - ANIDADO"""
    model = Extension300
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['extension']
    verbose_name = "Extensión"
    verbose_name_plural = "✏️ Extensiones (300 $a - R)"


class Dimension300Inline(admin.TabularInline):
    """300 $c - Dimensiones (R) - ANIDADO"""
    model = Dimension300
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['dimension']
    verbose_name = "Dimensión"
    verbose_name_plural = "📏 Dimensiones (300 $c - R)"


class DescripcionFisicaInline(admin.StackedInline):
    """300 - Descripción física (R) - PRINCIPAL"""
    model = DescripcionFisica
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [Extension300Inline, Dimension300Inline]
    fields = ['otras_caracteristicas_fisicas', 'material_acompanante']
    verbose_name = "Descripción Física"
    verbose_name_plural = "📚 Descripciones Físicas (300 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 300 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 300, los subcampos $a (extensión) y $c (dimensión) "
            "también son REPETIBLES. Agregue múltiples para cada categoría."
        )
        return formset


class Tecnica340Inline(admin.TabularInline):
    """340 $d - Técnicas (R) - ANIDADO"""
    model = Tecnica340
    extra = 1
    min_num = 1
    max_num = 10
    
    fields = ['tecnica']
    verbose_name = "Técnica"
    verbose_name_plural = "✏️ Técnicas (340 $d - R)"


class MedioFisicoInline(admin.StackedInline):
    """340 - Medio físico (R) - PRINCIPAL"""
    model = MedioFisico
    extra = 1
    min_num = 0
    max_num = 5
    
    inlines = [Tecnica340Inline]
    verbose_name = "Medio Físico"
    verbose_name_plural = "📀 Medios Físicos (340 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 340 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 340, el subcampo $d (técnica) también es REPETIBLE. "
            "Se autogenera basado en tipo_registro. Agregue múltiples técnicas."
        )
        return formset


class Formato348Inline(admin.TabularInline):
    """348 $a - Formatos (R) - ANIDADO"""
    model = Formato348
    extra = 1
    min_num = 1
    max_num = 10
    
    fields = ['formato']
    verbose_name = "Formato"
    verbose_name_plural = "✏️ Formatos (348 $a - R)"


class CaracteristicaMusicaNotadaInline(admin.StackedInline):
    """348 - Características música notada (R) - PRINCIPAL"""
    model = CaracteristicaMusicaNotada
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [Formato348Inline]
    verbose_name = "Característica Música Notada"
    verbose_name_plural = "🎼 Características Música Notada (348 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 348 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 348, $a (formato) también es REPETIBLE. "
            "NO use si la música es para piano en doble pauta tradicional."
        )
        return formset


class MedioInterpretacion382_aInline(admin.TabularInline):
    """382 $a - Medios (R) - ANIDADO"""
    model = MedioInterpretacion382_a
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['medio']
    verbose_name = "Medio"
    verbose_name_plural = "🎵 Medios (382 $a - R)"


class Solista382Inline(admin.TabularInline):
    """382 $b - Solistas (R) - ANIDADO"""
    model = Solista382
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['solista']
    verbose_name = "Solista"
    verbose_name_plural = "🎤 Solistas (382 $b - R)"


class NumeroInterpretes382Inline(admin.TabularInline):
    """382 $n - Números (R) - ANIDADO"""
    model = NumeroInterpretes382
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Número"
    verbose_name_plural = "👥 Números Intérpretes (382 $n - R)"


class MedioInterpretacion382Inline(admin.StackedInline):
    """382 - Medio de interpretación (R) - PRINCIPAL"""
    model = MedioInterpretacion382
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [
        MedioInterpretacion382_aInline,
        Solista382Inline,
        NumeroInterpretes382Inline
    ]
    verbose_name = "Medio de Interpretación"
    verbose_name_plural = "🎼 Medios de Interpretación (382 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 382 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 382, $a (medios), $b (solistas), $n (cantidad) "
            "son todos REPETIBLES e INDEPENDIENTES."
        )
        return formset


class NumeroObra383Inline(admin.TabularInline):
    """383 $a - Números (R) - ANIDADO"""
    model = NumeroObra383
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero_obra']
    verbose_name = "Número"
    verbose_name_plural = "🔢 Números de Obra (383 $a - R)"


class Opus383Inline(admin.TabularInline):
    """383 $b - Opus (R) - ANIDADO"""
    model = Opus383
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['opus']
    verbose_name = "Opus"
    verbose_name_plural = "♯ Opus (383 $b - R)"


class DesignacionNumericaObraInline(admin.StackedInline):
    """383 - Designación numérica (R) - PRINCIPAL"""
    model = DesignacionNumericaObra
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [NumeroObra383Inline, Opus383Inline]
    verbose_name = "Designación Numérica"
    verbose_name_plural = "🔢 Designaciones Numéricas (383 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 383 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 383, $a (número) y $b (opus) son REPETIBLES e INDEPENDIENTES."
        )
        return formset


# ================================================
# 🔧 INLINES PARA BLOQUE 4XX - Series
# ================================================

class TituloSerie490Inline(admin.TabularInline):
    """490 $a - Títulos (R) - ANIDADO"""
    model = TituloSerie490
    extra = 1
    min_num = 1
    max_num = 10
    
    fields = ['titulo_serie']
    verbose_name = "Título"
    verbose_name_plural = "📚 Títulos de Serie (490 $a - R)"


class VolumenSerie490Inline(admin.TabularInline):
    """490 $v - Volúmenes (R) - ANIDADO"""
    model = VolumenSerie490
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['volumen']
    verbose_name = "Volumen"
    verbose_name_plural = "📖 Volúmenes (490 $v - R)"


class MencionSerie490Inline(admin.StackedInline):
    """490 - Mención de serie (R) - PRINCIPAL"""
    model = MencionSerie490
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [TituloSerie490Inline, VolumenSerie490Inline]
    fields = ['relacion']
    verbose_name = "Mención de Serie"
    verbose_name_plural = "📚 Menciones de Serie (490 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 490 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 490, $a (título) y $v (volumen) son REPETIBLES. "
            "Primer indicador: 0=no relacionado, 1=relacionado con 800-830."
        )
        return formset

# =====================================================
# 🗒️ BLOQUE 5XX – Notas y descripciones
# =====================================================

# -------------------------------
# 500 ## Nota general (R)
# -------------------------------
class NotaGeneral500Inline(admin.StackedInline):
    """500 ## Nota general (R)"""
    model = NotaGeneral500
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['nota_general']
    verbose_name = "Nota general"
    verbose_name_plural = "🗒️ Notas generales (500 - R)"
    classes = ['collapse']


# -------------------------------
# 505 00 Contenido (R)
# -------------------------------
class Contenido505Inline(admin.StackedInline):
    """505 00 Contenido (R)"""
    model = Contenido505
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['contenido']
    verbose_name = "Contenido"
    verbose_name_plural = "📄 Contenidos (505 - R)"
    classes = ['collapse']


# -------------------------------
# 520 ## Sumario (R)
# -------------------------------
class Sumario520Inline(admin.StackedInline):
    """520 ## Sumario (R)"""
    model = Sumario520
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['sumario']
    verbose_name = "Sumario"
    verbose_name_plural = "📘 Sumarios (520 - R)"
    classes = ['collapse']


# -------------------------------
# 545 0# Datos biográficos del compositor (R)
# -------------------------------
class DatosBiograficos545Inline(admin.StackedInline):
    """545 0# Datos biográficos del compositor (R)"""
    model = DatosBiograficos545
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['datos_biograficos', 'url']
    verbose_name = "Datos biográficos del compositor"
    verbose_name_plural = "🎼 Datos biográficos del compositor (545 - R)"
    classes = ['collapse']

# ============================================================
# BLOQUE 6XX - MATERIAS
# ============================================================

# 650 – Materia (Temas)
class SubdivisionMateria650Inline(admin.TabularInline):
    model = SubdivisionMateria650
    extra = 1
    verbose_name = "Subdivisión de materia"
    verbose_name_plural = "Subdivisiones ($x)"


class Materia650Inline(admin.StackedInline):
    model = Materia650
    extra = 1
    verbose_name = "Materia (Tema)"
    verbose_name_plural = "Materias (650)"
    inlines = [SubdivisionMateria650Inline]


# 655 – Materia (Género/Forma)
class SubdivisionGeneral655Inline(admin.TabularInline):
    model = SubdivisionGeneral655
    extra = 1
    verbose_name = "Subdivisión general"
    verbose_name_plural = "Subdivisiones ($x)"


class MateriaGenero655Inline(admin.StackedInline):
    model = MateriaGenero655
    extra = 1
    verbose_name = "Materia (Género/Forma)"
    verbose_name_plural = "Materias (655)"
    inlines = [SubdivisionGeneral655Inline]


# =====================================================
# 🟣 BLOQUE 7XX – Accesos adicionales y relaciones
# =====================================================

# --- Subcampos del 700 ---
class TerminoAsociado700Inline(admin.TabularInline):
    """700 $c – Término asociado al nombre (R)"""
    model = TerminoAsociado700
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['termino']
    verbose_name = "Término asociado"
    verbose_name_plural = "🧩 Términos asociados (700 $c - R)"


class Funcion700Inline(admin.TabularInline):
    """700 $e – Función (R)"""
    model = Funcion700
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['funcion']
    verbose_name = "Función"
    verbose_name_plural = "🎶 Funciones (700 $e - R)"


class Relacion700Inline(admin.TabularInline):
    """700 $i – Relación (R)"""
    model = Relacion700
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['descripcion']
    verbose_name = "Relación"
    verbose_name_plural = "🔗 Relaciones (700 $i - R)"


class Autoria700Inline(admin.TabularInline):
    """700 $j – Autoría (R)"""
    model = Autoria700
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['autoria']
    verbose_name = "Autoría"
    verbose_name_plural = "📜 Autorías (700 $j - R)"


class NombreRelacionado700Inline(admin.StackedInline):
    """700 1# – Nombre relacionado (R)"""
    model = NombreRelacionado700
    autocomplete_fields = ['persona']
    extra = 1
    min_num = 0
    max_num = 10

    # ✅ $d se rellena automáticamente desde AutoridadPersona
    readonly_fields = ['fechas']  
    fields = ['persona', 'fechas', 'titulo_obra']

    verbose_name = "Nombre relacionado"
    verbose_name_plural = "🧑‍🎤 Nombres relacionados (700 - R)"

    inlines = [
        TerminoAsociado700Inline,
        Funcion700Inline,
        Relacion700Inline,
        Autoria700Inline,
    ]

    class Media:
        # ✅ Asegúrate de que esta ruta coincida con tu carpeta "static/catalogacion/js/"
        js = ('catalogacion/js/auto_fecha_persona.js',)


# --- Subcampos del 710 ---
class EntidadRelacionada710Inline(admin.StackedInline):
    """710 2# – Entidad relacionada (R)"""
    model = EntidadRelacionada710
    autocomplete_fields = ['entidad']
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['entidad', 'funcion']
    verbose_name = "Entidad relacionada"
    verbose_name_plural = "🏛️ Entidades relacionadas (710 - R)"


# --- Enlaces entre obras ---
class EnlaceDocumentoFuente773Inline(admin.StackedInline):
    """773 1# – Enlace a documento fuente (R)"""
    model = EnlaceDocumentoFuente773
    autocomplete_fields = ['encabezamiento_principal']
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['encabezamiento_principal', 'titulo', 'numero_obra_relacionada']
    verbose_name = "Documento fuente"
    verbose_name_plural = "📘 Documentos fuente (773 - R)"


class EnlaceUnidadConstituyente774Inline(admin.StackedInline):
    """774 1# – Enlace a unidad constituyente (R)"""
    model = EnlaceUnidadConstituyente774
    autocomplete_fields = ['encabezamiento_principal']
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['encabezamiento_principal', 'titulo', 'numero_obra_relacionada']
    verbose_name = "Unidad constituyente"
    verbose_name_plural = "📚 Unidades constituyentes (774 - R)"


class OtrasRelaciones787Inline(admin.StackedInline):
    """787 1# – Otras relaciones (R)"""
    model = OtrasRelaciones787
    autocomplete_fields = ['encabezamiento_principal']
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['encabezamiento_principal', 'titulo', 'numero_obra_relacionada']
    verbose_name = "Otra relación"
    verbose_name_plural = "🔗 Otras relaciones (787 - R)"


# ============================================================
# 📦 BLOQUE 8XX – ADMIN COMPLETO Y CORREGIDO
# ============================================================

class Estanteria852Inline(admin.TabularInline):
    """Subcampo repetible $c – Estantería"""
    model = Estanteria852
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['estanteria']
    verbose_name = "Estantería ($c)"
    verbose_name_plural = "📚 Estanterías ($c)"


class Ubicacion852Inline(admin.StackedInline):
    """Bloque 852 ## – Ubicación (R)"""
    model = Ubicacion852
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['institucion_persona', 'signatura_original']
    inlines = [Estanteria852Inline]  # 👈 Aquí se anidan las estanterías
    verbose_name = "Ubicación (852)"
    verbose_name_plural = "📍 Ubicaciones (852)"
    show_change_link = True


class Disponible856Inline(admin.StackedInline):
    """Bloque 856 4# – Disponible (R)"""
    model = Disponible856
    extra = 1
    min_num = 0
    max_num = 10
    fields = ['url', 'texto_enlace']
    verbose_name = "Recurso disponible (856)"
    verbose_name_plural = "🌐 Recursos disponibles (856)"
    show_change_link = True




# ================================================
# 🎯 ADMIN PRINCIPAL - ObraGeneral
# ================================================

@admin.register(ObraGeneral)
class ObraGeneralAdmin(admin.ModelAdmin):
    """
    Admin principal para ObraGeneral
    Integra todos los campos MARC21 en una ficha completa
    """
    
    list_display = [
        'num_control',
        'titulo_principal_corto',
        'compositor_display',
        'tipo_registro_display',
        'fecha_creacion_sistema'
    ]
    
    list_filter = [
        'tipo_registro',
        'nivel_bibliografico',
        'fecha_creacion_sistema',
    ]
    
    search_fields = [
        'num_control',
        'titulo_principal',
        'compositor__apellidos_nombres'
    ]
    
    readonly_fields = [
        'num_control',
        'estado_registro',
        'fecha_hora_ultima_transaccion',
        'codigo_informacion',
        'clasif_institucion',
        'clasif_proyecto',
        'clasif_pais',
        'clasif_ms_imp',
        'clasif_num_control',
        'fecha_creacion_sistema',
        'fecha_modificacion_sistema',
        'signatura_display'
    ]
    
    fieldsets = (
        ('🔑 CABECERA Y CONTROL', {
            'fields': (
                'num_control',
                'tipo_registro',
                'nivel_bibliografico',
                'estado_registro',
                'fecha_hora_ultima_transaccion',
                'codigo_informacion',
            ),
            'classes': ('collapse',)
        }),
        
        ('🏢 CLASIFICACIÓN LOCAL (092)', {
            'fields': (
                'centro_catalogador',
                'signatura_display',
                'clasif_institucion',
                'clasif_proyecto',
                'clasif_pais',
                'clasif_ms_imp',
                'clasif_num_control',
            ),
            'classes': ('collapse',)
        }),
        
        ('👤 BLOQUE 1XX - PUNTOS DE ACCESO PRINCIPALES', {
            'fields': (
                'compositor',
                'titulo_uniforme',
                'titulo_uniforme_tonalidad',
                'titulo_uniforme_arreglo',
                'titulo_240',
                'titulo_240_tonalidad',
                'titulo_240_arreglo',
            ),
            'description': (
                '⚠️ REGLA: Si hay compositor (100), use campo 240. '
                'Si NO hay compositor, use campo 130. '
                'Debe haber al menos uno de estos puntos de acceso.'
            ),
            'classes': ('wide',)
        }),
        
        ('📖 BLOQUE 2XX - TÍTULOS Y PUBLICACIÓN', {
            'fields': (
                'titulo_principal',
                'subtitulo',
                'mencion_responsabilidad',
            ),
            'description': 'Campo 245 - Mención de título (obligatorio)'
        }),
        
        ('🎵 BLOQUE 3XX - DESCRIPCIÓN FÍSICA Y CARACTERÍSTICAS', {
            'fields': ('tonalidad_384',),
            'description': (
                'Campo 384 - Tonalidad (NR). '
                'Resto de campos 3XX se gestionan en inlines.'
            ),
            'classes': ('wide',)
        }),
        
        ('📅 METADATOS DEL SISTEMA', {
            'fields': (
                'fecha_creacion_sistema',
                'fecha_modificacion_sistema',
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        # Bloque 1XX
        FuncionCompositorInline,
        AtribucionCompositorInline,
        Forma130Inline,
        MedioInterpretacion130Inline,
        NumeroParteSección130Inline,
        NombreParteSección130Inline,
        Forma240Inline,
        MedioInterpretacion240Inline,
        NumeroParteSección240Inline,
        NombreParteSección240Inline,
        
        # Bloque 2XX
        TituloAlternativoInline,
        EdicionInline,
        ProduccionPublicacionInline,
        
        # Bloque 3XX
        DescripcionFisicaInline,
        MedioFisicoInline,
        CaracteristicaMusicaNotadaInline,
        MedioInterpretacion382Inline,
        DesignacionNumericaObraInline,
        
        # Bloque 4XX
        MencionSerie490Inline,
        # Bloque 5XX
        NotaGeneral500Inline,
        Contenido505Inline,
        Sumario520Inline,
        DatosBiograficos545Inline,
        # Bloque 6XX
        Materia650Inline,
        MateriaGenero655Inline,
        # Bloque 7XX
        NombreRelacionado700Inline,
        EntidadRelacionada710Inline,
        EnlaceDocumentoFuente773Inline,
        EnlaceUnidadConstituyente774Inline,
        OtrasRelaciones787Inline,
        # Bloque 8XX
        Ubicacion852Inline,     # 852 completo (con estanterías)
        Disponible856Inline,    # 856 URLs

        
        
    ]
    list_display = ('titulo_principal', 'nivel_bibliografico')
    
    # Métodos de visualización
    def titulo_principal_corto(self, obj):
        """Mostrar título principal acortado"""
        titulo = obj.titulo_principal or '(sin título)'
        if len(titulo) > 50:
            return f"{titulo[:47]}..."
        return titulo
    titulo_principal_corto.short_description = "Título"
    
    def compositor_display(self, obj):
        """Mostrar compositor con enlace"""
        if obj.compositor:
            return format_html(
                '<strong>{}</strong>',
                obj.compositor.apellidos_nombres
            )
        return format_html('<em>Anónimo</em>')
    compositor_display.short_description = "Compositor"
    
    def tipo_registro_display(self, obj):
        """Mostrar tipo de registro con etiqueta"""
        tipos = {'c': '📄 Impreso', 'd': '✍️ Manuscrito'}
        etiqueta = tipos.get(obj.tipo_registro, 'Desconocido')
        color = '#00AA00' if obj.tipo_registro == 'd' else '#0000AA'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            etiqueta
        )
    tipo_registro_display.short_description = "Tipo"
    
    def signatura_display(self, obj):
        """Mostrar signatura completa"""
        return format_html(
            '<code style="background: #f0f0f0; padding: 5px; border-radius: 3px;">{}</code>',
            obj.get_signatura_completa()
        )
    signatura_display.short_description = "Signatura Completa"
    
    # Acciones personalizadas
    actions = ['generar_clasificacion_accion']
    
    def generar_clasificacion_accion(self, request, queryset):
        """Acción para regenerar clasificación 092"""
        updated = 0
        for obra in queryset:
            obra.generar_clasificacion_092()
            obra.save()
            updated += 1
        
        self.message_user(
            request,
            f'{updated} obra(s) clasificada(s) correctamente.'
        )
    generar_clasificacion_accion.short_description = "♻️ Regenerar clasificación (092)"
    
    # Métodos de validación
    def save_model(self, request, obj, form, change):
        """Guardar modelo con validaciones"""
        try:
            obj.full_clean()
        except Exception as e:
            from django.contrib.admin import display
            self.message_user(request, f'⚠️ {str(e)}', level='ERROR')
            return
        
        super().save_model(request, obj, form, change)
        self.message_user(request, '✅ Obra guardada correctamente.')


# ================================================
# REGISTROS DE MODELOS AUXILIARES
# ================================================

@admin.register(AutoridadPersona)
class AutoridadPersonaAdmin(admin.ModelAdmin):
    """Admin para autoridades de personas"""
    list_display = ['apellidos_nombres', 'fechas']
    search_fields = ['apellidos_nombres']
    list_filter = ['fechas']


@admin.register(AutoridadTituloUniforme)
class AutoridadTituloUniformeAdmin(admin.ModelAdmin):
    """Admin para títulos uniformes"""
    list_display = ['titulo']
    search_fields = ['titulo']


@admin.register(AutoridadFormaMusical)
class AutoridadFormaMusicalAdmin(admin.ModelAdmin):
    """Admin para formas musicales"""
    list_display = ['forma']
    search_fields = ['forma']

@admin.register(AutoridadEntidad)
class AutoridadEntidadAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'pais', 'descripcion']
    list_display = ['nombre', 'pais']
