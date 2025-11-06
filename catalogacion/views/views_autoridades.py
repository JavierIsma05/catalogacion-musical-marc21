"""
Vistas de Autoridades - Sistema de Catalogación MARC21 Musical
==============================================================

Endpoints JSON para búsqueda y autocompletado con campos editables.

Maneja:
- Búsqueda de personas (compositores, autores)
- Búsqueda de títulos uniformes
- Búsqueda de formas musicales
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from ..models import AutoridadPersona, AutoridadTituloUniforme, AutoridadFormaMusical


@require_GET
def get_autoridades_json(request):
    """
    Endpoint para obtener autoridades en formato JSON para autocompletado
    
    Parámetros GET:
        model (str): Tipo de autoridad ('compositor', 'titulo_uniforme', 'forma_musical')
        q (str): Término de búsqueda
    
    Returns:
        JsonResponse: Lista de resultados con formato {id, text, ...}
    
    Ejemplo:
        GET /api/autoridades/?model=compositor&q=Bach
        
    Respuesta:
        {
            "results": [
                {
                    "id": "Bach, Johann Sebastian", 
                    "text": "Bach, Johann Sebastian 1685-1750", 
                    "fechas": "1685-1750"
                },
                ...
            ]
        }
    """
    modelo = request.GET.get('model')
    busqueda = request.GET.get('q', '').strip()
    
    resultados = []
    
    if modelo == 'compositor':
        # Búsqueda de compositores (AutoridadPersona)
        if busqueda:
            # Buscar por apellidos_nombres O fechas
            query = AutoridadPersona.objects.filter(
                Q(apellidos_nombres__icontains=busqueda) |
                Q(fechas__icontains=busqueda)
            ).order_by('apellidos_nombres')[:20]
        else:
            # Devolver los primeros 100 si no hay búsqueda
            query = AutoridadPersona.objects.all().order_by('apellidos_nombres')[:100]
        
        resultados = [
            {
                'id': p.apellidos_nombres,  # El ID es el nombre completo
                'text': f"{p.apellidos_nombres} {p.fechas}".strip() if p.fechas else p.apellidos_nombres,
                'fechas': p.fechas or ''
            }
            for p in query
        ]
    
    elif modelo == 'titulo_uniforme':
        # Búsqueda de títulos uniformes
        if busqueda:
            query = AutoridadTituloUniforme.objects.filter(
                titulo__icontains=busqueda
            ).order_by('titulo')[:20]
        else:
            query = AutoridadTituloUniforme.objects.all().order_by('titulo')[:100]
        
        resultados = [
            {
                'id': t.titulo,  # El ID es el título completo
                'text': t.titulo,
                'fechas': ''  # No aplica para títulos
            }
            for t in query
        ]
    
    elif modelo == 'forma_musical':
        # Búsqueda de formas musicales
        if busqueda:
            query = AutoridadFormaMusical.objects.filter(
                forma__icontains=busqueda
            ).order_by('forma')[:20]
        else:
            query = AutoridadFormaMusical.objects.all().order_by('forma')[:100]
        
        resultados = [
            {
                'id': f.forma,  # El ID es la forma completa
                'text': f.forma,
                'fechas': ''  # No aplica para formas
            }
            for f in query
        ]
    
    return JsonResponse({'results': resultados})