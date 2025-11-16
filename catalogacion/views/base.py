"""
Views base del sistema
"""
from django.views.generic import TemplateView
from django.db.models import Count, Q
from catalogacion.models import ObraGeneral


class IndexView(TemplateView):
    """
    Vista principal del dashboard
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        obras = ObraGeneral.objects.activos()
        
        context['stats'] = {
            'total_obras': obras.count(),
            'colecciones': obras.filter(nivel_bibliografico='c').count(),
            'manuscritos': obras.filter(tipo_registro='d').count(),
            'impresos': obras.filter(tipo_registro='c').count(),
        }
        
        # Obras recientes (últimas 10)
        context['obras_recientes'] = obras.order_by('-fecha_creacion_sistema')[:10]
        
        return context
