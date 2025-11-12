"""
Admin unificado para modelos MARC21
====================================

Configuracion completa del Django admin para toda la ficha MARC21
con soporte para campos repetibles, subcampos repetibles e inlines anidados.

Estructura de inlines:
- TabularInline: para campos simples y repetibles
- StackedInline: para contenedores principales
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

# Importar todos los modelos
from .models import (
    # ObraGeneral
    ObraGeneral,
    # Bloque 0XX
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadEntidad,
    # Bloque 1XX
    FuncionCompositor,
    AtribucionCompositor,
    Forma130,
    MedioInterpretacion130,
    NumeroParteSeccion130,
    NombreParteSeccion130,
    Forma240,
    MedioInterpretacion240,
    NumeroParteSeccion240,
    NombreParteSeccion240,
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
    NotaContenido505,
    NotaBiografica545,

    # Bloque 6XX
    Materia650,
    MateriaGenero655,

    # Bloque 7XX
    Relacion700,
    Autoria700,
    FuncionEntidad710,
    NumeroDocumentoRelacionado773,
    NumeroObraRelacionada774,
    NumeroObraRelacionada787,
  
    # Bloque 8XX
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
    verbose_name = "Funcion"
    verbose_name_plural = "✏️ Funciones Compositor (100 $e - R)"


class AtribucionCompositorInline(admin.TabularInline):
    """100 $j - Atribuciones del compositor (R)"""
    model = AtribucionCompositor
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['atribucion']
    verbose_name = "Atribucion"
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
    verbose_name_plural = "🎵 Medios de Interpretacion (130 $m - R)"


class NumeroParteSeccion130Inline(admin.TabularInline):
    """130 $n - Numeros de parte (R)"""
    model = NumeroParteSeccion130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Numero"
    verbose_name_plural = "🔢 Numeros de Parte/Seccion (130 $n - R)"


class NombreParteSeccion130Inline(admin.TabularInline):
    """130 $p - Nombres de parte (R)"""
    model = NombreParteSeccion130
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['nombre']
    verbose_name = "Nombre"
    verbose_name_plural = "📝 Nombres de Parte/Seccion (130 $p - R)"


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
    verbose_name_plural = "🎵 Medios de Interpretacion (240 $m - R)"


class NumeroParteSeccion240Inline(admin.TabularInline):
    """240 $n - Numeros de parte (R)"""
    model = NumeroParteSeccion240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Numero"
    verbose_name_plural = "🔢 Numeros de Parte/Seccion (240 $n - R)"


class NombreParteSeccion240Inline(admin.TabularInline):
    """240 $p - Nombres de parte (R)"""
    model = NombreParteSeccion240
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['nombre']
    verbose_name = "Nombre"
    verbose_name_plural = "📝 Nombres de Parte/Seccion (240 $p - R)"


# ================================================
# 🔧 INLINES PARA BLOQUE 2XX - Titulos y publicacion
# ================================================

class TituloAlternativoInline(admin.TabularInline):
    """246 - Titulos alternativos (R)"""
    model = TituloAlternativo
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['titulo', 'resto_titulo']
    verbose_name = "Titulo Alternativo"
    verbose_name_plural = "🔤 Titulos Alternativos (246 - R)"


class EdicionInline(admin.TabularInline):
    """250 - Ediciones (R)"""
    model = Edicion
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['edicion']
    verbose_name = "Edicion"
    verbose_name_plural = "📖 Ediciones (250 - R)"


class ProduccionPublicacionInline(admin.TabularInline):
    """264 - Produccion/Publicacion (R) - LIGADOS"""
    model = ProduccionPublicacion
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['funcion', 'lugar', 'nombre_entidad', 'fecha']
    verbose_name = "Produccion/Publicacion"
    verbose_name_plural = "🏭 Producciones/Publicaciones (264 - R, LIGADOS)"
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 264 es COMPLETAMENTE REPETIBLE. "
            "Los subcampos $a (lugar), $b (entidad), $c (fecha) estan LIGADOS. "
            "Cada fila es una instancia de 264 con su funcion."
        )
        return formset


# ================================================
# 🔧 INLINES PARA BLOQUE 3XX - Descripcion fisica
# ================================================

class Extension300Inline(admin.TabularInline):
    """300 $a - Extensiones (R) - ANIDADO"""
    model = Extension300
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['extension']
    verbose_name = "Extension"
    verbose_name_plural = "✏️ Extensiones (300 $a - R)"


class Dimension300Inline(admin.TabularInline):
    """300 $c - Dimensiones (R) - ANIDADO"""
    model = Dimension300
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['dimension']
    verbose_name = "Dimension"
    verbose_name_plural = "📏 Dimensiones (300 $c - R)"


class DescripcionFisicaInline(admin.StackedInline):
    """300 - Descripcion fisica (R) - PRINCIPAL"""
    model = DescripcionFisica
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [Extension300Inline, Dimension300Inline]
    fields = ['otras_caracteristicas_fisicas', 'material_acompanante']
    verbose_name = "Descripcion Fisica"
    verbose_name_plural = "📚 Descripciones Fisicas (300 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 300 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 300, los subcampos $a (extension) y $c (dimension) "
            "también son REPETIBLES. Agregue multiples para cada categoria."
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
    """340 - Medio fisico (R) - PRINCIPAL"""
    model = MedioFisico
    extra = 1
    min_num = 0
    max_num = 5
    
    inlines = [Tecnica340Inline]
    verbose_name = "Medio Fisico"
    verbose_name_plural = "📀 Medios Fisicos (340 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 340 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 340, el subcampo $d (técnica) también es REPETIBLE. "
            "Se autogenera basado en tipo_registro. Agregue multiples técnicas."
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
    """348 - Caracteristicas musica notada (R) - PRINCIPAL"""
    model = CaracteristicaMusicaNotada
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [Formato348Inline]
    verbose_name = "Caracteristica Musica Notada"
    verbose_name_plural = "🎼 Caracteristicas Musica Notada (348 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 348 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 348, $a (formato) también es REPETIBLE. "
            "NO use si la musica es para piano en doble pauta tradicional."
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
    """382 $n - Numeros (R) - ANIDADO"""
    model = NumeroInterpretes382
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero']
    verbose_name = "Numero"
    verbose_name_plural = "👥 Numeros Intérpretes (382 $n - R)"


class MedioInterpretacion382Inline(admin.StackedInline):
    """382 - Medio de interpretacion (R) - PRINCIPAL"""
    model = MedioInterpretacion382
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [
        MedioInterpretacion382_aInline,
        Solista382Inline,
        NumeroInterpretes382Inline
    ]
    verbose_name = "Medio de Interpretacion"
    verbose_name_plural = "🎼 Medios de Interpretacion (382 - R)"
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
    """383 $a - Numeros (R) - ANIDADO"""
    model = NumeroObra383
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['numero_obra']
    verbose_name = "Numero"
    verbose_name_plural = "🔢 Numeros de Obra (383 $a - R)"


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
    """383 - Designacion numérica (R) - PRINCIPAL"""
    model = DesignacionNumericaObra
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [NumeroObra383Inline, Opus383Inline]
    verbose_name = "Designacion Numérica"
    verbose_name_plural = "🔢 Designaciones Numéricas (383 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 383 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 383, $a (numero) y $b (opus) son REPETIBLES e INDEPENDIENTES."
        )
        return formset


# ================================================
# 🔧 INLINES PARA BLOQUE 4XX - Series
# ================================================

class TituloSerie490Inline(admin.TabularInline):
    """490 $a - Titulos (R) - ANIDADO"""
    model = TituloSerie490
    extra = 1
    min_num = 1
    max_num = 10
    
    fields = ['titulo_serie']
    verbose_name = "Titulo"
    verbose_name_plural = "📚 Titulos de Serie (490 $a - R)"


class VolumenSerie490Inline(admin.TabularInline):
    """490 $v - Volumenes (R) - ANIDADO"""
    model = VolumenSerie490
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['volumen']
    verbose_name = "Volumen"
    verbose_name_plural = "📖 Volumenes (490 $v - R)"


class MencionSerie490Inline(admin.StackedInline):
    """490 - Mencion de serie (R) - PRINCIPAL"""
    model = MencionSerie490
    extra = 1
    min_num = 0
    max_num = 10
    
    inlines = [TituloSerie490Inline, VolumenSerie490Inline]
    fields = ['relacion']
    verbose_name = "Mencion de Serie"
    verbose_name_plural = "📚 Menciones de Serie (490 - R)"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 490 es COMPLETAMENTE REPETIBLE. "
            "Dentro de cada 490, $a (titulo) y $v (volumen) son REPETIBLES. "
            "Primer indicador: 0=no relacionado, 1=relacionado con 800-830."
        )
        return formset
# =====================================================
# 🔧 INLINES BLOQUE 5XX – Notas y contenido
# =====================================================
class NotaGeneral500Inline(admin.TabularInline):
    model = NotaGeneral500
    extra = 1
    fields = ['texto']
    verbose_name = "500 Nota general"
    verbose_name_plural = "📝 500 Notas generales (R)"


class NotaContenido505Inline(admin.TabularInline):
    model = NotaContenido505
    extra = 1
    fields = ['contenido']
    verbose_name_plural = "📖 Contenidos (505 - R)"


class NotaBiografica545Inline(admin.TabularInline):
    model = NotaBiografica545
    extra = 1
    fields = ['datos_biograficos', 'url']
    verbose_name_plural = "👤 Notas biográficas (545 - R)"


# =====================================================
# 🔧 INLINES BLOQUE 6XX – Materias y género/forma
# =====================================================
class Materia650Inline(admin.TabularInline):
    model = Materia650
    extra = 1
    fields = ['subdivision']
    verbose_name_plural = "📚 Materias (650 - R)"


class MateriaGenero655Inline(admin.TabularInline):
    model = MateriaGenero655
    extra = 1
    fields = ['subdivision_general']
    verbose_name_plural = "🎭 Materias (Género/forma) (655 - R)"


# =====================================================
# 🔧 INLINES BLOQUE 7XX – Accesos adicionales y relaciones
# =====================================================
class Relacion700Inline(admin.TabularInline):
    model = Relacion700
    extra = 1
    fields = ['descripcion']
    verbose_name_plural = "🔗 Relaciones (700 $i - R)"


class Autoria700Inline(admin.TabularInline):
    model = Autoria700
    extra = 1
    fields = ['autoria']
    verbose_name_plural = "🧾 Autorías (700 $j - R)"


class FuncionEntidad710Inline(admin.TabularInline):
    model = FuncionEntidad710
    extra = 1
    fields = ['funcion']
    verbose_name_plural = "🏛️ Funciones de entidad (710 $e - R)"


class NumeroDocRelacionado773Inline(admin.TabularInline):
    model = NumeroDocumentoRelacionado773
    extra = 1
    fields = ['numero']
    verbose_name_plural = "📘 Números de obra relacionadas (773 $w - R)"


class NumeroObraRelacionada774Inline(admin.TabularInline):
    model = NumeroObraRelacionada774
    extra = 1
    fields = ['numero']
    verbose_name_plural = "📗 Números de obra relacionadas (774 $w - R)"


class NumeroObraRelacionada787Inline(admin.TabularInline):
    model = NumeroObraRelacionada787
    extra = 1
    fields = ['numero']
    verbose_name_plural = "📙 Números de obra relacionadas (787 $w - R)"


# =====================================================
# 🔧 INLINES BLOQUE 8XX – Ubicación y disponibilidad
# =====================================================
class Estanteria852Inline(admin.TabularInline):
    model = Estanteria852
    extra = 1
    fields = ['estanteria']
    verbose_name_plural = "📚 Estanterías (852 $c - R)"


class Disponible856Inline(admin.TabularInline):
    model = Disponible856
    extra = 1
    fields = ['url', 'texto_enlace']
    verbose_name_plural = "🌐 Recursos disponibles (856 - R)"



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
        
        ('🏢 CLASIFICACIoN LOCAL (092)', {
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
        
        ('📖 BLOQUE 2XX - TiTULOS Y PUBLICACIoN', {
            'fields': (
                'titulo_principal',
                'subtitulo',
                'mencion_responsabilidad',
            ),
            'description': 'Campo 245 - Mencion de titulo (obligatorio)'
        }),
        
        ('🎵 BLOQUE 3XX - DESCRIPCIoN FiSICA Y CARACTERiSTICAS', {
            'fields': ('tonalidad_384',),
            'description': (
                'Campo 384 - Tonalidad (NR). '
                'Resto de campos 3XX se gestionan en inlines.'
            ),
            'classes': ('wide',)
        }),
        ('📝 BLOQUE 5XX – NOTAS Y CONTENIDO', {
            'fields': (
                'sumario_520',
            ),
            'description': 'Campos de notas (NR): Sumario o resumen del contenido de la obra (520 $a).',
            'classes': ('wide',)
        }),

        ('🏷️ BLOQUE 6XX – MATERIAS Y GÉNERO/FORMA', {
            'fields': (
                'materia_principal_650',
                'materia_genero_655',
            ),
            'description': (
                'Campos 650 y 655 – Materias controladas según vocabularios autorizados. '
                'Ambos son no repetibles (NR).'
            ),
            'classes': ('wide',)
        }),

        ('🤝 BLOQUE 7XX – RELACIONES Y ACCESOS ADICIONALES', {
            'fields': (
                'nombre_relacionado_700a',
                'coordenadas_biograficas_700d',
                'titulo_relacionado_700t',
                'entidad_relacionada_710a',
                'compositor_coleccion_773a',
                'titulo_coleccion_773t',
                'enlace_unidad_774',
                'titulo_unidad_774t',
                'encabezamiento_principal_787a',
                'titulo_obra_relacionada_787t',
            ),
            'description': (
                'Campos de relación no repetibles según MARC21. '
                'Incluyen accesos personales, institucionales y relaciones con otras obras.'
            ),
            'classes': ('wide',)
        }),

        ('📦 BLOQUE 8XX – UBICACIÓN Y DISPONIBILIDAD', {
            'fields': (
                'institucion_persona_852a',
                'signatura_original_852h',
            ),
            'description': (
                'Campos 852 – Identifican la institución o persona depositaria y la signatura original. '
                'Ambos son no repetibles (NR).'
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
        NumeroParteSeccion130Inline,
        NombreParteSeccion130Inline,
        Forma240Inline,
        MedioInterpretacion240Inline,
        NumeroParteSeccion240Inline,
        NombreParteSeccion240Inline,
        
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
        NotaContenido505Inline,
        NotaBiografica545Inline,
        # Bloque 6XX
        Materia650Inline,
        MateriaGenero655Inline,
        # Bloque 7XX
        Relacion700Inline,
        Autoria700Inline,
        FuncionEntidad710Inline,
        NumeroDocRelacionado773Inline,
        NumeroObraRelacionada774Inline,
        NumeroObraRelacionada787Inline,
        # Bloque 8XX
        Estanteria852Inline,
        Disponible856Inline,

    ]
    
    # Métodos de visualizacion
    def titulo_principal_corto(self, obj):
        """Mostrar titulo principal acortado"""
        titulo = obj.titulo_principal or '(sin titulo)'
        if len(titulo) > 50:
            return f"{titulo[:47]}..."
        return titulo
    titulo_principal_corto.short_description = "Titulo"
    
    def compositor_display(self, obj):
        """Mostrar compositor con enlace"""
        if obj.compositor:
            return format_html(
                '<strong>{}</strong>',
                obj.compositor.apellidos_nombres
            )
        return format_html('<em>Anonimo</em>')
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
        """Accion para regenerar clasificacion 092"""
        updated = 0
        for obra in queryset:
            obra.generar_clasificacion_092()
            obra.save()
            updated += 1
        
        self.message_user(
            request,
            f'{updated} obra(s) clasificada(s) correctamente.'
        )
    generar_clasificacion_accion.short_description = "♻️ Regenerar clasificacion (092)"
    
    # Métodos de validacion
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
    """Admin para titulos uniformes"""
    list_display = ['titulo']
    search_fields = ['titulo']


@admin.register(AutoridadFormaMusical)
class AutoridadFormaMusicalAdmin(admin.ModelAdmin):
    """Admin para formas musicales"""
    list_display = ['forma']
    search_fields = ['forma']


@admin.register(AutoridadEntidad)
class AutoridadEntidadAdmin(admin.ModelAdmin):
    """Admin para autoridades de entidades"""
    list_display = ['nombre']
    search_fields = ['nombre']

