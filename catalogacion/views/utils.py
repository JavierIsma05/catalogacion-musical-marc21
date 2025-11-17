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
    Soporta búsqueda por apellidos_nombres y coordenadas_biograficas
    Permite crear nuevas personas si se envía 'crear=true'
    Permite buscar por ID si se envía 'id=123'
    """
    q = request.GET.get('q', '')
    crear = request.GET.get('crear', 'false') == 'true'
    persona_id = request.GET.get('id', None)
    
    # Si se busca por ID específico
    if persona_id:
        try:
            persona = AutoridadPersona.objects.get(id=persona_id)
            return JsonResponse({
                'results': [{
                    'id': persona.id,
                    'text': str(persona),
                    'apellidos_nombres': persona.apellidos_nombres,
                    'coordenadas_biograficas': persona.coordenadas_biograficas or '',
                }]
            })
        except AutoridadPersona.DoesNotExist:
            return JsonResponse({'results': []})
    
    # Si se solicita crear una nueva persona
    if crear and q:
        persona, created = AutoridadPersona.objects.get_or_create(
            apellidos_nombres=q,
            defaults={'coordenadas_biograficas': ''}
        )
        return JsonResponse({
            'id': persona.id,
            'text': str(persona),
            'created': created
        })
    
    # Búsqueda normal
    personas = AutoridadPersona.objects.filter(
        Q(apellidos_nombres__icontains=q) |
        Q(coordenadas_biograficas__icontains=q)
    ).order_by('apellidos_nombres')[:20]
    
    results = [
        {
            'id': p.id,
            'text': str(p),
            'apellidos_nombres': p.apellidos_nombres,
            'coordenadas_biograficas': p.coordenadas_biograficas or '',
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
        Q(pais__icontains=q)
    ).order_by('nombre')[:20]
    
    results = [
        {
            'id': e.id,
            'text': str(e),
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
        titulo__icontains=q
    ).order_by('titulo')[:20]
    
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
        termino__icontains=q
    ).order_by('termino')[:20]
    
    results = [
        {
            'id': m.id,
            'text': m.termino,
        }
        for m in materias
    ]
    
    return JsonResponse({'results': results})
