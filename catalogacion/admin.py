# from django.contrib import admin
# from django.utils.html import format_html
# from django.db import models
# from django.forms import TextInput, Textarea, Select, NumberInput
# from .models import (
#     ObraGeneral,
#     AutoridadPersona,
#     AutoridadTituloUniforme,
#     AutoridadFormaMusical,
#     AutoridadMateria,
#     TituloAlternativo,
#     Edicion,
#     ProduccionPublicacion,
#     DescripcionFisica
# )

# # ================================================
# # 📚 ADMINISTRACIÓN DE TABLAS DE AUTORIDADES
# # ================================================

# @admin.register(AutoridadPersona)
# class AutoridadPersonaAdmin(admin.ModelAdmin):
#     """Gestión de nombres de personas normalizados"""
#     list_display = ['apellidos_nombres', 'fechas', 'num_obras', 'fecha_creacion']
#     search_fields = ['apellidos_nombres', 'fechas']
#     list_filter = ['fecha_creacion']
#     ordering = ['apellidos_nombres']
    
#     fieldsets = (
#         ('Información de la Persona', {
#             'fields': ('apellidos_nombres', 'fechas'),
#             'description': 'Formato: Apellidos, Nombres | Fechas: año nacimiento - año muerte'
#         }),
#     )
    
#     def num_obras(self, obj):
#         """Mostrar cantidad de obras donde se usa este compositor"""
#         count = obj.obras_como_compositor.count()
#         return format_html(f'<span style="background-color: #d4edda; padding: 3px 8px; border-radius: 3px;"><strong>{count}</strong> obras</span>')
#     num_obras.short_description = '📊 Obras registradas'


# @admin.register(AutoridadTituloUniforme)
# class AutoridadTituloUniformeAdmin(admin.ModelAdmin):
#     """Gestión de títulos uniformes normalizados"""
#     list_display = ['titulo', 'usos_130', 'usos_240', 'fecha_creacion']
#     search_fields = ['titulo']
#     list_filter = ['fecha_creacion']
#     ordering = ['titulo']
    
#     def usos_130(self, obj):
#         """Contar usos en campo 130"""
#         count = obj.obras_130.count()
#         if count > 0:
#             return format_html(f'<span style="background-color: #cfe2ff; padding: 3px 8px; border-radius: 3px;"><strong>{count}</strong></span>')
#         return "-"
#     usos_130.short_description = '📌 Campo 130'
    
#     def usos_240(self, obj):
#         """Contar usos en campo 240"""
#         count = obj.obras_240.count()
#         if count > 0:
#             return format_html(f'<span style="background-color: #d1ecf1; padding: 3px 8px; border-radius: 3px;"><strong>{count}</strong></span>')
#         return "-"
#     usos_240.short_description = '📌 Campo 240'


# @admin.register(AutoridadFormaMusical)
# class AutoridadFormaMusicalAdmin(admin.ModelAdmin):
#     """Gestión de formas musicales"""
#     list_display = ['forma', 'usos_130', 'usos_240', 'usos_655', 'fecha_creacion']
#     search_fields = ['forma']
#     list_filter = ['fecha_creacion']
#     ordering = ['forma']
    
#     def usos_130(self, obj):
#         count = obj.obras_130_forma.count()
#         return f"{count}" if count > 0 else "-"
#     usos_130.short_description = 'Campo 130 $k'
    
#     def usos_240(self, obj):
#         count = obj.obras_240_forma.count()
#         return f"{count}" if count > 0 else "-"
#     usos_240.short_description = 'Campo 240 $k'
    
#     def usos_655(self, obj):
#         return "-"  # Para cuando implantes campo 655
#     usos_655.short_description = 'Campo 655'


# @admin.register(AutoridadMateria)
# class AutoridadMateriaAdmin(admin.ModelAdmin):
#     """Gestión de términos de materia"""
#     list_display = ['termino', 'fecha_creacion']
#     search_fields = ['termino']
#     list_filter = ['fecha_creacion']
#     ordering = ['termino']


# # ================================================
# # 📌 INLINES PARA CAMPOS REPETIBLES
# # ================================================

# class TituloAlternativoInline(admin.TabularInline):
#     """Inline para campo 246 - Títulos Alternativos"""
#     model = TituloAlternativo
#     extra = 1
#     fields = ['titulo', 'resto_titulo']
#     verbose_name_plural = "246 - Títulos Alternativos"


# class EdicionInline(admin.TabularInline):
#     """Inline para campo 250 - Ediciones"""
#     model = Edicion
#     extra = 1
#     fields = ['edicion']
#     verbose_name_plural = "250 - Ediciones"


# class ProduccionPublicacionInline(admin.TabularInline):
#     """Inline para campo 264 - Producción/Publicación"""
#     model = ProduccionPublicacion
#     extra = 1
#     fields = ['funcion', 'lugar', 'nombre_entidad', 'fecha']
#     verbose_name_plural = "264 - Producción/Publicación/Distribución/Fabricación/Copyright"


# class DescripcionFisicaInline(admin.TabularInline):
#     """Inline para campo 300 - Descripciones Físicas"""
#     model = DescripcionFisica
#     extra = 1
#     fields = ['extension', 'otras_caracteristicas_fisicas', 'dimensiones', 'material_acompanante']
#     verbose_name_plural = "300 - Descripciones Físicas"


# # ================================================
# # 📄 ADMINISTRACIÓN PRINCIPAL - OBRA GENERAL
# # ================================================

# @admin.register(ObraGeneral)
# class ObraGeneralAdmin(admin.ModelAdmin):
#     """Administración de Obras Musicales MARC21"""
    
#     list_display = [
#         'num_control_display',
#         'punto_acceso_principal',
#         'tipo_registro_display',
#         'codigo_lengua_display',
#         'fecha_creacion_sistema'
#     ]
    
#     search_fields = [
#         'num_control',
#         'compositor__apellidos_nombres',
#         'titulo_uniforme__titulo',
#         'titulo_240__titulo',
#         'titulo_principal'
#     ]
    
#     list_filter = [
#         'tipo_registro',
#         'nivel_bibliografico',
#         'codigo_lengua',
#         'codigo_pais',
#         'fecha_creacion_sistema'
#     ]
    
#     ordering = ['-num_control']
#     date_hierarchy = 'fecha_creacion_sistema'
    
#     # Inlines para campos repetibles
#     inlines = [
#         ProduccionPublicacionInline,
#         DescripcionFisicaInline,
#         TituloAlternativoInline,
#         EdicionInline
#     ]
    
#     # Fieldsets para organizar la información
#     fieldsets = (
#         ('🟩 Cabecera o Líder', {
#             'fields': ('tipo_registro', 'nivel_bibliografico'),
#             'classes': ('wide',)
#         }),
        
#         ('🟨 Bloque 0XX - Identificadores', {
#             'fields': (
#                 ('isbn', 'ismn'),
#                 ('numero_editor', 'indicador_028'),
#                 'centro_catalogador',
#                 ('codigo_lengua', 'codigo_pais'),
#             ),
#             'classes': ('collapse',)
#         }),
        
#         ('🟨 Bloque 0XX - Íncipit Musical (031)', {
#             'fields': (
#                 ('incipit_num_obra', 'incipit_num_movimiento', 'incipit_num_pasaje'),
#                 'incipit_titulo',
#                 'incipit_voz_instrumento',
#                 'incipit_notacion',
#                 'incipit_url'
#             ),
#             'classes': ('collapse',)
#         }),
        
#         ('🟨 Bloque 0XX - Clasificación Local (092)', {
#             'fields': (
#                 'clasif_institucion',
#                 'clasif_proyecto',
#                 'clasif_pais',
#                 'clasif_ms_imp'
#             ),
#             'classes': ('collapse',)
#         }),
        
#         ('🟦 Bloque 1XX - Compositor (Campo 100)', {
#             'fields': (
#                 'compositor',
#                 ('compositor_funcion', 'compositor_autoria')
#             ),
#             'description': '⚠️ Si hay compositor aquí, use campo 240 abajo, NO use campo 130'
#         }),
        
#         ('🟦 Bloque 1XX - Título Uniforme Principal (Campo 130)', {
#             'fields': (
#                 'titulo_uniforme',
#                 'titulo_uniforme_forma',
#                 'titulo_uniforme_medio_interpretacion',
#                 ('titulo_uniforme_num_parte', 'titulo_uniforme_tonalidad'),
#                 'titulo_uniforme_arreglo',
#                 'titulo_uniforme_nombre_parte'
#             ),
#             'description': '⚠️ Solo use este campo si NO hay compositor. Si hay compositor, use campo 240',
#             'classes': ('collapse',)
#         }),
        
#         ('🟩 Bloque 2XX - Título Uniforme con Compositor (Campo 240)', {
#             'fields': (
#                 'titulo_240',
#                 'titulo_240_forma',
#                 'titulo_240_medio_interpretacion',
#                 ('titulo_240_num_parte', 'titulo_240_tonalidad'),
#                 'titulo_240_arreglo',
#                 'titulo_240_nombre_parte'
#             ),
#             'description': '⚠️ Solo use este campo si HAY compositor. Si no hay, use campo 130',
#             'classes': ('collapse',)
#         }),
        
#         ('🟩 Bloque 2XX - Título Principal (Campo 245)', {
#             'fields': (
#                 'titulo_principal',
#                 'subtitulo',
#                 'mencion_responsabilidad'
#             )
#         }),
        
#         ('📚 Campos Repetibles (Inlines arriba)', {
#             'fields': (),
#             'description': 'Campo 246 - Títulos Alternativos | Campo 250 - Ediciones | Campo 264 - Producción/Publicación | Campo 300 - Descripción Física'
#         }),
        
#         ('🔧 Campos Automáticos (Solo Lectura)', {
#             'fields': (
#                 'num_control',
#                 'estado_registro',
#                 'fecha_hora_ultima_transaccion',
#                 'codigo_informacion',
#                 'clasif_num_control',
#                 'fecha_creacion_sistema',
#                 'fecha_modificacion_sistema'
#             ),
#             'classes': ('collapse', 'wide'),
#             'description': 'Estos campos se generan automáticamente'
#         })
#     )
    
#     # Campos solo lectura
#     readonly_fields = (
#         'num_control',
#         'estado_registro',
#         'fecha_hora_ultima_transaccion',
#         'codigo_informacion',
#         'clasif_num_control',
#         'fecha_creacion_sistema',
#         'fecha_modificacion_sistema'
#     )
    
#     # Personalizar widgets
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size': '80'})},
#         models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
#     }
    
#     def num_control_display(self, obj):
#         """Mostrar número de control con color"""
#         return format_html(
#             '<span style="background-color: #d4edda; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
#             obj.num_control
#         )
#     num_control_display.short_description = '📄 Nº Control'
    
#     def punto_acceso_principal(self, obj):
#         """Mostrar el punto de acceso principal (100 o 130)"""
#         if obj.compositor:
#             return format_html(
#                 '👤 <strong>{}</strong>',
#                 obj.compositor.apellidos_nombres
#             )
#         elif obj.titulo_uniforme:
#             return format_html(
#                 '🎵 <strong>{}</strong>',
#                 obj.titulo_uniforme.titulo
#             )
#         return "❌ Sin punto de acceso"
#     punto_acceso_principal.short_description = 'Punto de Acceso Principal'
    
#     def tipo_registro_display(self, obj):
#         """Mostrar tipo de registro con icono"""
#         if obj.tipo_registro == 'c':
#             return format_html('<span style="color: green;">📖 Impreso</span>')
#         else:
#             return format_html('<span style="color: blue;">✍️ Manuscrito</span>')
#     tipo_registro_display.short_description = 'Tipo'
    
#     def codigo_lengua_display(self, obj):
#         """Mostrar código de lengua con etiqueta"""
#         return obj.get_codigo_lengua_display()
#     codigo_lengua_display.short_description = 'Idioma'
    
#     # Acciones personalizadas
#     actions = ['duplicar_obra', 'cambiar_a_impreso', 'cambiar_a_manuscrito']
    
#     def duplicar_obra(self, request, queryset):
#         """Duplicar una obra sin número de control"""
#         for obra in queryset:
#             obra.id = None
#             obra.num_control = None
#             obra.save()
#         self.message_user(request, f"✅ {queryset.count()} obra(s) duplicada(s) exitosamente")
#     duplicar_obra.short_description = "📋 Duplicar obra seleccionada"
    
#     def cambiar_a_impreso(self, request, queryset):
#         """Cambiar tipo de registro a impreso"""
#         queryset.update(tipo_registro='c')
#         self.message_user(request, f"✅ {queryset.count()} obra(s) cambiada(s) a impreso")
#     cambiar_a_impreso.short_description = "📖 Cambiar a Impreso"
    
#     def cambiar_a_manuscrito(self, request, queryset):
#         """Cambiar tipo de registro a manuscrito"""
#         queryset.update(tipo_registro='d')
#         self.message_user(request, f"✅ {queryset.count()} obra(s) cambiada(s) a manuscrito")
#     cambiar_a_manuscrito.short_description = "✍️ Cambiar a Manuscrito"
    
#     def save_model(self, request, obj, form, change):
#         """Guardar modelo ejecutando validaciones"""
#         obj.full_clean()  # Ejecutar validaciones del modelo
#         super().save_model(request, obj, form, change)
        
#     def get_readonly_fields(self, request, obj=None):
#         """Hacer campos readonly solo al editar"""
#         if obj:  # Si existe el objeto (está siendo editado)
#             return self.readonly_fields + ('estado_registro', 'tipo_registro')
#         return self.readonly_fields
