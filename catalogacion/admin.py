from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea, Select, NumberInput
from .models import (
    ObraGeneral,
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadMateria,
    TituloAlternativo,        # ✅ Campo 246
    Edicion,                   # ✅ Campo 250
    ProduccionPublicacion      # ✅ Campo 264
)

# ================================================
# 🎬 INLINES PARA CAMPOS REPETIBLES
# ================================================

class TituloAlternativoInline(admin.TabularInline):
    """
    Inline para gestionar múltiples títulos alternativos (Campo 246)
    Permite agregar variantes de títulos
    """
    model = TituloAlternativo
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = ['titulo', 'resto_titulo']
    
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '60', 'class': 'vTextField'})
        },
    }
    
    verbose_name = "Título Alternativo (246)"
    verbose_name_plural = "📚 Títulos Alternativos (Campo 246) - Repetible"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        """Personalizar el formset"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 246 es REPETIBLE. Agregue títulos alternativos, abreviados o variantes "
            "que aparezcan en el recurso."
        )
        return formset


class EdicionInline(admin.TabularInline):
    """
    Inline para gestionar múltiples ediciones (Campo 250)
    Permite registrar información de las ediciones
    """
    model = Edicion
    extra = 1
    min_num = 0
    max_num = 5
    
    fields = ['edicion']
    
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '60', 'class': 'vTextField'})
        },
    }
    
    verbose_name = "Edición (250)"
    verbose_name_plural = "📚 Ediciones (Campo 250) - Repetible"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        """Personalizar el formset"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 250 es REPETIBLE. Agregue diferentes ediciones "
            "con sus correspondientes datos de edición."
        )
        return formset


class ProduccionPublicacionInline(admin.TabularInline):
    """
    Inline para gestionar múltiples registros 264 (Producción/Publicación)
    Permite agregar producción, publicación, distribución, fabricación y copyright
    """
    model = ProduccionPublicacion
    extra = 1
    min_num = 0
    max_num = 10
    
    fields = [
        'funcion',
        'lugar',
        'nombre_entidad',
        'fecha',
        'orden'
    ]
    
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '40', 'class': 'vTextField'})
        },
    }
    
    verbose_name = "Registro 264 (Producción/Publicación/Distribución/Fabricación/Copyright)"
    verbose_name_plural = "📚 BLOQUE 2XX - Producción/Publicación (Campo 264) - Repetible"
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        """Personalizar el formset"""
        formset = super().get_formset(request, obj, **kwargs)
        formset.help_text = (
            "⚠️ Campo 264 es REPETIBLE. Puede agregar múltiples registros para "
            "distinguir entre producción, publicación, distribución, fabricación y copyright. "
            "Para manuscritos, use función 'Producción' (0)."
        )
        return formset


# ================================================
# 📚 ADMINISTRACIÓN DE TABLAS DE AUTORIDADES
# ================================================

@admin.register(AutoridadPersona)
class AutoridadPersonaAdmin(admin.ModelAdmin):
    """Gestión de nombres de personas normalizados"""
    
    list_display = ['apellidos_nombres', 'fechas', 'fecha_creacion']
    search_fields = ['apellidos_nombres', 'fechas']
    list_filter = ['fecha_creacion']
    ordering = ['apellidos_nombres']
    
    fieldsets = (
        ('Información de la Persona', {
            'fields': ('apellidos_nombres', 'fechas'),
            'description': 'Formato: Apellidos, Nombres | Fechas: año nacimiento - año muerte'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['fecha_creacion']
        return []


@admin.register(AutoridadTituloUniforme)
class AutoridadTituloUniformeAdmin(admin.ModelAdmin):
    """Gestión de títulos uniformes normalizados"""
    
    list_display = ['titulo', 'fecha_creacion', 'cantidad_usos']
    search_fields = ['titulo']
    list_filter = ['fecha_creacion']
    ordering = ['titulo']
    
    def cantidad_usos(self, obj):
        """Muestra cuántas obras usan este título"""
        usos_130 = obj.obras_130.count()
        usos_240 = obj.obras_240.count()
        total = usos_130 + usos_240
        return f"{total} obras ({usos_130} en 130, {usos_240} en 240)"
    
    cantidad_usos.short_description = 'Usos'


@admin.register(AutoridadFormaMusical)
class AutoridadFormaMusicalAdmin(admin.ModelAdmin):
    """Gestión de formas musicales normalizadas"""
    
    list_display = ['forma', 'fecha_creacion', 'cantidad_usos']
    search_fields = ['forma']
    list_filter = ['fecha_creacion']
    ordering = ['forma']
    
    def cantidad_usos(self, obj):
        """Muestra cuántas obras usan esta forma"""
        usos_130 = obj.obras_130_forma.count()
        usos_240 = obj.obras_240_forma.count()
        total = usos_130 + usos_240
        return f"{total} obras ({usos_130} en 130, {usos_240} en 240)"
    
    cantidad_usos.short_description = 'Usos'


@admin.register(AutoridadMateria)
class AutoridadMateriaAdmin(admin.ModelAdmin):
    """Gestión de términos de materia normalizados"""
    
    list_display = ['termino', 'fecha_creacion']
    search_fields = ['termino']
    list_filter = ['fecha_creacion']
    ordering = ['termino']


# ================================================
# 🎵 ADMINISTRACIÓN PRINCIPAL - OBRA GENERAL
# ================================================

@admin.register(ObraGeneral)
class ObraGeneralAdmin(admin.ModelAdmin):
    """
    Administración principal de obras musicales MARC21
    Organizado según la estructura del documento
    """
    
    # ✅ AGREGAR LOS INLINES - Orden importante para visualización
    inlines = [
        TituloAlternativoInline,    # Campo 246
        EdicionInline,               # Campo 250
        ProduccionPublicacionInline  # Campo 264
    ]
    
    # ------------------------------------------------
    # Lista de registros
    # ------------------------------------------------
    list_display = [
        'num_control',
        'get_punto_acceso_principal',
        'titulo_principal',
        'get_tipo_registro_display',
        'get_nivel_bibliografico_display',
        'fecha_creacion_sistema'
    ]
    
    list_filter = [
        'tipo_registro',
        'nivel_bibliografico',
        'codigo_lengua',
        'codigo_pais',
        'fecha_creacion_sistema'
    ]
    
    search_fields = [
        'num_control',
        'compositor__apellidos_nombres',
        'titulo_uniforme__titulo',
        'titulo_240__titulo',
        'titulo_principal',
        'isbn',
        'ismn'
    ]
    
    ordering = ['-num_control']
    
    # ------------------------------------------------
    # Campos solo lectura (autogenerados)
    # ------------------------------------------------
    readonly_fields = [
        'num_control',
        'fecha_hora_ultima_transaccion',
        'codigo_informacion',
        'clasif_num_control',
        'estado_registro',
        'fecha_creacion_sistema',
        'fecha_modificacion_sistema'
    ]
    
    # ------------------------------------------------
    # Organización en secciones (fieldsets)
    # ✅ AJUSTADO: Eliminados campos que ahora son repetibles
    # ------------------------------------------------
    fieldsets = (
        ('🎯 DATOS GENERADOS AUTOMÁTICAMENTE', {
            'classes': ('collapse',),
            'fields': (
                'num_control',
                'fecha_hora_ultima_transaccion',
                'codigo_informacion',
                'estado_registro',
                'fecha_creacion_sistema',
                'fecha_modificacion_sistema'
            ),
            'description': 'Estos campos se generan automáticamente según MARC21'
        }),
        
        ('📋 CABECERA O LÍDER', {
            'fields': (
                'tipo_registro',
                'nivel_bibliografico'
            ),
            'description': 'Posiciones 05, 06, 07 de la cabecera MARC21'
        }),
        
        ('🔢 BLOQUE 0XX - Números e identificadores', {
            'fields': (
                ('isbn', 'ismn'),
                ('numero_editor', 'indicador_028'),
                'centro_catalogador',
                ('codigo_lengua', 'codigo_pais'),
            ),
            'description': 'Campos 020, 024, 028, 040, 041, 044'
        }),
        
        ('🎼 BLOQUE 0XX - Íncipit musical (Campo 031)', {
            'classes': ('collapse',),
            'fields': (
                ('incipit_num_obra', 'incipit_num_movimiento', 'incipit_num_pasaje'),
                'incipit_titulo',
                'incipit_voz_instrumento',
                'incipit_notacion',
                'incipit_url'
            ),
            'description': 'Información del íncipit musical codificado'
        }),
        
        ('📁 BLOQUE 0XX - Clasificación local (Campo 092)', {
            'fields': (
                ('clasif_institucion', 'clasif_proyecto', 'clasif_pais'),
                ('clasif_ms_imp', 'clasif_num_control')
            ),
            'description': 'Sistema de clasificación local UNL-BLMP'
        }),
        
        ('👤 BLOQUE 1XX - Punto de acceso principal: COMPOSITOR (Campo 100)', {
            'fields': (
                'compositor',
                ('compositor_funcion', 'compositor_autoria')
            ),
            'description': '⚠️ Usar SOLO si hay compositor identificado. Si usa esto, debe llenar campo 240 (no 130). Cruzar con campos 600 y 700.'
        }),
        
        ('🎵 BLOQUE 1XX - Punto de acceso principal: TÍTULO UNIFORME (Campo 130)', {
            'fields': (
                'titulo_uniforme',
                'titulo_uniforme_forma',
                'titulo_uniforme_medio_interpretacion',
                ('titulo_uniforme_num_parte', 'titulo_uniforme_nombre_parte'),
                'titulo_uniforme_arreglo',
                'titulo_uniforme_tonalidad'
            ),
            'description': '⚠️ Usar SOLO para obras anónimas o sin compositor principal. NO usar si ya llenó campo 100. Cruzar con campo 240.'
        }),
        
        ('🎶 BLOQUE 2XX - Título uniforme secundario (Campo 240)', {
            'fields': (
                'titulo_240',
                'titulo_240_forma',
                'titulo_240_medio_interpretacion',
                ('titulo_240_num_parte', 'titulo_240_nombre_parte'),
                'titulo_240_arreglo',
                'titulo_240_tonalidad'
            ),
            'description': '⚠️ Usar SOLO cuando hay compositor en campo 100. Cruzar con campo 130.'
        }),
        
        ('📖 BLOQUE 2XX - Título propiamente dicho (Campo 245)', {
            'fields': (
                'titulo_principal',
                'subtitulo',
                'mencion_responsabilidad'
            ),
            'description': 'Título tal como aparece en la fuente (obligatorio). Los campos 246, 250 y 264 se manejan como modelos repetibles en los inlines.'
        }),
        
        ('📏 BLOQUE 3XX - Descripción física (Campo 300)', {
            'fields': (
                'extension',
                'otros_detalles_fisicos',
                'dimensiones',
                'material_acompanante'
            ),
            'description': 'Características físicas del recurso'
        }),
    )
    
    # ------------------------------------------------
    # Personalización de widgets para campos específicos
    # ------------------------------------------------
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '80', 'class': 'vTextField'})
        },
        models.TextField: {
            'widget': Textarea(attrs={'rows': 3, 'cols': 80, 'class': 'vLargeTextField'})
        },
    }
    
    # ------------------------------------------------
    # Acciones personalizadas
    # ------------------------------------------------
    actions = ['duplicar_obra', 'exportar_marc']
    
    def duplicar_obra(self, request, queryset):
        """Duplica las obras seleccionadas con todos sus registros relacionados"""
        for obra in queryset:
            # Guardar los registros relacionados antes de duplicar
            titulos_alt = list(obra.titulos_alternativos.all())
            ediciones = list(obra.ediciones.all())
            registros_264 = list(obra.produccion_publicacion.all())
            
            # Duplicar la obra principal
            obra.pk = None
            obra.num_control = None
            obra.save()
            
            # Duplicar títulos alternativos (campo 246)
            for titulo in titulos_alt:
                titulo.pk = None
                titulo.obra = obra
                titulo.save()
            
            # Duplicar ediciones (campo 250)
            for edicion in ediciones:
                edicion.pk = None
                edicion.obra = obra
                edicion.save()
            
            # Duplicar registros 264
            for registro in registros_264:
                registro.pk = None
                registro.obra = obra
                registro.save()
        
        self.message_user(
            request,
            f"✅ {queryset.count()} obra(s) duplicada(s) con todos sus registros relacionados "
            f"(246, 250, 264)"
        )
    
    duplicar_obra.short_description = "Duplicar obras seleccionadas"
    
    def exportar_marc(self, request, queryset):
        """Exportar registros en formato MARC21"""
        # TODO: Implementar exportación MARC21
        self.message_user(request, "Funcionalidad en desarrollo")
    
    exportar_marc.short_description = "Exportar a formato MARC21"
    
    # ------------------------------------------------
    # Métodos personalizados para la lista
    # ------------------------------------------------
    def get_punto_acceso_principal(self, obj):
        """Muestra el punto de acceso principal (100 o 130)"""
        if obj.compositor:
            return f"👤 {obj.compositor}"
        elif obj.titulo_uniforme:
            return f"🎵 {obj.titulo_uniforme}"
        return "⚠️ Sin punto de acceso"
    
    get_punto_acceso_principal.short_description = 'Punto de Acceso Principal'
    get_punto_acceso_principal.admin_order_field = 'compositor'
    
    # ------------------------------------------------
    # Validación adicional en el admin
    # ------------------------------------------------
    def save_model(self, request, obj, form, change):
        """Validaciones adicionales antes de guardar"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
            
            if obj.compositor:
                self.message_user(
                    request,
                    f"✅ Obra guardada con compositor: {obj.compositor}. Se usó campo 240.",
                    level='SUCCESS'
                )
            elif obj.titulo_uniforme:
                self.message_user(
                    request,
                    f"✅ Obra guardada con título uniforme: {obj.titulo_uniforme}. Se usó campo 130.",
                    level='SUCCESS'
                )
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
            raise
    
    # ------------------------------------------------
    # Optimización de consultas
    # ------------------------------------------------
    def get_queryset(self, request):
        """Optimizar consultas con select_related y prefetch_related"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'compositor',
            'titulo_uniforme',
            'titulo_uniforme_forma',
            'titulo_240',
            'titulo_240_forma'
        ).prefetch_related(
            'titulos_alternativos',  # ✅ Campo 246
            'ediciones',              # ✅ Campo 250
            'produccion_publicacion'  # ✅ Campo 264
        )
    
    # ------------------------------------------------
    # Información adicional en la página de cambio
    # ------------------------------------------------
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Agregar contexto adicional a la vista de edición"""
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        
        if obj:
            validaciones = []
            
            if obj.compositor and obj.titulo_uniforme:
                validaciones.append({
                    'tipo': 'error',
                    'mensaje': '⚠️ ERROR: No puede tener campo 100 (compositor) y 130 (título) simultáneamente'
                })
            
            if not obj.compositor and obj.titulo_240:
                validaciones.append({
                    'tipo': 'error',
                    'mensaje': '⚠️ ERROR: Campo 240 solo debe usarse cuando hay compositor en campo 100'
                })
            
            if obj.compositor and not obj.titulo_240:
                validaciones.append({
                    'tipo': 'warning',
                    'mensaje': '⚠️ ADVERTENCIA: Hay compositor (100) pero no hay título uniforme (240)'
                })
            
            if not obj.titulo_principal:
                validaciones.append({
                    'tipo': 'error',
                    'mensaje': '⚠️ ERROR: Campo 245 (título principal) es obligatorio'
                })
            
            extra_context['validaciones_marc'] = validaciones
        
        return super().change_view(request, object_id, form_url, extra_context)


# ================================================
# 🎨 PERSONALIZACIÓN ADICIONAL DEL ADMIN SITE
# ================================================

admin.site.site_header = "BLMP-UNL - Sistema de Catalogación Musical MARC21"
admin.site.site_title = "BLMP-UNL Admin"
admin.site.index_title = "Gestión de Obras Musicales Manuscritas e Impresas"
