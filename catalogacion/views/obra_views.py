"""
Views principales para gestión de obras MARC21.
Este módulo contiene las vistas CRUD para obras musicales siguiendo el estándar MARC21.
"""
import logging
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Q
from jsonschema import ValidationError
from catalogacion.forms.formsets import Funcion700FormSet
from catalogacion.models import (
    NumeroControl773,
    NumeroControl774,
    NumeroControl787,
)
from catalogacion.models import ObraGeneral
from catalogacion.forms import ObraGeneralForm
from catalogacion.views.obra_config import (
    TIPO_OBRA_CONFIG,
    get_campos_visibles,
    debe_mostrar_formset,
)
from catalogacion.views.obra_mixins import ObraFormsetMixin
from usuarios.mixins import CatalogadorRequiredMixin

# Configurar logger
logger = logging.getLogger('catalogacion')


class SeleccionarTipoObraView(CatalogadorRequiredMixin, TemplateView):
    """
    Vista para seleccionar el tipo de obra a catalogar.
    Presenta las opciones disponibles según la configuración MARC21.
    """
    template_name = 'catalogacion/seleccionar_tipo_obra.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_obra'] = TIPO_OBRA_CONFIG
        return context
    
    def post(self, request, *args, **kwargs):
        """Redirigir a la vista de creación con el tipo seleccionado"""
        tipo_obra = request.POST.get('tipo_obra')
        if tipo_obra in TIPO_OBRA_CONFIG:
            return redirect('catalogacion:crear_obra', tipo=tipo_obra)
        
        messages.error(request, 'Debe seleccionar un tipo de obra válido.')
        return self.get(request, *args, **kwargs)


def validar_autores_principales_y_secundarios(form_principal, formset_700):
    autor_100 = form_principal.cleaned_data.get("compositor")

    if not autor_100:
        return []  # No hay autor principal, no validar nada

    errores = []

    for f in formset_700:
        if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
            autor_700 = f.cleaned_data.get("nombre_relacionado")

            if autor_700 and autor_700 == autor_100:
                errores.append("El autor del campo 700 no puede ser igual al autor del 100.")

    return errores
class CrearObraView(CatalogadorRequiredMixin, ObraFormsetMixin, CreateView):
    """
    Vista para crear una nueva obra MARC21.
    Guarda correctamente formulario principal + formsets + formsets anidados.
    """

    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/crear_obra.html'

    # =====================================================
    # POST (solo logging / debug)
    # =====================================================
    def post(self, request, *args, **kwargs):
        logger.info("=" * 70)
        logger.info(f"📨 POST RECIBIDO: {len(request.POST)} campos")
        logger.info(f"tipo_obra: {kwargs.get('tipo')}")
        logger.info("=" * 70)
        return super().post(request, *args, **kwargs)

    # =====================================================
    # DISPATCH
    # =====================================================
    def dispatch(self, request, *args, **kwargs):
        self.tipo_obra = kwargs.get('tipo')

        if self.tipo_obra not in TIPO_OBRA_CONFIG:
            messages.error(request, 'Tipo de obra inválido.')
            return redirect('catalogacion:seleccionar_tipo')

        self.config_obra = TIPO_OBRA_CONFIG[self.tipo_obra]
        return super().dispatch(request, *args, **kwargs)

    # =====================================================
    # FORM KWARGS
    # =====================================================
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == 'GET':
            kwargs['initial'] = {
                'tipo_registro': self.config_obra['tipo_registro'],
                'nivel_bibliografico': self.config_obra['nivel_bibliografico'],
            }
        return kwargs

    # =====================================================
    # CONTEXT
    # =====================================================
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tipo_obra'] = self.tipo_obra
        context['tipo_obra_titulo'] = self.config_obra['titulo']
        context['tipo_obra_descripcion'] = self.config_obra['descripcion']

        # Borradores: si se viene de "recuperar borrador", se guarda en sesión
        context['borrador_id_recuperar'] = self.request.session.get('borrador_id')

        campos_config = get_campos_visibles(self.tipo_obra)
        context['campos_visibles'] = campos_config['campos_simples']
        context['formsets_visibles'] = campos_config['formsets_visibles']

        with_post = self.request.method == 'POST'
        formsets = self._get_formsets(instance=None, with_post=with_post)

        for key, fs in formsets.items():
            context[key] = fs
        # =====================================================
        # 🔥 INLINE FORMSET 700 $e – Función
        # =====================================================
        formset_700 = formsets.get("nombres_relacionados_700") or formsets.get("700")

        if formset_700:
            for form in formset_700:
                form.funcion700_formset = Funcion700FormSet(
                    instance=form.instance,
                    prefix=f'funcion700-{form.prefix}',
                )


        # 382 → nested
        medios_formset = context.get('medios_interpretacion')
        if medios_formset:
            parent_instances = (
                [f.instance for f in medios_formset if f.instance.pk]
                if with_post else []
            )
            nested = self._get_nested_formsets(
                parent_instances=parent_instances,
                with_post=with_post
            )
            context.update(nested)

        return context

    # =====================================================
    # FORM VALID
    # =====================================================
    @transaction.atomic
    def form_valid(self, form):
        logger.info("🚀 INICIANDO form_valid()")

        context = self.get_context_data()
        formsets_validos, formsets = self._validar_formsets(context)

        if not formsets_validos:
            messages.error(self.request, "Hay errores en los formsets.")
            return self.form_invalid(form)

        # =====================================================
        # GUARDAR OBRA PRINCIPAL (UNA SOLA VEZ)
        # =====================================================
        self.object = form.save(commit=False)
        self.object.save()

        # =====================================================
        # 773 / 774 / 787 $w
        # =====================================================
        for enlace in self.object.enlaces_documento_fuente_773.all():
            for obra_id in self.request.POST.getlist(f"w_773_{enlace.pk}"):
                if obra_id and int(obra_id) != self.object.pk:
                    NumeroControl773.objects.create(
                        enlace_773=enlace,
                        obra_relacionada_id=obra_id
                    )

        for enlace in self.object.enlaces_unidades_774.all():
            for obra_id in self.request.POST.getlist(f"w_774_{enlace.pk}"):
                if obra_id and int(obra_id) != self.object.pk:
                    NumeroControl774.objects.create(
                        enlace_774=enlace,
                        obra_relacionada_id=obra_id
                    )

        for enlace in self.object.otras_relaciones_787.all():
            for obra_id in self.request.POST.getlist(f"w_787_{enlace.pk}"):
                if obra_id and int(obra_id) != self.object.pk:
                    NumeroControl787.objects.create(
                        enlace_787=enlace,
                        obra_relacionada_id=obra_id
                    )

        # =====================================================
        # 382 – Medios de interpretación
        # =====================================================
        medios_formset = formsets.get("medios_interpretacion")
        if medios_formset:
            medios = medios_formset.save(commit=False)
            for m in medios:
                m.obra = self.object
                m.save()
            for m in medios_formset.deleted_objects:
                m.delete()

        # =====================================================
        # 🔥 GUARDAR TODOS LOS FORMSETS (856 INCLUIDO)
        # =====================================================
        self._guardar_formsets(formsets, self.object)

        messages.success(self.request, "Obra registrada exitosamente.")
        return redirect(self.get_success_url())



class EditarObraView(CatalogadorRequiredMixin, ObraFormsetMixin, UpdateView):
    """
    Vista para editar una obra MARC21 existente.
    Maneja el formulario principal y todos los formsets anidados.
    """
    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/editar_obra.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Obtener configuración según tipo de obra"""
        # Obtener la obra ANTES de llamar a super().dispatch()
        # para que self.object esté disponible en get_context_data()
        self.object = self.get_object()
        
        # Determinar tipo de obra basado en sus características
        self.tipo_obra = self._determinar_tipo_obra(self.object)
        self.config_obra = TIPO_OBRA_CONFIG.get(self.tipo_obra, {})
        
        # Ahora sí llamar a super().dispatch()
        return super().dispatch(request, *args, **kwargs)
    
    def _determinar_tipo_obra(self, obra):
        """
        Determinar el tipo de obra basado en sus características MARC21.
        
        Args:
            obra: Instancia de ObraGeneral
        
        Returns:
            str: Clave del tipo de obra en TIPO_OBRA_CONFIG
        """
        tipo_reg = obra.tipo_registro
        nivel_bib = obra.nivel_bibliografico
        
        # Manuscritos (tipo_registro = 'd')
        if tipo_reg == 'd':
            if nivel_bib == 'c':
                return 'coleccion_manuscrita'
            elif nivel_bib == 'a':
                return 'obra_en_coleccion_manuscrita'
            elif nivel_bib == 'm':
                return 'obra_manuscrita_individual'
        
        # Impresos (tipo_registro = 'c')
        elif tipo_reg == 'c':
            if nivel_bib == 'c':
                return 'coleccion_impresa'
            elif nivel_bib == 'a':
                return 'obra_en_coleccion_impresa'
            elif nivel_bib == 'm':
                return 'obra_impresa_individual'
        
        # Default
        return 'obra_impresa_individual'
    
    def get_context_data(self, **kwargs):
        logger.info(f"🔧 get_context_data() EDITAR (method={self.request.method})")

        context = super().get_context_data(**kwargs)

        # Información del tipo de obra
        context['tipo_obra'] = self.tipo_obra
        context['tipo_obra_titulo'] = self.config_obra.get('titulo', 'Obra')
        context['tipo_obra_descripcion'] = self.config_obra.get('descripcion', '')

        # Configuración de campos visibles
        campos_config = get_campos_visibles(self.tipo_obra)
        context['campos_visibles'] = campos_config['campos_simples']

        # 🚨 IMPORTANTE: declarar formsets_visibles ANTES de generarlos
        context['formsets_visibles'] = campos_config['formsets_visibles']

        with_post = self.request.method == 'POST'

        # 🚀 Crear todos los formsets
        formsets = self._get_formsets(instance=self.object, with_post=with_post)

        # Añadir cada formset explícitamente al contexto
        for key, fs in formsets.items():
            context[key] = fs
        
        # =====================================================
        # 🔥 INLINE FORMSET 700 $e – Función
        # =====================================================
        formset_700 = formsets.get("nombres_relacionados_700") or formsets.get("700")

        if formset_700:
            for form in formset_700:
                form.funcion700_formset = Funcion700FormSet(
                    instance=form.instance,
                    prefix=f'funcion700-{form.prefix}',
                )


        logger.debug(f"   Formsets cargados en contexto (editar): {list(formsets.keys())}")

        # Formsets anidados del 382 (382$a)
        medios_formset = context.get('medios_interpretacion')
        if medios_formset:
            if with_post:
                # Instancias con PK
                parent_instances = [
                    form.instance for form in medios_formset if form.instance.pk
                ]
            else:
                # Todas las instancias ya guardadas
                parent_instances = list(self.object.medios_interpretacion_382.all())

            nested = self._get_nested_formsets(
                parent_instances=parent_instances,
                with_post=with_post
            )
            context.update(nested)

        return context

    @transaction.atomic
    def form_valid(self, form):
        """Actualizar obra y todos los formsets en una transacción atómica"""
        context = self.get_context_data()
        
        # Validar todos los formsets
        formsets_validos, formsets = self._validar_formsets(context)
        
        if not formsets_validos:
            messages.error(
                self.request,
                'Por favor corrija los errores en los formularios.'
            )
            return self.form_invalid(form)
        
        # Actualizar la obra principal
        self.object = form.save(commit=False)
        
        self.object.save()
        
        # Guardar todos los formsets y sus subcampos
        self._guardar_formsets(formsets, self.object)
        
        # Mensaje de éxito
        messages.success(self.request, f'{self.config_obra["titulo"]} actualizada exitosamente.')
        
        return redirect(self.get_success_url())
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.errors:
            logger.error("❌ Errores en formulario de EDICIÓN:")
            for field, errs in form.errors.items():
                logger.error(f"   - {field}: {errs}")

        return super().post(request, *args, **kwargs)

    
    def get_success_url(self):
        """Redirigir al detalle de la obra"""
        return reverse('catalogacion:detalle_obra', kwargs={'pk': self.object.pk})


class DetalleObraView(CatalogadorRequiredMixin, DetailView):
    """
    Vista de detalle de una obra.
    Muestra toda la información catalogada de una obra MARC21.
    """
    model = ObraGeneral
    template_name = 'catalogacion/detalle_obra.html'
    context_object_name = 'obra'


class ListaObrasView(CatalogadorRequiredMixin, ListView):
    """
    Vista de listado de obras con paginación y búsqueda.
    Permite filtrar obras por título, número de control o compositor.
    """
    model = ObraGeneral
    template_name = 'catalogacion/lista_obras.html'
    context_object_name = 'obras'
    paginate_by = 20
    
    def get_queryset(self):
        """Obtener queryset con búsqueda y optimizaciones"""
        queryset = ObraGeneral.objects.activos().select_related(
            'compositor',
            'titulo_uniforme'
        ).order_by('-fecha_creacion_sistema')
        
        # Filtro de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo_principal__icontains=q) |
                Q(num_control__icontains=q) |
                Q(compositor__apellidos_nombres__icontains=q)
            )
        
        return queryset


class EliminarObraView(CatalogadorRequiredMixin, DeleteView):
    """
    Vista para eliminar (soft delete) una obra.
    No elimina físicamente, solo marca como inactiva.
    """
    model = ObraGeneral
    success_url = reverse_lazy('catalogacion:lista_obras')
    
    def delete(self, request, *args, **kwargs):
        """Realizar soft delete de la obra"""
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(
            request,
            f'Obra "{self.object.titulo_principal}" eliminada exitosamente.'
        )
        return redirect(self.success_url)