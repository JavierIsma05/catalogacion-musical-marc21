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

from catalogacion.models import ObraGeneral
from catalogacion.forms import ObraGeneralForm
from catalogacion.views.obra_config import (
    TIPO_OBRA_CONFIG,
    get_campos_visibles,
    debe_mostrar_formset,
)
from catalogacion.views.obra_mixins import ObraFormsetMixin

# Configurar logger
logger = logging.getLogger('catalogacion')


class SeleccionarTipoObraView(TemplateView):
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


class CrearObraView(ObraFormsetMixin, CreateView):
    """
    Vista para crear una nueva obra MARC21.
    Maneja el formulario principal y todos los formsets anidados.
    """
    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/crear_obra.html'
    
    def post(self, request, *args, **kwargs):
        """POST interceptado para logging"""
        # TRIPLE LOGGING para asegurar que se vea
        print("\n" + "🔵"*40, flush=True)
        print("📨 POST REQUEST RECIBIDO en CrearObraView", flush=True)
        print(f"📋 Total campos POST: {len(request.POST)}", flush=True)
        print("🔵"*40 + "\n", flush=True)
        
        logger.info("\n" + "🔵"*40)
        logger.info("📨 POST REQUEST RECIBIDO en CrearObraView")
        logger.debug(f"📋 Datos POST: {dict(request.POST.lists())}")
        logger.info("🔵"*40 + "\n")
        
        # También escribir en archivo por si acaso
        try:
            with open('debug_post.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n\n{'='*60}\n")
                f.write(f"POST recibido: {len(request.POST)} campos\n")
                f.write(f"{'='*60}\n")
        except:
            pass
        
        return super().post(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        """Validar que el tipo de obra sea válido"""
        self.tipo_obra = kwargs.get('tipo')
        
        if self.tipo_obra not in TIPO_OBRA_CONFIG:
            messages.error(request, 'Tipo de obra inválido.')
            return redirect('catalogacion:seleccionar_tipo')
        
        self.config_obra = TIPO_OBRA_CONFIG[self.tipo_obra]
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """Configurar el formulario con valores iniciales según tipo de obra"""
        kwargs = super().get_form_kwargs()
        
        # Solo pre-cargar en GET inicial, en POST los valores vienen del formulario
        if self.request.method == 'GET':
            kwargs['initial'] = {
                'tipo_registro': self.config_obra['tipo_registro'],
                'nivel_bibliografico': self.config_obra['nivel_bibliografico'],
            }
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Agregar formsets y contexto de tipo de obra"""
        context = super().get_context_data(**kwargs)
        
        # Información del tipo de obra
        context['tipo_obra'] = self.tipo_obra
        context['tipo_obra_titulo'] = self.config_obra['titulo']
        context['tipo_obra_descripcion'] = self.config_obra['descripcion']
        
        # Configuración de campos visibles según tipo de obra
        campos_config = get_campos_visibles(self.tipo_obra)
        context['campos_visibles'] = campos_config['campos_simples']
        context['formsets_visibles'] = campos_config['formsets_visibles']
        
        # Obtener formsets según método HTTP
        with_post = self.request.method == 'POST'
        context.update(self._get_formsets(instance=None, with_post=with_post))
        
        # Pasar borrador_id SOLO si viene de recuperar_borrador_view
        # y luego limpiar inmediatamente la sesión
        if 'borrador_id' in self.request.session:
            context['borrador_id_recuperar'] = self.request.session.get('borrador_id')
            # Limpiar la sesión inmediatamente para que no persista
            del self.request.session['borrador_id']
            if 'tipo_obra' in self.request.session:
                del self.request.session['tipo_obra']
            self.request.session.modified = True
        
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        """Guardar obra y todos los formsets en una transacción atómica"""
        logger.info("\n" + "="*80)
        logger.info("🚀 FORM_VALID LLAMADO - Iniciando guardado de obra")
        logger.info("="*80)
        
        context = self.get_context_data()
        
        # Validar todos los formsets
        formsets_validos, formsets = self._validar_formsets(context)
        
        logger.info(f"\n✅ Formsets válidos: {formsets_validos}")
        logger.info(f"📦 Formsets recibidos: {list(formsets.keys())}")
        
        if not formsets_validos:
            logger.error("\n❌ ERROR: Formsets NO válidos")
            for nombre, formset in formsets.items():
                if hasattr(formset, 'errors') and formset.errors:
                    logger.error(f"\n  ❌ Errores en {nombre}:")
                    for i, errors in enumerate(formset.errors):
                        if errors:
                            logger.error(f"     Form {i}: {errors}")
            
            messages.error(
                self.request,
                'Por favor corrija los errores en los formularios.'
            )
            return self.form_invalid(form)
        
        # Validar campo 382 obligatorio (al menos un medio de interpretación)
        medios_formset = formsets.get('medios_interpretacion')
        if medios_formset:
            tiene_medios = False
            for medio_form in medios_formset:
                if medio_form.cleaned_data and not medio_form.cleaned_data.get('DELETE', False):
                    # Verificar si tiene al menos un subcampo $a
                    medio_id = medio_form.instance.pk if medio_form.instance else None
                    if medio_id:
                        # Ya existe, verificar si tiene subcampos $a
                        from catalogacion.models import MedioInterpretacion382_a
                        tiene_medios = MedioInterpretacion382_a.objects.filter(
                            medio_interpretacion=medio_id
                        ).exists()
                    else:
                        # Nuevo registro, verificar en POST si tiene subcampos dinámicos
                        # Los subcampos $a se envían como medio_interpretacion_382_X_timestamp
                        pattern = 'medio_interpretacion_382_'
                        for key in self.request.POST:
                            if key.startswith(pattern) and self.request.POST[key]:
                                tiene_medios = True
                                break
                    if tiene_medios:
                        break
            
            if not tiene_medios:
                messages.error(
                    self.request,
                    'Campo 382 - Medio de Interpretación: Debe especificar al menos un medio de interpretación ($a).'
                )
                return self.form_invalid(form)
        else:
            messages.error(
                self.request,
                'Campo 382 - Medio de Interpretación es obligatorio.'
            )
            return self.form_invalid(form)
        
        # Guardar la obra principal
        self.object = form.save(commit=False)
        
        # Asegurar tipo_registro y nivel_bibliografico
        if not self.object.tipo_registro:
            self.object.tipo_registro = self.config_obra['tipo_registro']
        
        if not self.object.nivel_bibliografico:
            self.object.nivel_bibliografico = self.config_obra['nivel_bibliografico']
        
        self.object.save()
        
        # Guardar todos los formsets y sus subcampos
        self._guardar_formsets(formsets, self.object)
        
        # Marcar borrador como convertido si existe
        borrador_id = self.request.session.get('borrador_id')
        if borrador_id:
            try:
                from catalogacion.models import BorradorObra
                borrador = BorradorObra.objects.get(id=borrador_id, estado='activo')
                borrador.estado = 'convertido'
                borrador.obra_creada = self.object
                borrador.save()
                
                # Limpiar sesión
                del self.request.session['borrador_id']
                if 'tipo_obra' in self.request.session:
                    del self.request.session['tipo_obra']
            except BorradorObra.DoesNotExist:
                pass
        
        # Mensaje de éxito
        messages.success(self.request, f'{self.config_obra["titulo"]} registrada exitosamente.')
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        """Redirigir al detalle de la obra recién creada"""
        return reverse('catalogacion:detalle_obra', kwargs={'pk': self.object.pk})


class EditarObraView(ObraFormsetMixin, UpdateView):
    """
    Vista para editar una obra MARC21 existente.
    Maneja el formulario principal y todos los formsets anidados.
    """
    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/editar_obra.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Obtener configuración según tipo de obra"""
        response = super().dispatch(request, *args, **kwargs)
        
        # Determinar tipo de obra basado en sus características
        obra = self.get_object()
        self.tipo_obra = self._determinar_tipo_obra(obra)
        self.config_obra = TIPO_OBRA_CONFIG.get(self.tipo_obra, {})
        
        return response
    
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
        """Agregar formsets con datos de la instancia"""
        context = super().get_context_data(**kwargs)
        
        # Información del tipo de obra
        context['tipo_obra'] = self.tipo_obra
        context['tipo_obra_titulo'] = self.config_obra.get('titulo', 'Obra')
        context['tipo_obra_descripcion'] = self.config_obra.get('descripcion', '')
        
        # Configuración de campos visibles según tipo de obra
        campos_config = get_campos_visibles(self.tipo_obra)
        context['campos_visibles'] = campos_config['campos_simples']
        context['formsets_visibles'] = campos_config['formsets_visibles']
        
        # Obtener formsets según método HTTP
        with_post = self.request.method == 'POST'
        context.update(self._get_formsets(instance=self.object, with_post=with_post))
        
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
    
    def get_success_url(self):
        """Redirigir al detalle de la obra"""
        return reverse('catalogacion:detalle_obra', kwargs={'pk': self.object.pk})


class DetalleObraView(DetailView):
    """
    Vista de detalle de una obra.
    Muestra toda la información catalogada de una obra MARC21.
    """
    model = ObraGeneral
    template_name = 'catalogacion/detalle_obra.html'
    context_object_name = 'obra'


class ListaObrasView(ListView):
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


class EliminarObraView(DeleteView):
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
