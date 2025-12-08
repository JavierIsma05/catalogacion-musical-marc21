from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q

from catalogacion.models import ObraGeneral


class HomePublicoView(TemplateView):
    """Página de inicio pública del catálogo"""
    template_name = 'catalogo_publico/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Catálogo Musical MARC21'
        context['total_obras'] = ObraGeneral.objects.activos().count()
        # Últimas obras catalogadas
        context['ultimas_obras'] = ObraGeneral.objects.activos().order_by('-fecha_creacion_sistema')[:6]
        return context


class ListaObrasPublicaView(ListView):
    """Lista pública de obras catalogadas"""
    model = ObraGeneral
    template_name = 'catalogo_publico/lista_obras.html'
    context_object_name = 'obras'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = (
            ObraGeneral.objects.activos()
            .select_related(
                'compositor',
                'titulo_uniforme',
                'titulo_240',
                'forma_130',
                'forma_240',
            )
            .prefetch_related(
                'medios_interpretacion_382__medios',
                'materias_650__subdivisiones',
                'materias_655__subdivisiones',
                'producciones_publicaciones__lugares',
                'producciones_publicaciones__entidades',
                'producciones_publicaciones__fechas',
                'enlaces_documento_fuente_773__titulo',
                'enlaces_documento_fuente_773__encabezamiento_principal',
                'incipits_musicales',
            )
            .order_by('-fecha_creacion_sistema')
        )
        
        # Búsqueda por texto
        busqueda = self.request.GET.get('q', '')
        if busqueda:
            queryset = queryset.filter(
                Q(titulo_principal__icontains=busqueda) |
                Q(compositor__apellidos_nombres__icontains=busqueda)
            )
        
        # Filtro por tipo de obra
        tipo = self.request.GET.get('tipo', '')
        if tipo:
            queryset = queryset.filter(tipo_registro=tipo)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Catálogo de Obras'
        context['busqueda'] = self.request.GET.get('q', '')
        context['tipo_seleccionado'] = self.request.GET.get('tipo', '')
        # Opciones de tipos de registro para el filtro
        context['tipos_obra'] = [
            ('d', 'Manuscritos'),
            ('c', 'Impresos'),
        ]
        return context


class DetalleObraPublicaView(DetailView):
    """Vista pública de detalle de una obra"""
    model = ObraGeneral
    template_name = 'catalogo_publico/resumen_obra.html'
    context_object_name = 'obra'
    
    def get_queryset(self):
        return (
            ObraGeneral.objects.activos()
            .select_related(
                'compositor',
                'titulo_uniforme',
                'titulo_240',
                'forma_130',
                'forma_240',
            )
            .prefetch_related(
                'medios_interpretacion_382__medios',
                'materias_650__subdivisiones',
                'materias_655__subdivisiones',
                'producciones_publicaciones__lugares',
                'producciones_publicaciones__entidades',
                'producciones_publicaciones__fechas',
                'enlaces_documento_fuente_773__titulo',
                'enlaces_documento_fuente_773__encabezamiento_principal',
                'incipits_musicales',
                'notas_generales_500',
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Detalle: {self.object}'
        return context


class VistaDetalladaObraView(DetailView):
    """Vista pública detallada completa de una obra"""
    model = ObraGeneral
    template_name = 'catalogo_publico/detalle_obra.html'
    context_object_name = 'obra'
    
    def get_queryset(self):
        return (
            ObraGeneral.objects.activos()
            .select_related(
                'compositor',
                'titulo_uniforme',
                'titulo_240',
                'forma_130',
                'forma_240',
            )
            .prefetch_related(
                'medios_interpretacion_382__medios',
                'materias_650__subdivisiones',
                'materias_655__subdivisiones',
                'producciones_publicaciones__lugares',
                'producciones_publicaciones__entidades',
                'producciones_publicaciones__fechas',
                'enlaces_documento_fuente_773__titulo',
                'enlaces_documento_fuente_773__encabezamiento_principal',
                'incipits_musicales',
                'notas_generales_500',
                'titulos_alternativos',
                'ediciones',
                'nombres_relacionados_700__persona',
                'nombres_relacionados_700__funciones',
                'nombres_relacionados_700__terminos_asociados',
                'entidades_relacionadas_710__entidad',
                'menciones_serie__titulos',
                'menciones_serie__volumenes',
                'enlaces_unidades_774__encabezamiento_principal',
                'enlaces_unidades_774__titulo',
                'otras_relaciones_787__encabezamiento_principal',
                'contenidos_505',
                'sumarios_520',
                'ubicaciones_852__institucion_persona',
                'ubicaciones_852__estanterias',
                'disponibles_856__urls_856',
                'disponibles_856__textos_enlace_856',
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Vista detallada: {self.object}'
        return context
