"""
Utilidades para views
"""
from django.http import JsonResponse
from django.db.models import Q

from catalogacion.models import (
    AutoridadPersona,
    AutoridadEntidad,
    AutoridadTituloUniforme,
    AutoridadMateria,
)


def autocompletar_persona(request):
    """
    API para autocompletar personas en Select2
    """
    q = request.GET.get('q', '')
    
    personas = AutoridadPersona.objects.filter(
        Q(apellidos_nombres__icontains=q) |
        Q(codigo_autoridad__icontains=q)
    )[:20]
    
    results = [
        {
            'id': p.id,
            'text': f"{p.apellidos_nombres} ({p.fechas})" if p.fechas else p.apellidos_nombres,
        }
        for p in personas
    ]
    
    return JsonResponse({'results': results})


def autocompletar_entidad(request):
    """
    API para autocompletar entidades en Select2
    """
    q = request.GET.get('q', '')
    
    entidades = AutoridadEntidad.objects.filter(
        Q(nombre__icontains=q) |
        Q(codigo_autoridad__icontains=q)
    )[:20]
    
    results = [
        {
            'id': e.id,
            'text': f"{e.nombre} ({e.lugar})" if e.lugar else e.nombre,
        }
        for e in entidades
    ]
    
    return JsonResponse({'results': results})


def autocompletar_titulo_uniforme(request):
    """
    API para autocompletar títulos uniformes en Select2
    """
    q = request.GET.get('q', '')
    
    titulos = AutoridadTituloUniforme.objects.filter(
        Q(titulo__icontains=q) |
        Q(codigo_autoridad__icontains=q)
    )[:20]
    
    results = [
        {
            'id': t.id,
            'text': t.titulo,
        }
        for t in titulos
    ]
    
    return JsonResponse({'results': results})


def autocompletar_materia(request):
    """
    API para autocompletar materias en Select2
    """
    q = request.GET.get('q', '')
    
    materias = AutoridadMateria.objects.filter(
        Q(termino__icontains=q) |
        Q(codigo_autoridad__icontains=q)
    )[:20]
    
    results = [
        {
            'id': m.id,
            'text': m.termino,
        }
        for m in materias
    ]
    
    return JsonResponse({'results': results})
