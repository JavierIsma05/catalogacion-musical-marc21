"""
Configuración del Admin de Django organizado por tipo de plantilla MARC21
"""
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse

from .models import (
    ObraGeneral,
    NumeroControlSecuencia,
    BorradorObra,
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadEntidad,
    AutoridadMateria,
    # Modelos auxiliares
    ObraLengua,
    # Bloque 0xx
    IncipitMusical,
    CodigoLengua,
    # Bloque 1xx
    FuncionCompositor,
    # Bloque 2xx
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    Lugar264,
    NombreEntidad264,
    Fecha264,
    # Bloque 3xx
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    # Bloque 4xx
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
    # Bloque 5xx
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
    # Bloque 6xx
    Materia650,
    SubdivisionMateria650,
    MateriaGenero655,
    SubdivisionGeneral655,
    # Bloque 7xx
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    EnlaceUnidadConstituyente774,
    OtrasRelaciones787,
    # Bloque 8xx
    Estanteria852,
    Disponible856,
    TextoEnlace856,
    URL856,
)
from .formatters import MARCFormatter


# ============================================
# INLINES PARA CAMPOS REPETIBLES
# ============================================

# Bloque 0xx - Íncipits
class IncipitMusicalInline(admin.TabularInline):
    model = IncipitMusical
    extra = 0
    fields = ['numero_obra', 'numero_movimiento', 'numero_pasaje', 'titulo_encabezamiento', 'personaje', 'clave', 'voz_instrumento',
              'armadura', 'tiempo', 'notacion_musical'  ]
    verbose_name = "Íncipit Musical (031)"
    verbose_name_plural = "📝 Íncipits Musicales (031 - R)"


# Bloque 1xx - Funciones del Compositor
class FuncionCompositorInline(admin.TabularInline):
    model = FuncionCompositor
    extra = 1
    fields = ['funcion']
    verbose_name = "Función del Compositor (100 $e)"
    verbose_name_plural = "🎼 Funciones del Compositor (100 $e - R)"


# Bloque 2xx - Títulos y Publicación
class TituloAlternativoInline(admin.TabularInline):
    model = TituloAlternativo
    extra = 0
    fields = ['titulo', 'resto_titulo']
    verbose_name = "Título Alternativo (246)"
    verbose_name_plural = "📚 Títulos Alternativos (246 - R)"


class EdicionInline(admin.TabularInline):
    model = Edicion
    extra = 0
    fields = ['edicion']
    verbose_name = "Edición (250)"
    verbose_name_plural = "📖 Ediciones (250 - R)"


class Lugar264Inline(admin.TabularInline):
    model = Lugar264
    extra = 1
    fields = ['lugar']
    verbose_name = "Lugar (264 $a)"
    verbose_name_plural = "Lugares (264 $a - R)"


class Entidad264Inline(admin.TabularInline):
    model = NombreEntidad264
    extra = 1
    fields = ['nombre']
    verbose_name = "Entidad (264 $b)"
    verbose_name_plural = "Entidades (264 $b - R)"


class Fecha264Inline(admin.TabularInline):
    model = Fecha264
    extra = 1
    fields = ['fecha']
    verbose_name = "Fecha (264 $c)"
    verbose_name_plural = "Fechas (264 $c - R)"


class ProduccionPublicacionInline(admin.StackedInline):
    model = ProduccionPublicacion
    extra = 0
    fields = ['funcion']
    inlines = [Lugar264Inline, Entidad264Inline, Fecha264Inline]
    verbose_name = "Producción/Publicación (264)"
    verbose_name_plural = "🏭 Producción/Publicación (264 - R)"


# Bloque 3xx - Medio de Interpretación
class MedioInterpretacion382_aInline(admin.TabularInline):
    model = MedioInterpretacion382_a
    extra = 1
    fields = ['medio']
    verbose_name = "Medio (382 $a)"
    verbose_name_plural = "Medios (382 $a - R)"


class MedioInterpretacion382Inline(admin.StackedInline):
    model = MedioInterpretacion382
    extra = 0
    verbose_name = "Medio de Interpretación (382)"
    verbose_name_plural = "🎹 Medio de Interpretación (382 - R)"
    show_change_link = True


# Bloque 4xx - Series
class TituloSerie490Inline(admin.TabularInline):
    model = TituloSerie490
    extra = 1
    fields = ['titulo_serie']
    verbose_name = "Título Serie (490 $a)"
    verbose_name_plural = "Títulos (490 $a - R)"


class VolumenSerie490Inline(admin.TabularInline):
    model = VolumenSerie490
    extra = 1
    fields = ['volumen']
    verbose_name = "Volumen (490 $v)"
    verbose_name_plural = "Volúmenes (490 $v - R)"


class MencionSerie490Inline(admin.StackedInline):
    model = MencionSerie490
    extra = 0
    fields = []
    verbose_name = "Mención de Serie (490)"
    verbose_name_plural = "📚 Menciones de Serie (490 - R)"
    show_change_link = True

# ============================================
# Bloque 5xx - Notas
# ============================================

class NotaGeneral500Inline(admin.TabularInline):
    model = NotaGeneral500
    extra = 0
    fields = ['nota_general']
    verbose_name = "Nota General (500)"
    verbose_name_plural = "📝 Notas Generales (500 - R)"


class Contenido505Inline(admin.TabularInline):
    model = Contenido505
    extra = 0
    fields = ['contenido']
    verbose_name = "Contenido (505)"
    verbose_name_plural = "📋 Contenidos (505 - R)"


class Sumario520Inline(admin.TabularInline):
    model = Sumario520
    extra = 0
    fields = ['sumario']
    verbose_name = "Sumario (520)"
    verbose_name_plural = "📄 Sumarios (520 - R)"


class DatosBiograficos545Inline(admin.TabularInline):
    model = DatosBiograficos545
    extra = 0
    fields = []
    verbose_name = "Datos Biográficos (545)"
    verbose_name_plural = "👤 Datos Biográficos (545 - R)"


# ============================================
# Bloque 6xx - Materias
# ============================================

class SubdivisionMateria650Inline(admin.TabularInline):
    model = SubdivisionMateria650
    extra = 1
    fields = ['subdivision']
    verbose_name = "Subdivisión (650 $x)"
    verbose_name_plural = "Subdivisiones (650 $x - R)"


class Materia650Inline(admin.StackedInline):
    model = Materia650
    extra = 0
    fields = ['materia']
    verbose_name = "Materia (650)"
    verbose_name_plural = "🏷️ Materias - Temas (650 - R)"
    show_change_link = True


class SubdivisionGeneral655Inline(admin.TabularInline):
    model = SubdivisionGeneral655
    extra = 1
    fields = ['subdivision']
    verbose_name = "Subdivisión (655 $x)"
    verbose_name_plural = "Subdivisiones (655 $x - R)"


class MateriaGenero655Inline(admin.StackedInline):
    model = MateriaGenero655
    extra = 0
    fields = ['materia']
    verbose_name = "Materia Género/Forma (655)"
    verbose_name_plural = "🎭 Materias - Género/Forma (655 - R)"
    show_change_link = True


# ============================================
# Bloque 7xx - Puntos de Acceso Adicionales
# ============================================

class TerminoAsociado700Inline(admin.TabularInline):
    model = TerminoAsociado700
    extra = 0
    fields = ['termino']
    verbose_name = "Término Asociado (700 $c)"
    verbose_name_plural = "Términos Asociados (700 $c - R)"


class Funcion700Inline(admin.TabularInline):
    model = Funcion700
    extra = 1
    fields = ['funcion']
    verbose_name = "Función (700 $e)"
    verbose_name_plural = "Funciones (700 $e - R)"


class NombreRelacionado700Inline(admin.StackedInline):
    model = NombreRelacionado700
    extra = 0
    fields = ['persona', 'coordenadas_biograficas', 'relacion', 'autoria', 'titulo_obra']
    verbose_name = "Nombre Relacionado (700)"
    verbose_name_plural = "👥 Nombres Relacionados (700 - R)"
    show_change_link = True


class EntidadRelacionada710Inline(admin.TabularInline):
    model = EntidadRelacionada710
    extra = 0
    fields = ['entidad', 'funcion']
    verbose_name = "Entidad Relacionada (710)"
    verbose_name_plural = "🏛️ Entidades Relacionadas (710 - R)"


# 773 — Enlace a documento fuente
class EnlaceDocumentoFuente773Inline(admin.TabularInline):
    model = EnlaceDocumentoFuente773
    extra = 0
    fields = ['encabezamiento_principal', 'titulo']
    verbose_name = "Documento Fuente (773)"
    verbose_name_plural = "📘 Documentos Fuente (773 - R)"


# 774 — Enlace a unidad constituyente
class EnlaceUnidadConstituyente774Inline(admin.TabularInline):
    model = EnlaceUnidadConstituyente774
    extra = 0
    fields = ['encabezamiento_principal', 'titulo']
    verbose_name = "Unidad Constituyente (774)"
    verbose_name_plural = "📗 Unidades Constituyentes (774 - R)"


# 787 — Otras relaciones
class OtrasRelaciones787Inline(admin.TabularInline):
    model = OtrasRelaciones787
    extra = 0
    fields = ['encabezamiento_principal', 'titulo']
    verbose_name = "Otra Relación (787)"
    verbose_name_plural = "🔗 Otras Relaciones (787 - R)"


# ============================================
# Bloque 8xx - Ubicación
# ============================================

class Estanteria852Inline(admin.TabularInline):
    model = Estanteria852
    extra = 1
    fields = ['estanteria']
    verbose_name = "Estantería (852 $c)"
    verbose_name_plural = "Estanterías (852 $c - R)"


class Disponible856Inline(admin.TabularInline):
    model = Disponible856
    extra = 0
    fields = []
    verbose_name = "Recurso Disponible (856)"
    verbose_name_plural = "🌐 Recursos Disponibles (856 - R)"


class URL856Inline(admin.TabularInline):
    model = URL856
    extra = 1
    fields = ['url']
    verbose_name = "URL (856 $u)"
    verbose_name_plural = "URLs (856 $u)"

class TextoEnlace856Inline(admin.TabularInline):
    model = TextoEnlace856
    extra = 1
    fields = ['texto_enlace']
    verbose_name = "Texto del enlace (856 $y)"
    verbose_name_plural = "Textos del enlace (856 $y)"

# ============================================
# INLINES PARA MODELOS AUXILIARES
# ============================================

class ObraLenguaInline(admin.TabularInline):
    """Inline para campo 041 - Código de Lengua"""
    model = ObraLengua
    extra = 1
    fields = ['lengua', 'tipo_lengua', 'orden']
    ordering = ['orden']
    verbose_name = "Lengua (041)"
    verbose_name_plural = "🌍 Lenguas (041 - Código de Lengua)"


# ============================================
# MIXIN PARA VALIDACIÓN DE INLINES
# ============================================

class InlineValidationMixin:
    """Mixin para validar relaciones después de guardar todos los inlines"""

    def save_model(self, request, obj, form, change):
        """Guardar el modelo - validar solo en edición"""
        if not change:
            # Primera vez guardando (creación inicial)
            # Guardar sin validaciones completas del modelo
            obj.save()
            request._obra_to_validate = None  # No validar en creación
        else:
            # Guardado normal
            super().save_model(request, obj, form, change)
            request._obra_to_validate = obj

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if hasattr(request, '_obra_to_validate') and request._obra_to_validate:
            obj = request._obra_to_validate
            try:
                obj.clean()
            except ValidationError as e:
                if hasattr(e, 'error_dict'):
                    for field, errors in e.error_dict.items():
                        for error in errors:
                            self.message_user(
                                request,
                                f"Error en {field}: {error.message}",
                                level='warning'
                            )
                else:
                    self.message_user(request, f"Error de validación: {str(e)}", level='warning')


# ============================================
# FIELDSETS POR TIPO DE PLANTILLA
# ============================================

# COLECCIÓN MANUSCRITA (d, c)
FIELDSETS_COLECCION_MANUSCRITA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🎵 Punto de Acceso Principal', {
        'fields': (
            ('compositor', 'autoria'),
            ('titulo_uniforme', 'forma_130'),
            ('medio_interpretacion_130', 'tonalidad_130'),
            ('numero_parte_130', 'arreglo_130', 'nombre_parte_130'),
        )
    }),
    ('🎼 Título Uniforme con Compositor (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        ),
        'classes': ('collapse',)
    }),
    ('📖 Título y Responsabilidad (245/246/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación (382)', {
        'fields': (
            'medio_interpretacion_130',
        ),
        'classes': ('collapse',)
    }),
    # Los campos 500/505/520/545, 650/655, 700/710 se manejan con inlines
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)

# OBRA INDIVIDUAL EN COLECCIÓN MANUSCRITA (d, a)
FIELDSETS_OBRA_EN_COLECCION_MANUSCRITA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🎵 Compositor (100)', {
        'fields': (
            ('compositor', 'autoria'),
        )
    }),
    ('🎼 Título Uniforme (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        )
    }),
    ('📖 Título y Responsabilidad (245/246/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación y Designación (382/383/384)', {
        'fields': (
            'medio_interpretacion_240',
            ('numero_obra', 'opus'),
            'tonalidad_384',
        ),
        'classes': ('collapse',)
    }),
    # Los campos 500/520/545, 650/655, 700/710, 773 se manejan con inlines
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)

# OBRA INDIVIDUAL MANUSCRITA (d, m)
FIELDSETS_OBRA_MANUSCRITA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🎵 Compositor (100)', {
        'fields': (
            ('compositor', 'autoria'),
        )
    }),
    ('🎼 Título Uniforme (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        )
    }),
    ('📖 Título y Responsabilidad (245/246/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación y Designación (382/383/384)', {
        'fields': (
            'medio_interpretacion_240',
            ('numero_obra', 'opus'),
            'tonalidad_384',
        ),
        'classes': ('collapse',)
    }),
    # Los campos 500/520/545, 650/655, 700/710, 787 se manejan con inlines
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)

# COLECCIÓN IMPRESA (c, c)
FIELDSETS_COLECCION_IMPRESA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🔢 Identificadores (020/024/028)', {
        'fields': (
            ('isbn', 'ismn'),
            'numero_editor',
        )
    }),
    ('🎵 Punto de Acceso Principal', {
        'fields': (
            ('compositor', 'autoria'),
            ('titulo_uniforme', 'forma_130'),
            ('medio_interpretacion_130', 'tonalidad_130'),
            ('numero_parte_130', 'arreglo_130', 'nombre_parte_130'),
        )
    }),
    ('🎼 Título Uniforme con Compositor (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        ),
        'classes': ('collapse',)
    }),
    ('📖 Título y Responsabilidad (245/246/250/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación (382)', {
        'fields': (
            'medio_interpretacion_130',
        ),
        'classes': ('collapse',)
    }),
    ('📝 Notas y Contenido (500/505/520/545)', {
        'fields': (),
        'classes': ('collapse',)
    }),
    ('🏷️ Materias (650/655)', {
        'fields': (),
        'classes': ('collapse',)
    }),
    ('🔗 Puntos de Acceso Adicionales (700/710)', {
        'fields': (),
        'classes': ('collapse',)
    }),
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)

# OBRA INDIVIDUAL EN COLECCIÓN IMPRESA (c, a)
FIELDSETS_OBRA_EN_COLECCION_IMPRESA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🎵 Compositor (100)', {
        'fields': (
            ('compositor', 'autoria'),
        )
    }),
    ('🎼 Título Uniforme (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        )
    }),
    ('📖 Título y Responsabilidad (245/246/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación y Designación (382/383/384)', {
        'fields': (
            'medio_interpretacion_240',
            ('numero_obra', 'opus'),
            'tonalidad_384',
        ),
        'classes': ('collapse',)
    }),
    # Los campos 500/520/545, 650/655, 700/710, 773 se manejan con inlines
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)

# OBRA INDIVIDUAL IMPRESA (c, m)
FIELDSETS_OBRA_IMPRESA = (
    ('📋 Identificación', {
        'fields': ('num_control', 'tipo_registro', 'nivel_bibliografico', 'tipo_obra_display')
    }),
    ('🔢 Identificadores (020/024/028)', {
        'fields': (
            ('isbn', 'ismn'),
            'numero_editor',
        )
    }),
    ('🎵 Compositor (100)', {
        'fields': (
            ('compositor', 'autoria'),
        )
    }),
    ('🎼 Título Uniforme (240)', {
        'fields': (
            ('titulo_240', 'forma_240'),
            ('medio_interpretacion_240', 'tonalidad_240'),
            ('numero_parte_240', 'arreglo_240', 'nombre_parte_240'),
        )
    }),
    ('📖 Título y Responsabilidad (245/246/250/264)', {
        'fields': (
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
        )
    }),
    ('📐 Descripción Física (300/340/348)', {
        'fields': (
            'extension',
            'otras_caracteristicas',
            ('dimension', 'material_acompanante'),
            ('ms_imp', 'formato'),
        ),
        'classes': ('collapse',)
    }),
    ('🎹 Medio de Interpretación y Designación (382/383/384)', {
        'fields': (
            'medio_interpretacion_240',
            ('numero_obra', 'opus'),
            'tonalidad_384',
        ),
        'classes': ('collapse',)
    }),
    # Los campos 500/520/545, 650/655, 700/710, 787 se manejan con inlines
    ('🏛️ Catalogación (040/092)', {
        'fields': ('centro_catalogador', 'signatura_completa_display'),
        'classes': ('collapse',)
    }),
    ('📅 Metadatos del Sistema', {
        'fields': ('fecha_creacion_sistema', 'fecha_modificacion_sistema', 'fecha_hora_ultima_transaccion'),
        'classes': ('collapse',)
    }),
    ('👁️ Vista Previa MARC', {
        'fields': ('preview_marc',),
        'classes': ('collapse',)
    }),
)


# ============================================
# ADMIN PRINCIPAL
# ============================================

@admin.register(ObraGeneral)
class ObraGeneralAdmin(InlineValidationMixin, admin.ModelAdmin):
    """Admin que cambia los fieldsets según el tipo de obra"""

    search_fields = [
        'num_control',
        'titulo_principal',
        'subtitulo',
        'compositor__apellidos_nombres',
        'titulo_uniforme__titulo',
    ]

    list_filter = [
        'tipo_registro',
        'nivel_bibliografico',
        'centro_catalogador',
        'fecha_creacion_sistema',
    ]

    list_display = [
        'num_control_link',
        'titulo_principal_truncado',
        'tipo_obra_badge',
        'punto_acceso_principal',
        'fecha_creacion_sistema',
        'ver_marc',
    ]

    ordering = ['-fecha_creacion_sistema']

    readonly_fields = [
        'num_control',
        'estado_registro',
        'codigo_informacion',
        'fecha_hora_ultima_transaccion',
        'fecha_creacion_sistema',
        'fecha_modificacion_sistema',
        'tipo_obra_display',
        'signatura_completa_display',
        'preview_marc',
    ]

    actions = ['exportar_marc', 'duplicar_obras']

    # Inlines para campos repetibles (organizados por bloque MARC)
    inlines = [
        # Modelos Auxiliares - Lenguas
        ObraLenguaInline,
        # Bloque 0xx - Íncipits
        IncipitMusicalInline,
        # Bloque 1xx - Compositor
        FuncionCompositorInline,
        # Bloque 2xx - Títulos y Publicación
        TituloAlternativoInline,
        EdicionInline,
        ProduccionPublicacionInline,
        # Bloque 3xx - Medio de Interpretación
        MedioInterpretacion382Inline,
        # Bloque 4xx - Series
        MencionSerie490Inline,
        # Bloque 5xx - Notas
        NotaGeneral500Inline,
        Contenido505Inline,
        Sumario520Inline,
        DatosBiograficos545Inline,
        # Bloque 6xx - Materias
        Materia650Inline,
        MateriaGenero655Inline,
        # Bloque 7xx - Puntos de Acceso Adicionales
        NombreRelacionado700Inline,
        EntidadRelacionada710Inline,
        EnlaceDocumentoFuente773Inline,
        EnlaceUnidadConstituyente774Inline,
        OtrasRelaciones787Inline,
        # Bloque 8xx - Ubicación
        Disponible856Inline,
    ]

    # Métodos para cambiar fieldsets dinámicamente

    def get_fieldsets(self, request, obj=None):
        """Retorna los fieldsets según el tipo de obra"""
        if obj is None:
            # Para crear nueva obra, mostrar campos básicos
            return (
                ('📋 Crear Nueva Obra', {
                    'fields': ('tipo_registro', 'nivel_bibliografico')
                }),
            )

        # Determinar tipo de obra
        tipo = (obj.tipo_registro, obj.nivel_bibliografico)

        fieldsets_map = {
            ('d', 'c'): FIELDSETS_COLECCION_MANUSCRITA,
            ('d', 'a'): FIELDSETS_OBRA_EN_COLECCION_MANUSCRITA,
            ('d', 'm'): FIELDSETS_OBRA_MANUSCRITA,
            ('c', 'c'): FIELDSETS_COLECCION_IMPRESA,
            ('c', 'a'): FIELDSETS_OBRA_EN_COLECCION_IMPRESA,
            ('c', 'm'): FIELDSETS_OBRA_IMPRESA,
        }

        return fieldsets_map.get(tipo, FIELDSETS_OBRA_MANUSCRITA)

    def get_readonly_fields(self, request, obj=None):
        """Campos de solo lectura según si es creación o edición"""
        if obj is None:
            # En creación, permitir seleccionar tipo y nivel
            return []

        # En edición, todo readonly excepto los campos editables
        return self.readonly_fields + ['tipo_registro', 'nivel_bibliografico']

    def get_form(self, request, obj=None, **kwargs):
        """Personalizar el formulario según si es creación o edición"""
        form = super().get_form(request, obj, **kwargs)

        if obj is None:
            # En creación, hacer campos opcionales temporalmente
            for field_name in ['titulo_principal', 'compositor', 'titulo_uniforme']:
                if field_name in form.base_fields:
                    form.base_fields[field_name].required = False

        return form

    # Métodos de visualización

    def num_control_link(self, obj):
        url = reverse('admin:catalogacion_obrageneral_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.num_control)
    num_control_link.short_description = 'N° Control'
    num_control_link.admin_order_field = 'num_control'

    def titulo_principal_truncado(self, obj):
        if len(obj.titulo_principal) > 50:
            return obj.titulo_principal[:50] + '...'
        return obj.titulo_principal
    titulo_principal_truncado.short_description = 'Título'
    titulo_principal_truncado.admin_order_field = 'titulo_principal'

    def tipo_obra_badge(self, obj):
        colors = {
            'CM': '#8B4513',
            'OICM': '#A0522D',
            'OIM': '#CD853F',
            'CI': '#4169E1',
            'OICI': '#4682B4',
            'OII': '#5F9EA0',
        }
        color = colors.get(obj.tipo_obra, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 0.85em;">{}</span>',
            color,
            obj.tipo_obra_descripcion
        )
    tipo_obra_badge.short_description = 'Tipo'

    def punto_acceso_principal(self, obj):
        if obj.compositor:
            return f"👤 {obj.compositor}"
        if obj.titulo_uniforme:
            return f"📚 {obj.titulo_uniforme}"
        return "⚠️ Sin definir"
    punto_acceso_principal.short_description = 'Punto de Acceso'

    def ver_marc(self, obj):
        return format_html(
            '<a class="button" href="{}#marc-preview">Ver MARC</a>',
            reverse('admin:catalogacion_obrageneral_change', args=[obj.pk])
        )
    ver_marc.short_description = 'MARC'

    def tipo_obra_display(self, obj):
        if obj.pk:
            return f"{obj.tipo_obra} - {obj.tipo_obra_descripcion}"
        return "Se asignará al guardar"
    tipo_obra_display.short_description = 'Tipo de Obra'

    def signatura_completa_display(self, obj):
        if obj.pk:
            return obj.signatura_completa
        return "Se generará al guardar"
    signatura_completa_display.short_description = 'Signatura (092)'

    def preview_marc(self, obj):
        if not obj.pk:
            return "Guarde la obra para ver el registro MARC"

        formatter = MARCFormatter(obj)
        marc_text = formatter.format_full_record()

        return format_html(
            '<pre id="marc-preview" style="background-color: #f5f5f5; padding: 15px; '
            'border: 1px solid #ddd; border-radius: 4px; '
            'font-family: monospace; font-size: 0.9em;">{}</pre>',
            marc_text
        )
    preview_marc.short_description = 'Registro MARC Completo'

    # Acciones

    def exportar_marc(self, request, queryset):
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="obras_marc.txt"'

        for obra in queryset:
            formatter = MARCFormatter(obra)
            response.write(formatter.format_full_record())
            response.write("\n\n" + "="*80 + "\n\n")

        self.message_user(request, f"{queryset.count()} obras exportadas correctamente.")
        return response
    exportar_marc.short_description = "📥 Exportar como MARC21"

    def duplicar_obras(self, request, queryset):
        contador = 0
        for obra in queryset:
            obra.pk = None
            obra.num_control = None
            obra.save()
            contador += 1

        self.message_user(request, f"✅ {contador} obra(s) duplicada(s) correctamente.")
    duplicar_obras.short_description = "📋 Duplicar obras"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        total = ObraGeneral.objects.count()
        manuscritas = ObraGeneral.objects.manuscritas().count()
        impresas = ObraGeneral.objects.impresas().count()
        colecciones = ObraGeneral.objects.colecciones().count()

        extra_context['stats'] = {
            'total': total,
            'manuscritas': manuscritas,
            'impresas': impresas,
            'colecciones': colecciones,
        }

        return super().changelist_view(request, extra_context)


@admin.register(NumeroControlSecuencia)
class NumeroControlSecuenciaAdmin(admin.ModelAdmin):
    list_display = ['tipo_registro_display', 'ultimo_numero', 'fecha_actualizacion']
    readonly_fields = ['tipo_registro', 'ultimo_numero', 'fecha_actualizacion']

    def tipo_registro_display(self, obj):
        return obj.get_tipo_registro_display()
    tipo_registro_display.short_description = 'Tipo de Registro'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================
# ADMIN PARA MODELOS ANIDADOS (CON SUBCAMPOS REPETIBLES)
# ============================================

@admin.register(ProduccionPublicacion)
class ProduccionPublicacionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'funcion', 'obra']
    list_filter = ['funcion']
    inlines = [Lugar264Inline, Entidad264Inline, Fecha264Inline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


@admin.register(MedioInterpretacion382)
class MedioInterpretacion382Admin(admin.ModelAdmin):
    list_display = ['__str__', 'obra']
    inlines = [MedioInterpretacion382_aInline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


@admin.register(MencionSerie490)
class MencionSerie490Admin(admin.ModelAdmin):
    list_display = ['__str__', 'obra']
    list_filter = ['obra']
    inlines = [TituloSerie490Inline, VolumenSerie490Inline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


@admin.register(Materia650)
class Materia650Admin(admin.ModelAdmin):
    list_display = ['materia', 'obra']
    search_fields = ['materia']
    inlines = [SubdivisionMateria650Inline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


@admin.register(MateriaGenero655)
class MateriaGenero655Admin(admin.ModelAdmin):
    list_display = ['materia', 'obra']
    search_fields = ['materia']
    inlines = [SubdivisionGeneral655Inline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


@admin.register(NombreRelacionado700)
class NombreRelacionado700Admin(admin.ModelAdmin):
    list_display = ['persona', 'relacion', 'autoria', 'titulo_obra', 'obra']
    search_fields = ['persona__apellidos_nombres', 'titulo_obra', 'relacion', 'autoria']
    inlines = [TerminoAsociado700Inline, Funcion700Inline]

    def has_module_permission(self, request):
        return False  # Ocultar del menú principal


# @admin.register(Ubicacion852)
# class Ubicacion852Admin(admin.ModelAdmin):
#     list_display = ['institucion_persona', 'signatura_original', 'obra']
#     search_fields = ['institucion_persona', 'signatura_original']
#     inlines = [Estanteria852Inline]

#     def has_module_permission(self, request):
#         return False  # Ocultar del menú principal
@admin.register(Disponible856)
class Disponible856Admin(admin.ModelAdmin):
    inlines = [URL856Inline, TextoEnlace856Inline]

    def has_module_permission(self, request):
        return False


# ============================================
# ADMIN PARA AUTORIDADES
# ============================================

@admin.register(AutoridadPersona)
class AutoridadPersonaAdmin(admin.ModelAdmin):
    list_display = ['apellidos_nombres', 'coordenadas_biograficas', 'fecha_modificacion']
    search_fields = ['apellidos_nombres', 'coordenadas_biograficas']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['apellidos_nombres']

    fieldsets = (
        ('Información de la Persona', {
            'fields': ('apellidos_nombres', 'coordenadas_biograficas')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AutoridadTituloUniforme)
class AutoridadTituloUniformeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_modificacion']
    search_fields = ['titulo']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['titulo']

    fieldsets = (
        ('Información del Título', {
            'fields': ('titulo',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AutoridadFormaMusical)
class AutoridadFormaMusicalAdmin(admin.ModelAdmin):
    list_display = ['forma', 'fecha_modificacion']
    search_fields = ['forma']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['forma']

    fieldsets = (
        ('Información de la Forma Musical', {
            'fields': ('forma',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AutoridadEntidad)
class AutoridadEntidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'fecha_modificacion']
    search_fields = ['nombre', 'pais']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['nombre']

    fieldsets = (
        ('Información de la Entidad', {
            'fields': ('nombre', 'pais', 'descripcion')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AutoridadMateria)
class AutoridadMateriaAdmin(admin.ModelAdmin):
    list_display = ['termino', 'fecha_modificacion']
    search_fields = ['termino']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    ordering = ['termino']

    fieldsets = (
        ('Información de la Materia', {
            'fields': ('termino',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# ADMIN DE BORRADORES
# ============================================

@admin.register(BorradorObra)
class BorradorObraAdmin(admin.ModelAdmin):
    """Administración de borradores de obras MARC21"""

    list_display = [
        'titulo_temporal',
        'tipo_obra_display',
        'tipo_registro_display',
        'pestana_actual',
        'fecha_modificacion',
        'dias_antiguedad_display'
    ]
    list_filter = [
        'tipo_obra',
        'tipo_registro',
        'nivel_bibliografico',
        'fecha_creacion',
        'fecha_modificacion'
    ]
    search_fields = [
        'titulo_temporal',
        'num_control_temporal',
        'datos_formulario'
    ]
    readonly_fields = [
        'fecha_creacion',
        'fecha_modificacion',
        'titulo_temporal',
        'num_control_temporal',
        'tipo_registro',
        'nivel_bibliografico'
    ]
    ordering = ['-fecha_modificacion']

    fieldsets = (
        ('Información del Borrador', {
            'fields': (
                'tipo_obra',
                'titulo_temporal',
                'num_control_temporal',
                'tipo_registro',
                'nivel_bibliografico',
                'pestana_actual'
            )
        }),
        ('Datos del Formulario', {
            'fields': ('datos_formulario',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )

    actions = ['eliminar_borradores_antiguos', 'limpiar_borradores_sin_titulo']

    def tipo_obra_display(self, obj):
        """Muestra el tipo de obra con icono"""
        iconos = {
            'manuscrito_independiente': '📜',
            'manuscrito_coleccion': '📚',
            'impreso_independiente': '📖',
            'impreso_coleccion': '📚',
        }
        icono = iconos.get(obj.tipo_obra, '📄')
        return format_html(
            '{} {}',
            icono,
            obj.get_descripcion_tipo()
        )
    tipo_obra_display.short_description = 'Tipo de Obra'

    def tipo_registro_display(self, obj):
        """Muestra el tipo de registro"""
        if obj.tipo_registro == 'd':
            return '📝 Manuscrito'
        elif obj.tipo_registro == 'c':
            return '🖨️ Impreso'
        return '-'
    tipo_registro_display.short_description = 'Tipo'

    def dias_antiguedad_display(self, obj):
        """Muestra días desde última modificación con color"""
        dias = obj.dias_desde_modificacion()
        if dias == 0:
            return format_html('<span style="color: green;">●</span> Hoy')
        elif dias == 1:
            return format_html('<span style="color: green;">●</span> Ayer')
        elif dias < 7:
            return format_html(
                '<span style="color: orange;">●</span> Hace {} días',
                dias
            )
        else:
            return format_html(
                '<span style="color: red;">●</span> Hace {} días',
                dias
            )
    dias_antiguedad_display.short_description = 'Antigüedad'

    def eliminar_borradores_antiguos(self, request, queryset):
        """Elimina borradores con más de 30 días"""
        count = 0
        for borrador in queryset:
            if borrador.dias_desde_modificacion() > 30:
                borrador.delete()
                count += 1

        self.message_user(
            request,
            f"{count} borradores antiguos (>30 días) eliminados."
        )
    eliminar_borradores_antiguos.short_description = "🗑️ Eliminar borradores > 30 días"

    def limpiar_borradores_sin_titulo(self, request, queryset):
        """Elimina borradores sin título"""
        count = queryset.filter(titulo_temporal='Sin título').delete()[0]
        self.message_user(
            request,
            f"{count} borradores sin título eliminados."
        )
    limpiar_borradores_sin_titulo.short_description = "🧹 Limpiar borradores sin título"
