"""
Mixins para vistas de obras MARC21.
Contiene funcionalidad compartida entre CrearObraView y EditarObraView.
"""
import logging
from django.contrib import messages
from django.db import transaction

from catalogacion.forms.formsets import (
    # Bloque 0XX
    IncipitMusicalFormSet, CodigoLenguaFormSet, CodigoPaisEntidadFormSet,
    # Bloque 1XX  
    FuncionCompositorFormSet,
    # Bloque 2XX
    TituloAlternativoFormSet, EdicionFormSet, ProduccionPublicacionFormSet,
    # Bloque 3XX
    MedioInterpretacion382FormSet,
    # Bloque 4XX
    MencionSerie490FormSet,
    # Bloque 5XX
    NotaGeneral500FormSet, Contenido505FormSet, Sumario520FormSet, DatosBiograficos545FormSet,
    # Bloque 6XX
    Materia650FormSet, MateriaGenero655FormSet,
    # Bloque 7XX
    NombreRelacionado700FormSet,
    EntidadRelacionada710FormSet,
    EnlaceDocumentoFuente773FormSet,
    NumeroControl773FormSet,
    EnlaceUnidadConstituyente774FormSet,
    NumeroControl774FormSet,
    OtrasRelaciones787FormSet,
    NumeroControl787FormSet,
    # Bloque 8XX
    Ubicacion852FormSet,
    Disponible856FormSet,
)
from catalogacion.views.obra_formset_handlers import SUBCAMPO_HANDLERS

# Configurar logger
logger = logging.getLogger('catalogacion')


class ObraFormsetMixin:
    """
    Mixin que proporciona funcionalidad de formsets para vistas de obras.
    Maneja la inicialización y guardado de todos los formsets MARC21.
    """
    
    def _get_formsets_kwargs(self, instance=None, with_post=False):
        """
        Obtener kwargs comunes para todos los formsets.
        
        Args:
            instance: Instancia de ObraGeneral (None para crear, self.object para editar)
            with_post: Si True, incluye request.POST en kwargs
        
        Returns:
            dict: kwargs base para formsets
        """
        kwargs = {}
        if with_post:
            kwargs['data'] = self.request.POST
        if instance:
            kwargs['instance'] = instance
        return kwargs
    
    def _get_formsets(self, instance=None, with_post=False):
        """
        Obtener todos los formsets configurados.
        
        Args:
            instance: Instancia de ObraGeneral (None para crear, self.object para editar)
            with_post: Si True, incluye datos POST
        
        Returns:
            dict: Diccionario con todos los formsets configurados
        """
        kwargs = self._get_formsets_kwargs(instance, with_post)
        
        # Para formsets sin instancia (crear), pasamos instance=None explícitamente
        ubicacion_kwargs = kwargs.copy()
        disponible_kwargs = kwargs.copy()
        
        if not instance:
            ubicacion_kwargs['instance'] = None
            disponible_kwargs['instance'] = None
        
        return {
            # Bloque 0XX - Números de control e información codificada
            'incipits_musicales': IncipitMusicalFormSet(prefix='incipits', **kwargs),
            'codigos_lengua': CodigoLenguaFormSet(prefix='lenguas', **kwargs),
            'codigos_pais': CodigoPaisEntidadFormSet(prefix='paises', **kwargs),
            
            # Bloque 1XX - Encabezamiento principal
            'funciones_compositor': FuncionCompositorFormSet(prefix='funciones', **kwargs),
            
            # Bloque 2XX - Títulos y menciones de edición/publicación
            'titulos_alternativos': TituloAlternativoFormSet(prefix='titulos_alt', **kwargs),
            'ediciones': EdicionFormSet(prefix='ediciones', **kwargs),
            'produccion_publicacion': ProduccionPublicacionFormSet(prefix='produccion', **kwargs),
            
            # Bloque 3XX - Descripción física
            'medios_interpretacion': MedioInterpretacion382FormSet(prefix='medios_382', **kwargs),
            
            # Bloque 4XX - Mención de serie
            'menciones_serie_490': MencionSerie490FormSet(prefix='menciones_490', **kwargs),
            
            # Bloque 5XX - Notas
            'notas_generales': NotaGeneral500FormSet(prefix='notas_500', **kwargs),
            'contenidos': Contenido505FormSet(prefix='contenidos_505', **kwargs),
            'sumarios': Sumario520FormSet(prefix='sumarios_520', **kwargs),
            'datos_biograficos': DatosBiograficos545FormSet(prefix='biograficos_545', **kwargs),
            
            # Bloque 6XX - Encabezamientos de materia
            'materias_650': Materia650FormSet(prefix='materias_650', **kwargs),
            'materias_genero_655': MateriaGenero655FormSet(prefix='generos_655', **kwargs),
            
            # Bloque 7XX - Asientos secundarios
            'nombres_relacionados_700': NombreRelacionado700FormSet(prefix='nombres_700', **kwargs),
            'entidades_relacionadas_710': EntidadRelacionada710FormSet(prefix='entidades_710', **kwargs),
            'enlaces_documento_fuente_773': EnlaceDocumentoFuente773FormSet(prefix='enlaces_773', **kwargs),
            'enlaces_unidad_constituyente_774': EnlaceUnidadConstituyente774FormSet(prefix='enlaces_774', **kwargs),
            'otras_relaciones_787': OtrasRelaciones787FormSet(prefix='relaciones_787', **kwargs),
            
            # Bloque 8XX - Números y códigos alternativos
            'ubicaciones_852': Ubicacion852FormSet(prefix='ubicaciones_852', **ubicacion_kwargs),
            'disponibles_856': Disponible856FormSet(prefix='disponibles_856', **disponible_kwargs),
        }
    
    def _get_formset_names(self):
        """
        Obtener lista de nombres de formsets.
        
        Returns:
            list: Lista de nombres de formsets
        """
        return [
            'incipits_musicales', 'codigos_lengua', 'codigos_pais',
            'funciones_compositor', 'titulos_alternativos', 'ediciones',
            'produccion_publicacion', 'medios_interpretacion',
            'menciones_serie_490', 'notas_generales', 'contenidos',
            'sumarios', 'datos_biograficos', 'materias_650',
            'materias_genero_655', 'nombres_relacionados_700',
            'entidades_relacionadas_710', 'enlaces_documento_fuente_773',
            'enlaces_unidad_constituyente_774', 'otras_relaciones_787',
            'ubicaciones_852', 'disponibles_856',
        ]
    
    def _validar_formsets(self, context):
        """
        Validar todos los formsets en el contexto.
        
        Args:
            context: Contexto con formsets
        
        Returns:
            tuple: (formsets_validos: bool, formsets: dict)
        """
        logger.info("🔍 Iniciando validación de formsets...")
        formsets_validos = True
        formsets = {}

        formsets_visibles = context.get('formsets_visibles') or self._get_formset_names()

        # Formsets opcionales que NO deben validarse si no tienen datos POST
        formsets_opcionales = {
            'incipits_musicales': 'incipits-TOTAL_FORMS',
            'menciones_serie_490': 'menciones_490-TOTAL_FORMS',
            'contenidos': 'contenidos_505-TOTAL_FORMS',
            'enlaces_documento_fuente_773': 'enlaces_773-TOTAL_FORMS',
            'enlaces_unidad_constituyente_774': 'enlaces_774-TOTAL_FORMS',
            'otras_relaciones_787': 'relaciones_787-TOTAL_FORMS',
        }

        for key in self._get_formset_names():
            formset = context.get(key)
            
            if key not in formsets_visibles:
                logger.debug(f"  ⏭️  {key}: SALTADO (no está habilitado para este tipo de obra)")
                continue

            # Si es formset opcional y NO tiene ManagementForm en POST, saltarlo
            if key in formsets_opcionales:
                mgmt_field = formsets_opcionales[key]
                if mgmt_field not in self.request.POST:
                    logger.debug(f"  ⏭️  {key}: SALTADO (no está en el template)")
                    continue
            
            if formset:
                formsets[key] = formset
                is_valid = formset.is_valid()
                
                if is_valid:
                    logger.debug(f"  ✅ {key}: VÁLIDO")
                else:
                    logger.error(f"  ❌ {key}: INVÁLIDO")
                    logger.error(f"     Errores: {formset.errors}")
                    if hasattr(formset, 'non_form_errors') and formset.non_form_errors():
                        logger.error(f"     Errores no-form: {formset.non_form_errors()}")
                    formsets_validos = False
        
        logger.info(f"✅ Resultado final: {'TODOS VÁLIDOS' if formsets_validos else 'HAY ERRORES'}")
        return formsets_validos, formsets
    
    def _guardar_formsets(self, formsets, instance):
        """
        Guardar todos los formsets y procesar subcampos dinámicos.
        
        Args:
            formsets: Diccionario con formsets validados
            instance: Instancia de ObraGeneral guardada
        """
        # Mapeo de claves de formset a sus handlers de subcampos
        formset_subcampo_mapping = {
            'produccion_publicacion': ['_save_lugares_264', '_save_entidades_264', '_save_fechas_264'],
            'medios_interpretacion': ['_save_medios_382'],
            'menciones_serie_490': ['_save_titulos_490', '_save_volumenes_490'],
            'ubicaciones_852': ['_save_estanterias_852'],
            'disponibles_856': ['_save_urls_856', '_save_textos_enlace_856'],
            'materias_650': ['_save_subdivisiones_650'],
            'materias_genero_655': ['_save_subdivisiones_655'],
        }
        
        for key, formset in formsets.items():
            formset.instance = instance
            formset.save()

            if key == 'incipits_musicales':
                incipits_guardados = list(instance.incipits_musicales.all())
                logger.info(
                    "🎼 Campo 031: %s íncipit(s) guardado(s) para la obra %s",
                    len(incipits_guardados),
                    instance.pk,
                )
                for incipit in incipits_guardados:
                    logger.debug(
                        "   · Íncipit ID=%s | %s | Clave=%s | Armadura=%s | Tiempo=%s",
                        incipit.id,
                        incipit.identificador_completo,
                        incipit.clave or '-',
                        incipit.armadura or '-',
                        incipit.tiempo or '-',
                    )
            
            # Procesar subcampos dinámicos si el formset los tiene
            if key in formset_subcampo_mapping:
                for handler_name in formset_subcampo_mapping[key]:
                    handler = SUBCAMPO_HANDLERS[handler_name]
                    handler(self.request.POST, formset)


class ObraSuccessMessageMixin:
    """
    Mixin para manejar mensajes de éxito en operaciones de obras.
    """
    
    def _get_success_message(self, action='publish'):
        """
        Obtener mensaje de éxito según la acción.
        
        Args:
            action: Acción realizada ('publish', 'draft', 'update')
        
        Returns:
            str: Mensaje de éxito
        """
        config = getattr(self, 'config_obra', {})
        titulo_tipo = config.get('titulo', 'Obra')
        
        mensajes = {
            'draft': f'Borrador de {titulo_tipo} guardado exitosamente.',
            'publish': f'{titulo_tipo} creada exitosamente.',
            'update': f'{titulo_tipo} actualizada exitosamente.',
        }
        
        return mensajes.get(action, 'Operación exitosa.')
    
    def _mostrar_mensaje_exito(self, action='publish'):
        """
        Mostrar mensaje de éxito.
        
        Args:
            action: Acción realizada
        """
        mensaje = self._get_success_message(action)
        messages.success(self.request, mensaje)
