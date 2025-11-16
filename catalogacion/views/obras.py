"""
Views para gestión de obras MARC21
"""
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction

from catalogacion.models import ObraGeneral
from catalogacion.forms import (
    ObraGeneralForm,
    # Formsets del bloque 0XX
    IncipitMusicalFormSet,
    CodigoLenguaFormSet,
    CodigoPaisEntidadFormSet,
    # Formsets del bloque 1XX
    FuncionCompositorFormSet,
    # Formsets del bloque 2XX
    TituloAlternativoFormSet,
    EdicionFormSet,
    ProduccionPublicacionFormSet,
    # Formsets del bloque 5XX
    NotaGeneral500FormSet,
    Contenido505FormSet,
    Sumario520FormSet,
    DatosBiograficos545FormSet,
    # Formsets del bloque 6XX
    Materia650FormSet,
    MateriaGenero655FormSet,
    # Formsets del bloque 7XX
    NombreRelacionado700FormSet,
    EntidadRelacionada710FormSet,
    EnlaceDocumentoFuente773FormSet,
    EnlaceUnidadConstituyente774FormSet,
    OtrasRelaciones787FormSet,
)

# Mapeo de tipos de obra a configuraciones MARC21
TIPO_OBRA_CONFIG = {
    'coleccion_manuscrita': {
        'titulo': 'Colección Manuscrita',
        'descripcion': 'Conjunto de obras manuscritas sin compositor único',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'c',
        'punto_acceso': '130',  # Título uniforme principal
    },
    'obra_en_coleccion_manuscrita': {
        'titulo': 'Obra en Colección Manuscrita',
        'descripcion': 'Obra individual manuscrita dentro de una colección',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'a',
        'punto_acceso': '100',  # Compositor
    },
    'obra_manuscrita_individual': {
        'titulo': 'Obra Manuscrita Individual',
        'descripcion': 'Obra manuscrita completa e independiente',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'm',
        'punto_acceso': '100',  # Compositor
    },
    'coleccion_impresa': {
        'titulo': 'Colección Impresa',
        'descripcion': 'Conjunto de obras publicadas',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'c',
        'punto_acceso': '130',  # Título uniforme principal
    },
    'obra_en_coleccion_impresa': {
        'titulo': 'Obra en Colección Impresa',
        'descripcion': 'Obra individual publicada dentro de una colección',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'a',
        'punto_acceso': '100',  # Compositor
    },
    'obra_impresa_individual': {
        'titulo': 'Obra Impresa Individual',
        'descripcion': 'Obra publicada completa e independiente',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'm',
        'punto_acceso': '100',  # Compositor
    },
}


class SeleccionarTipoObraView(TemplateView):
    """
    Vista para seleccionar el tipo de obra a catalogar
    """
    template_name = 'catalogacion/seleccionar_tipo_obra.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_obra'] = TIPO_OBRA_CONFIG
        return context
    
    def post(self, request, *args, **kwargs):
        """Redirigir al formulario de creación según el tipo seleccionado"""
        tipo_obra = request.POST.get('tipo_obra')
        
        if tipo_obra not in TIPO_OBRA_CONFIG:
            messages.error(request, 'Tipo de obra inválido.')
            return redirect('catalogacion:seleccionar_tipo')
        
        return redirect('catalogacion:crear_obra', tipo=tipo_obra)


class CrearObraView(CreateView):
    """
    Vista para crear una nueva obra MARC21
    Maneja el formulario principal y todos los formsets anidados
    """
    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/crear_obra.html'
    
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
        
        # IMPORTANTE: Solo pre-cargar en GET inicial
        # En POST, los valores vienen del formulario oculto
        if self.request.method == 'GET':
            kwargs['initial'] = {
                'tipo_registro': self.config_obra['tipo_registro'],
                'nivel_bibliografico': self.config_obra['nivel_bibliografico'],
            }
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Agregar formsets al contexto"""
        context = super().get_context_data(**kwargs)
        
        # Información del tipo de obra
        context['tipo_obra'] = self.tipo_obra
        context['tipo_obra_titulo'] = self.config_obra['titulo']
        context['tipo_obra_descripcion'] = self.config_obra['descripcion']
        
        # Inicializar formsets solo si es GET o si hay errores
        if self.request.POST:
            # POST con datos
            context.update(self._get_formsets_post())
        else:
            # GET inicial
            context.update(self._get_formsets_get())
        
        return context
    
    def _get_formsets_get(self):
        """Obtener formsets vacíos para GET"""
        return {
            # Bloque 0XX
            'incipits_musicales': IncipitMusicalFormSet(prefix='incipits'),
            'codigos_lengua': CodigoLenguaFormSet(prefix='lenguas'),
            'codigos_pais': CodigoPaisEntidadFormSet(prefix='paises'),
            
            # Bloque 1XX
            'funciones_compositor': FuncionCompositorFormSet(prefix='funciones'),
            
            # Bloque 2XX
            'titulos_alternativos': TituloAlternativoFormSet(prefix='titulos_alt'),
            'ediciones': EdicionFormSet(prefix='ediciones'),
            'produccion_publicacion': ProduccionPublicacionFormSet(prefix='produccion'),
            
            # Bloque 5XX
            'notas_generales': NotaGeneral500FormSet(prefix='notas_500'),
            'contenidos': Contenido505FormSet(prefix='contenidos_505'),
            'sumarios': Sumario520FormSet(prefix='sumarios_520'),
            'datos_biograficos': DatosBiograficos545FormSet(prefix='biograficos_545'),
            
            # Bloque 6XX
            'materias_650': Materia650FormSet(prefix='materias_650'),
            'materias_genero_655': MateriaGenero655FormSet(prefix='generos_655'),
            
            # Bloque 7XX
            'nombres_relacionados_700': NombreRelacionado700FormSet(prefix='nombres_700'),
            'entidades_relacionadas_710': EntidadRelacionada710FormSet(prefix='entidades_710'),
            'enlaces_documento_fuente_773': EnlaceDocumentoFuente773FormSet(prefix='enlaces_773'),
            'enlaces_unidad_constituyente_774': EnlaceUnidadConstituyente774FormSet(prefix='enlaces_774'),
            'otras_relaciones_787': OtrasRelaciones787FormSet(prefix='relaciones_787'),
        }
    
    def _get_formsets_post(self):
        """Obtener formsets con datos POST"""
        return {
            # Bloque 0XX
            'incipits_musicales': IncipitMusicalFormSet(self.request.POST, prefix='incipits'),
            'codigos_lengua': CodigoLenguaFormSet(self.request.POST, prefix='lenguas'),
            'codigos_pais': CodigoPaisEntidadFormSet(self.request.POST, prefix='paises'),
            
            # Bloque 1XX
            'funciones_compositor': FuncionCompositorFormSet(self.request.POST, prefix='funciones'),
            
            # Bloque 2XX
            'titulos_alternativos': TituloAlternativoFormSet(self.request.POST, prefix='titulos_alt'),
            'ediciones': EdicionFormSet(self.request.POST, prefix='ediciones'),
            'produccion_publicacion': ProduccionPublicacionFormSet(self.request.POST, prefix='produccion'),
            
            # Bloque 5XX
            'notas_generales': NotaGeneral500FormSet(self.request.POST, prefix='notas_500'),
            'contenidos': Contenido505FormSet(self.request.POST, prefix='contenidos_505'),
            'sumarios': Sumario520FormSet(self.request.POST, prefix='sumarios_520'),
            'datos_biograficos': DatosBiograficos545FormSet(self.request.POST, prefix='biograficos_545'),
            
            # Bloque 6XX
            'materias_650': Materia650FormSet(self.request.POST, prefix='materias_650'),
            'materias_genero_655': MateriaGenero655FormSet(self.request.POST, prefix='generos_655'),
            
            # Bloque 7XX
            'nombres_relacionados_700': NombreRelacionado700FormSet(self.request.POST, prefix='nombres_700'),
            'entidades_relacionadas_710': EntidadRelacionada710FormSet(self.request.POST, prefix='entidades_710'),
            'enlaces_documento_fuente_773': EnlaceDocumentoFuente773FormSet(self.request.POST, prefix='enlaces_773'),
            'enlaces_unidad_constituyente_774': EnlaceUnidadConstituyente774FormSet(self.request.POST, prefix='enlaces_774'),
            'otras_relaciones_787': OtrasRelaciones787FormSet(self.request.POST, prefix='relaciones_787'),
        }
    
    @transaction.atomic
    def form_valid(self, form):
        """Guardar obra y todos los formsets en una transacción atómica"""
        context = self.get_context_data()
        
        # Validar todos los formsets
        formsets_validos = True
        formsets = {}
        
        for key in ['incipits_musicales', 'codigos_lengua', 'codigos_pais',
                   'funciones_compositor', 'titulos_alternativos', 'ediciones',
                   'produccion_publicacion', 'notas_generales', 'contenidos',
                   'sumarios', 'datos_biograficos', 'materias_650',
                   'materias_genero_655', 'nombres_relacionados_700',
                   'entidades_relacionadas_710', 'enlaces_documento_fuente_773',
                   'enlaces_unidad_constituyente_774', 'otras_relaciones_787']:
            formset = context.get(key)
            if formset:
                formsets[key] = formset
                if not formset.is_valid():
                    formsets_validos = False
        
        if not formsets_validos:
            messages.error(
                self.request,
                'Por favor corrija los errores en los formularios.'
            )
            return self.form_invalid(form)
        
        # Guardar la obra principal
        self.object = form.save(commit=False)
        
        # IMPORTANTE: Asegurar que tipo_registro y nivel_bibliografico estén asignados
        # Estos valores vienen del formulario oculto en el POST
        if not self.object.tipo_registro:
            self.object.tipo_registro = self.config_obra['tipo_registro']
        
        if not self.object.nivel_bibliografico:
            self.object.nivel_bibliografico = self.config_obra['nivel_bibliografico']
        
        # Guardar obra (esto ejecuta el método save() del modelo que genera campos automáticos)
        self.object.save()
        
        # Guardar todos los formsets
        for formset in formsets.values():
            formset.instance = self.object
            formset.save()
        
        # Mensaje de éxito
        action = self.request.POST.get('action', 'publish')
        if action == 'draft':
            messages.success(self.request, f'Borrador de {self.config_obra["titulo"]} guardado exitosamente.')
        else:
            messages.success(self.request, f'{self.config_obra["titulo"]} creada exitosamente.')
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        """Redirigir según la acción"""
        action = self.request.POST.get('action', 'publish')
        
        if action == 'draft':
            # Volver a editar
            return reverse('catalogacion:editar_obra', kwargs={'pk': self.object.pk})
        else:
            # Ver detalle
            return reverse('catalogacion:detalle_obra', kwargs={'pk': self.object.pk})


class EditarObraView(UpdateView):
    """
    Vista para editar una obra existente
    Similar a CrearObraView pero con instancia existente
    """
    model = ObraGeneral
    form_class = ObraGeneralForm
    template_name = 'catalogacion/editar_obra.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Determinar tipo de obra basado en los campos
        tipo_obra = self._determinar_tipo_obra(self.object)
        config_obra = TIPO_OBRA_CONFIG.get(tipo_obra, TIPO_OBRA_CONFIG['obra_manuscrita_individual'])
        
        context['tipo_obra'] = tipo_obra
        context['tipo_obra_titulo'] = config_obra['titulo']
        context['tipo_obra_descripcion'] = config_obra['descripcion']
        
        # Cargar formsets con instancia existente
        if self.request.POST:
            context.update(self._get_formsets_post())
        else:
            context.update(self._get_formsets_get())
        
        return context
    
    def _determinar_tipo_obra(self, obra):
        """Determinar el tipo de obra basado en sus características"""
        tipo = obra.tipo_registro
        nivel = obra.nivel_bibliografico
        
        if tipo == 'd' and nivel == 'c':
            return 'coleccion_manuscrita'
        elif tipo == 'd' and nivel == 'a':
            return 'obra_en_coleccion_manuscrita'
        elif tipo == 'd' and nivel == 'm':
            return 'obra_manuscrita_individual'
        elif tipo == 'c' and nivel == 'c':
            return 'coleccion_impresa'
        elif tipo == 'c' and nivel == 'a':
            return 'obra_en_coleccion_impresa'
        elif tipo == 'c' and nivel == 'm':
            return 'obra_impresa_individual'
        
        return 'obra_manuscrita_individual'  # Por defecto
    
    def _get_formsets_get(self):
        """Obtener formsets con instancia existente"""
        return {
            'incipits_musicales': IncipitMusicalFormSet(instance=self.object, prefix='incipits'),
            'codigos_lengua': CodigoLenguaFormSet(instance=self.object, prefix='lenguas'),
            'codigos_pais': CodigoPaisEntidadFormSet(instance=self.object, prefix='paises'),
            'funciones_compositor': FuncionCompositorFormSet(instance=self.object, prefix='funciones'),
            'titulos_alternativos': TituloAlternativoFormSet(instance=self.object, prefix='titulos_alt'),
            'ediciones': EdicionFormSet(instance=self.object, prefix='ediciones'),
            'produccion_publicacion': ProduccionPublicacionFormSet(instance=self.object, prefix='produccion'),
            'notas_generales': NotaGeneral500FormSet(instance=self.object, prefix='notas_500'),
            'contenidos': Contenido505FormSet(instance=self.object, prefix='contenidos_505'),
            'sumarios': Sumario520FormSet(instance=self.object, prefix='sumarios_520'),
            'datos_biograficos': DatosBiograficos545FormSet(instance=self.object, prefix='biograficos_545'),
            'materias_650': Materia650FormSet(instance=self.object, prefix='materias_650'),
            'materias_genero_655': MateriaGenero655FormSet(instance=self.object, prefix='generos_655'),
            'nombres_relacionados_700': NombreRelacionado700FormSet(instance=self.object, prefix='nombres_700'),
            'entidades_relacionadas_710': EntidadRelacionada710FormSet(instance=self.object, prefix='entidades_710'),
            'enlaces_documento_fuente_773': EnlaceDocumentoFuente773FormSet(instance=self.object, prefix='enlaces_773'),
            'enlaces_unidad_constituyente_774': EnlaceUnidadConstituyente774FormSet(instance=self.object, prefix='enlaces_774'),
            'otras_relaciones_787': OtrasRelaciones787FormSet(instance=self.object, prefix='relaciones_787'),
        }
    
    def _get_formsets_post(self):
        """Obtener formsets con datos POST e instancia"""
        return {
            'incipits_musicales': IncipitMusicalFormSet(self.request.POST, instance=self.object, prefix='incipits'),
            'codigos_lengua': CodigoLenguaFormSet(self.request.POST, instance=self.object, prefix='lenguas'),
            'codigos_pais': CodigoPaisEntidadFormSet(self.request.POST, instance=self.object, prefix='paises'),
            'funciones_compositor': FuncionCompositorFormSet(self.request.POST, instance=self.object, prefix='funciones'),
            'titulos_alternativos': TituloAlternativoFormSet(self.request.POST, instance=self.object, prefix='titulos_alt'),
            'ediciones': EdicionFormSet(self.request.POST, instance=self.object, prefix='ediciones'),
            'produccion_publicacion': ProduccionPublicacionFormSet(self.request.POST, instance=self.object, prefix='produccion'),
            'notas_generales': NotaGeneral500FormSet(self.request.POST, instance=self.object, prefix='notas_500'),
            'contenidos': Contenido505FormSet(self.request.POST, instance=self.object, prefix='contenidos_505'),
            'sumarios': Sumario520FormSet(self.request.POST, instance=self.object, prefix='sumarios_520'),
            'datos_biograficos': DatosBiograficos545FormSet(self.request.POST, instance=self.object, prefix='biograficos_545'),
            'materias_650': Materia650FormSet(self.request.POST, instance=self.object, prefix='materias_650'),
            'materias_genero_655': MateriaGenero655FormSet(self.request.POST, instance=self.object, prefix='generos_655'),
            'nombres_relacionados_700': NombreRelacionado700FormSet(self.request.POST, instance=self.object, prefix='nombres_700'),
            'entidades_relacionadas_710': EntidadRelacionada710FormSet(self.request.POST, instance=self.object, prefix='entidades_710'),
            'enlaces_documento_fuente_773': EnlaceDocumentoFuente773FormSet(self.request.POST, instance=self.object, prefix='enlaces_773'),
            'enlaces_unidad_constituyente_774': EnlaceUnidadConstituyente774FormSet(self.request.POST, instance=self.object, prefix='enlaces_774'),
            'otras_relaciones_787': OtrasRelaciones787FormSet(self.request.POST, instance=self.object, prefix='relaciones_787'),
        }
    
    @transaction.atomic
    def form_valid(self, form):
        """Similar a CrearObraView"""
        context = self.get_context_data()
        
        # Validar formsets
        formsets_validos = True
        formsets = {}
        
        for key in ['incipits_musicales', 'codigos_lengua', 'codigos_pais',
                   'funciones_compositor', 'titulos_alternativos', 'ediciones',
                   'produccion_publicacion', 'notas_generales', 'contenidos',
                   'sumarios', 'datos_biograficos', 'materias_650',
                   'materias_genero_655', 'nombres_relacionados_700',
                   'entidades_relacionadas_710', 'enlaces_documento_fuente_773',
                   'enlaces_unidad_constituyente_774', 'otras_relaciones_787']:
            formset = context.get(key)
            if formset:
                formsets[key] = formset
                if not formset.is_valid():
                    formsets_validos = False
        
        if not formsets_validos:
            messages.error(self.request, 'Por favor corrija los errores en los formularios.')
            return self.form_invalid(form)
        
        # Guardar obra
        self.object = form.save()
        
        # Guardar formsets
        for formset in formsets.values():
            formset.save()
        
        messages.success(self.request, 'Obra actualizada exitosamente.')
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('catalogacion:detalle_obra', kwargs={'pk': self.object.pk})


class DetalleObraView(DetailView):
    """Vista de detalle de una obra"""
    model = ObraGeneral
    template_name = 'catalogacion/detalle_obra.html'
    context_object_name = 'obra'


class ListaObrasView(ListView):
    """Vista de listado de obras con paginación y búsqueda"""
    model = ObraGeneral
    template_name = 'catalogacion/lista_obras.html'
    context_object_name = 'obras'
    paginate_by = 20
    
    def get_queryset(self):
        from django.db.models import Q
        
        queryset = ObraGeneral.objects.activos().select_related(
            'compositor',
            'titulo_uniforme',
            'institucion_persona_852a'
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
    """Vista para eliminar (soft delete) una obra"""
    model = ObraGeneral
    success_url = reverse_lazy('catalogacion:lista_obras')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(request, f'Obra "{self.object.titulo_principal}" eliminada exitosamente.')
        return redirect(self.success_url)
