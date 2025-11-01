"""
Vistas de Autoridades - Sistema de Catalogación MARC21 Musical
==============================================================

Endpoints JSON para búsqueda y autocompletado con Select2.

Maneja:
- Búsqueda de personas (compositores, autores)
- Búsqueda de títulos uniformes
- Búsqueda de formas musicales
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ..models import AutoridadPersona, AutoridadTituloUniforme, AutoridadFormaMusical


@require_GET
def get_autoridades_json(request):
    """
    Endpoint para obtener autoridades en formato JSON para Select2
    
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
                {"id": "Bach, Johann Sebastian", "text": "Bach, Johann Sebastian 1685-1750", "fechas": "1685-1750"},
                ...
            ]
        }
    """
    modelo = request.GET.get('model')
    busqueda = request.GET.get('q', '')
    
    resultados = []
    
    if modelo == 'compositor':
        if busqueda:
            query = AutoridadPersona.objects.filter(
                apellidos_nombres__icontains=busqueda
            )[:20]
        else:
            # Devolver todos si no hay búsqueda (limitado a 100)
            query = AutoridadPersona.objects.all()[:100]
        
        resultados = [
            {
                'id': p.apellidos_nombres,
                'text': f"{p.apellidos_nombres} {p.fechas}" if p.fechas else p.apellidos_nombres,
                'fechas': p.fechas
            }
            for p in query
        ]
    
    elif modelo == 'titulo_uniforme':
        if busqueda:
            query = AutoridadTituloUniforme.objects.filter(
                titulo__icontains=busqueda
            )[:20]
        else:
            query = AutoridadTituloUniforme.objects.all()[:100]
        
        resultados = [
            {'id': t.titulo, 'text': t.titulo}
            for t in query
        ]
    
    elif modelo == 'forma_musical':
        if busqueda:
            query = AutoridadFormaMusical.objects.filter(
                forma__icontains=busqueda
            )[:20]
        else:
            query = AutoridadFormaMusical.objects.all()[:100]
        
        resultados = [
            {'id': f.forma, 'text': f.forma}
            for f in query
        ]
    
    return JsonResponse({'results': resultados})
