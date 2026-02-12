"""
Mixins para vistas de obras MARC21.
Contiene funcionalidad compartida entre CrearObraView y EditarObraView.
"""

import logging

from django.contrib import messages

from catalogacion.forms.formsets import (
    CodigoLenguaFormSet,
    CodigoPaisEntidadFormSet,
    Contenido505FormSet,
    DatosBiograficos545FormSet,
    Disponible856FormSet,
    EdicionFormSet,
    EnlaceDocumentoFuente773FormSet,
    EnlaceUnidadConstituyente774FormSet,
    EntidadRelacionada710FormSet,
    # Bloque 1XX
    FuncionCompositorFormSet,
    # Bloque 0XX
    IncipitMusicalFormSet,
    # Bloque 6XX
    Materia650FormSet,
    MateriaGenero655FormSet,
    MedioInterpretacion382_aFormSet,
    # Bloque 3XX
    MedioInterpretacion382FormSet,
    # Bloque 4XX
    MencionSerie490FormSet,
    # Bloque 7XX
    NombreRelacionado700FormSet,
    # Bloque 5XX
    NotaGeneral500FormSet,
    OtrasRelaciones787FormSet,
    ProduccionPublicacionFormSet,
    Sumario520FormSet,
    # Bloque 2XX
    TituloAlternativoFormSet,
    Ubicacion852FormSet,
)
from catalogacion.models.bloque_5xx import DatosBiograficos545
from catalogacion.models.bloque_8xx import Disponible856
from catalogacion.views.obra_formset_handlers import SUBCAMPO_HANDLERS

# Configurar logger
logger = logging.getLogger("catalogacion")


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
            kwargs["data"] = self.request.POST
        if instance:
            kwargs["instance"] = instance
        # =======================================================
        # 🔥 PASAR COMPOSITOR A TODOS LOS FORMSETS 7XX
        # =======================================================

        return kwargs

    def _get_nested_formsets(self, parent_instances=None, with_post=False):
        """
        Obtener formsets anidados (formsets dentro de otros formsets).
        Actualmente solo el 382 tiene formsets anidados (el 382_a dentro del 382).

        Args:
            parent_instances: Lista de instancias padre (ej: instancias de MedioInterpretacion382)
            with_post: Si True, incluye datos POST

        Returns:
            dict: {'medios_formsets': [formset_382_a_0, formset_382_a_1, ...]}
        """
        nested = {}

        if parent_instances:
            medios_formsets = []
            for idx, parent_instance in enumerate(parent_instances):
                kwargs = {}
                if with_post:
                    kwargs["data"] = self.request.POST
                kwargs["instance"] = parent_instance

                formset = MedioInterpretacion382_aFormSet(
                    prefix=f"medios_interpretacion382_set-{idx}", **kwargs
                )
                medios_formsets.append(formset)

            nested["medios_formsets"] = medios_formsets

        return nested

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
            ubicacion_kwargs["instance"] = None
            disponible_kwargs["instance"] = None

        return {
            # Bloque 0XX - Números de control e información codificada
            "incipits_musicales": IncipitMusicalFormSet(prefix="incipits", **kwargs),
            "codigos_lengua": CodigoLenguaFormSet(prefix="lenguas", **kwargs),
            "codigos_pais": CodigoPaisEntidadFormSet(prefix="paises", **kwargs),
            # Bloque 1XX - Encabezamiento principal
            "funciones_compositor": FuncionCompositorFormSet(
                prefix="funciones", **kwargs
            ),
            # Bloque 2XX - Títulos y menciones de edición/publicación
            "titulos_alternativos": TituloAlternativoFormSet(
                prefix="titulos_alt", **kwargs
            ),
            "ediciones": EdicionFormSet(prefix="ediciones", **kwargs),
            "produccion_publicacion": ProduccionPublicacionFormSet(
                prefix="produccion", **kwargs
            ),
            # Bloque 3XX - Descripción física
            "medios_interpretacion": MedioInterpretacion382FormSet(
                prefix="medios_382", **kwargs
            ),
            # Bloque 4XX - Mención de serie
            "menciones_serie_490": MencionSerie490FormSet(
                prefix="menciones_490", **kwargs
            ),
            # Bloque 5XX - Notas
            "notas_generales": NotaGeneral500FormSet(prefix="notas_500", **kwargs),
            "contenidos": Contenido505FormSet(prefix="contenidos_505", **kwargs),
            "sumarios": Sumario520FormSet(prefix="sumarios_520", **kwargs),
            "datos_biograficos": DatosBiograficos545FormSet(
                prefix="biograficos_545", **kwargs
            ),
            # Bloque 6XX - Encabezamientos de materia
            "materias_650": Materia650FormSet(prefix="materias_650", **kwargs),
            "materias_genero_655": MateriaGenero655FormSet(
                prefix="generos_655", **kwargs
            ),
            # Bloque 7XX - Asientos secundarios
            "nombres_relacionados_700": NombreRelacionado700FormSet(
                prefix="nombres_700", **kwargs
            ),
            "entidades_relacionadas_710": EntidadRelacionada710FormSet(
                prefix="entidades_710", **kwargs
            ),
            "enlaces_documento_fuente_773": EnlaceDocumentoFuente773FormSet(
                prefix="enlaces_773", **kwargs
            ),
            "enlaces_unidad_constituyente_774": EnlaceUnidadConstituyente774FormSet(
                prefix="enlaces_774", **kwargs
            ),
            "otras_relaciones_787": OtrasRelaciones787FormSet(
                prefix="relaciones_787", **kwargs
            ),
            # Bloque 8XX - Números y códigos alternativos
            "ubicaciones_852": Ubicacion852FormSet(
                prefix="ubicaciones_852", **ubicacion_kwargs
            ),
            "disponibles_856": Disponible856FormSet(
                prefix="disponibles_856", **disponible_kwargs
            ),
        }

    def _get_formset_names(self):
        """
        Obtener lista de nombres de formsets.

        Returns:
            list: Lista de nombres de formsets
        """
        return [
            "incipits_musicales",
            "codigos_lengua",
            "codigos_pais",
            "funciones_compositor",
            "titulos_alternativos",
            "ediciones",
            "produccion_publicacion",
            "medios_interpretacion",
            "menciones_serie_490",
            "notas_generales",
            "contenidos",
            "sumarios",
            "datos_biograficos",
            "materias_650",
            "materias_genero_655",
            "nombres_relacionados_700",
            "entidades_relacionadas_710",
            "enlaces_documento_fuente_773",
            "enlaces_unidad_constituyente_774",
            "otras_relaciones_787",
            "ubicaciones_852",
            "disponibles_856",
        ]

    def _validar_formsets(self, context):
        """
        Validar todos los formsets en el contexto.

        Returns:
            tuple: (formsets_validos: bool, formsets: dict)
        """
        logger.info("🔍 Iniciando validación de formsets...")

        formsets_validos = True
        formsets = {}

        formsets_inhabilitados = {
            "codigos_lengua",
        }

        formsets_visibles = context.get("formsets_visibles")
        if not formsets_visibles:
            formsets_visibles = [
                name
                for name in self._get_formset_names()
                if name not in formsets_inhabilitados
            ]

        formsets_opcionales = {
            "incipits_musicales": "incipits-TOTAL_FORMS",
            "menciones_serie_490": "menciones_490-TOTAL_FORMS",
            "contenidos": "contenidos_505-TOTAL_FORMS",
            "enlaces_documento_fuente_773": "enlaces_773-TOTAL_FORMS",
            "enlaces_unidad_constituyente_774": "enlaces_774-TOTAL_FORMS",
            "otras_relaciones_787": "relaciones_787-TOTAL_FORMS",
            "titulos_alternativos": "titulos_alt-TOTAL_FORMS",
            "ediciones": "ediciones-TOTAL_FORMS",
        }

        for key in self._get_formset_names():
            if key in formsets_inhabilitados:
                logger.debug(f"  ⏭️  {key}: SALTADO (inhabilitado en UI V2)")
                continue
            
            if key == "codigos_pais":
                logger.info(f"  🔍 PROCESANDO {key}: Campo 044 de países")

            formset = context.get(key)

            # 🚨 IGNORAR FORMSETS NO VISIBLES (aunque tengan datos en POST)
            if key not in formsets_visibles:
                logger.debug(
                    f"  ⏭️  {key}: SALTADO COMPLETAMENTE (no visible en este tipo de obra)"
                )
                continue

            if key in formsets_opcionales:
                mgmt_field = formsets_opcionales[key]
                if mgmt_field not in self.request.POST:
                    logger.debug(f"  ⏭️  {key}: SALTADO (no está en el POST/template)")
                    continue

            if not formset:
                continue

            # ⚠️ 856 se maneja por subcampos JS → no usar has_changed
            if key == "disponibles_856":
                # Comprobamos si hay algún cambio en los campos $u o $y en el POST
                hay_urls = any(
                    k.startswith("url_disponible_856_")
                    for k in self.request.POST.keys()
                )
                hay_textos = any(
                    k.startswith("texto_disponible_856_")
                    for k in self.request.POST.keys()
                )

                if not hay_urls and not hay_textos:
                    logger.debug("⏭️  disponibles_856: sin URLs ni textos, se omite")
                    continue
            else:
                # 🔥 CASO ESPECIAL 264: Guardar si hay subcampos aunque el principal esté vacío
                if key == "produccion_publicacion":
                    # Verificar si hay datos en subcampos del POST
                    tiene_lugares = any(k.startswith("lugar_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                    tiene_entidades = any(k.startswith("entidad_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                    tiene_fechas = any(k.startswith("fecha_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                    
                    print(f"🔥 DEBUG VALIDACIÓN 264: lugares={tiene_lugares}, entidades={tiene_entidades}, fechas={tiene_fechas}")
                    
                    # Mostrar todos los keys del POST relacionados con 264
                    keys_264 = [k for k in self.request.POST.keys() if any(x in k for x in ["lugar_produccion_264_", "entidad_produccion_264_", "fecha_produccion_264_"])]
                    print(f"🔥 DEBUG VALIDACIÓN 264: keys encontrados={keys_264}")
                    
                    if tiene_lugares or tiene_entidades or tiene_fechas:
                        logger.info(f"  🔥 264: GUARDAR POR SUBCAMPOS (lugares={tiene_lugares}, entidades={tiene_entidades}, fechas={tiene_fechas})")
                        # Forzar guardado aunque el principal esté vacío
                        pass
                    elif all(not form.has_changed() for form in formset.forms):
                        logger.debug(f"  ⏭️  {key}: SALTADO (todos los formularios vacíos)")
                        continue
                elif all(not form.has_changed() for form in formset.forms):
                    logger.debug(f"  ⏭️  {key}: SALTADO (todos los formularios vacíos)")
                    continue

            formsets[key] = formset

            # 856 se valida/guarda manualmente (borra y recrea), no usar is_valid()
            if key == "disponibles_856":
                logger.debug(f"  ✅ {key}: VÁLIDO (validación manual por subcampos)")
                continue

            if formset.is_valid():
                logger.debug(f"  ✅ {key}: VÁLIDO")
            else:
                logger.error(f"  ❌ FORMSET INVÁLIDO: {key}")
                formsets_validos = False

                for i, form in enumerate(formset.forms):
                    if form.errors:
                        logger.error(f"     ➤ Formulario #{i}: {form.errors}")

                if hasattr(formset, "deleted_objects"):
                    logger.debug(
                        f"     Deleted objects: {len(formset.deleted_objects)}"
                    )

        # 🔥 RETURN ÚNICO Y SEGURO
        logger.info(
            f"✅ Resultado final: {'TODOS VÁLIDOS' if formsets_validos else 'HAY ERRORES'}"
        )
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
            "produccion_publicacion": [
                "_save_lugares_264",
                "_save_entidades_264",
                "_save_fechas_264",
            ],
            "medios_interpretacion": ["_save_medios_382"],
            "menciones_serie_490": ["_save_titulos_490", "_save_volumenes_490"],
            "ubicaciones_852": ["_save_estanterias_852"],
            "disponibles_856": ["_save_urls_856", "_save_textos_enlace_856"],
            "materias_650": ["_save_subdivisiones_650", "_save_subdivisiones_geograficas_650"],
            "materias_genero_655": ["_save_subdivisiones_655"],
        }

        for key, formset in formsets.items():
            # 🔥 1) GUARDAR PADRES 856 ANTES QUE NADA
            if key == "disponibles_856":
                # Limpiar los registros previos en edición para evitar duplicados
                if getattr(instance, "pk", None):
                    eliminados, _ = instance.disponibles_856.all().delete()
                    logger.info(f"🧹 Registros 856 previos eliminados: {eliminados}")

                disponibles_creados = []

                total_forms = int(
                    self.request.POST.get("disponibles_856-TOTAL_FORMS", 0)
                )

                for i in range(total_forms):
                    prefix_url = f"url_disponible_856_{i}_"
                    prefix_texto = f"texto_disponible_856_{i}_"

                    tiene_urls = any(
                        key.startswith(prefix_url)
                        and self.request.POST.get(key, "").strip()
                        for key in self.request.POST.keys()
                    )

                    tiene_textos = any(
                        key.startswith(prefix_texto)
                        and self.request.POST.get(key, "").strip()
                        for key in self.request.POST.keys()
                    )

                    if self.request.POST.get(f"disponibles_856-{i}-DELETE"):
                        continue

                    if not tiene_urls and not tiene_textos:
                        logger.debug(
                            "⏭️  856-%s omitido: sin URLs ni textos de enlace", i
                        )
                        continue

                    disponible = Disponible856.objects.create(obra=instance)
                    disponibles_creados.append(disponible)

                logger.info(f"🟢 856 padres creados: {len(disponibles_creados)}")
                # 🔥 LLAMADAS CORRECTAS A LOS HANDLERS
                disponibles_para_urls = list(disponibles_creados)
                disponibles_para_textos = list(disponibles_creados)

                # 🔥 LLAMADAS CORRECTAS A LOS HANDLERS
                SUBCAMPO_HANDLERS["_save_urls_856"](
                    self.request.POST,
                    # disponibles_creados
                    disponibles_para_urls,
                )

                SUBCAMPO_HANDLERS["_save_textos_enlace_856"](
                    self.request.POST,
                    # disponibles_creados
                    disponibles_para_textos,
                )

                continue

            # ---------------------------
            # 🔥 CASO ESPECIAL 545: OneToOneField requiere update_or_create
            # ---------------------------
            if key == "datos_biograficos":
                for form in formset:
                    if getattr(form, "cleaned_data", None) and not form.cleaned_data.get(
                        "DELETE", False
                    ):
                        texto = form.cleaned_data.get("texto_biografico", "")
                        uri = form.cleaned_data.get("uri", "")

                        # Si ambos campos están vacíos, eliminar el registro existente
                        if not texto and not uri:
                            DatosBiograficos545.objects.filter(obra=instance).delete()
                            logger.info(f"🗑️ 545: Datos biográficos eliminados para obra {instance.pk}")
                        else:
                            # Usar update_or_create para manejar OneToOneField correctamente
                            obj, created = DatosBiograficos545.objects.update_or_create(
                                obra=instance,
                                defaults={
                                    "texto_biografico": texto,
                                    "uri": uri,
                                }
                            )
                            action = "creado" if created else "actualizado"
                            logger.info(f"📝 545: Datos biográficos {action} para obra {instance.pk}")
                    elif getattr(form, "cleaned_data", None) and form.cleaned_data.get("DELETE", False):
                        # Si se marcó para eliminar
                        DatosBiograficos545.objects.filter(obra=instance).delete()
                        logger.info(f"🗑️ 545: Datos biográficos eliminados (DELETE) para obra {instance.pk}")
                continue

            # ---------------------------
            # Guardado NORMAL para otros formsets
            # ---------------------------
            for form in formset:
                if getattr(form, "cleaned_data", None) and not form.cleaned_data.get(
                    "DELETE", False
                ):
                    obj = form.save(commit=False)

                    # 🔥 Asignar FK a la obra
                    if hasattr(obj, "obra_general"):
                        obj.obra_general = instance
                    elif hasattr(obj, "obra"):
                        obj.obra = instance

                    # 🔥 CASO ESPECIAL 264: Si el formulario está vacío pero hay subcampos, crear de todos modos
                    if key == "produccion_publicacion" and not form.has_changed():
                        # Verificar si hay subcampos en el POST
                        tiene_lugares = any(k.startswith("lugar_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                        tiene_entidades = any(k.startswith("entidad_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                        tiene_fechas = any(k.startswith("fecha_produccion_264_") and self.request.POST.get(k, "").strip() for k in self.request.POST.keys())
                        
                        if tiene_lugares or tiene_entidades or tiene_fechas:
                            logger.info(f"  🔥 264: CREANDO ProduccionPublicacion vacía para subcampos")
                            # Forzar la creación aunque esté vacía
                            obj.funcion = '0'  # Valor por defecto para manuscritos
                            logger.info(f"  📝 264: ProduccionPublicacion creada con función='{obj.funcion}'")

                    obj.save()
                    
                    # Log específico para países
                    if key == "codigos_pais":
                        logger.info(f"🌍 PAÍS GUARDADO: {obj.codigo_pais} - Obra: {obj.obra.num_control}")
                    
                    logger.info(f"📝 Guardado formset {key}: {obj.pk}")

                    # ------------------------------
                    # 🔥 Subcampos 852$c
                    # ------------------------------
                    if hasattr(obj, "estanterias"):
                        for sub in obj.estanterias.all():
                            if sub.ubicacion_id is None:
                                sub.ubicacion = obj
                                sub.save()

                    # ------------------------------
                    # 🔥 Subcampos 856$u y 856$y
                    # ------------------------------
                    if hasattr(obj, "urls_856"):
                        for sub in obj.urls_856.all():
                            if sub.disponible_id is None:
                                sub.disponible = obj
                                sub.save()

                    if hasattr(obj, "textos_enlace_856"):
                        for sub in obj.textos_enlace_856.all():
                            if sub.disponible_id is None:
                                sub.disponible = obj
                                sub.save()

            if key == "incipits_musicales":
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
                        incipit.clave or "-",
                        incipit.armadura or "-",
                        incipit.tiempo or "-",
                    )

            # Procesar subcampos dinámicos si el formset los tiene
            if key in formset_subcampo_mapping:
                for handler_name in formset_subcampo_mapping[key]:
                    handler = SUBCAMPO_HANDLERS[handler_name]
                    # 🔥 CASO ESPECIAL 264: Pasar la obra como parámetro
                    if key == "produccion_publicacion":
                        handler(self.request.POST, formset, instance)
                    else:
                        handler(self.request.POST, formset)


class ObraSuccessMessageMixin:
    """
    Mixin para manejar mensajes de éxito en operaciones de obras.
    """

    def _get_success_message(self, action="publish"):
        """
        Obtener mensaje de éxito según la acción.

        Args:
            action: Acción realizada ('publish', 'draft', 'update')

        Returns:
            str: Mensaje de éxito
        """
        config = getattr(self, "config_obra", {})
        titulo_tipo = config.get("titulo", "Obra")

        mensajes = {
            "draft": f"Borrador de {titulo_tipo} guardado exitosamente.",
            "publish": f"{titulo_tipo} creada exitosamente.",
            "update": f"{titulo_tipo} actualizada exitosamente.",
        }

        return mensajes.get(action, "Operación exitosa.")

    def _mostrar_mensaje_exito(self, action="publish"):
        """
        Mostrar mensaje de éxito.

        Args:
            action: Acción realizada
        """
        mensaje = self._get_success_message(action)
        messages.success(self.request, mensaje)
