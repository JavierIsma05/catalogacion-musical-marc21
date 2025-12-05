"""
Views para gestión de autoridades (Personas, Entidades, etc.)
"""
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from catalogacion.models import (
    AutoridadPersona,
    AutoridadEntidad,
    AutoridadTituloUniforme,
    AutoridadMateria,
)


# =====================================================
# VIEWS DE PERSONAS
# =====================================================

class ListaPersonasView(ListView):
    """Listar todas las autoridades de personas"""
    model = AutoridadPersona
    template_name = 'autoridades/lista_personas.html'
    context_object_name = 'personas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')
        
        # Filtro de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(apellidos_nombres__icontains=q) |
                Q(codigo_autoridad__icontains=q) |
                Q(fechas__icontains=q)
            )
        
        return queryset


class CrearPersonaView(CreateView):
    """Crear nueva autoridad de persona"""
    model = AutoridadPersona
    template_name = 'autoridades/crear_persona.html'
    fields = [
        'apellidos_nombres',
        'codigo_autoridad',
        'fechas',
        'termino_asociado',
        'notas',
        'activo',
    ]
    success_url = reverse_lazy('autoridades:lista_personas')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Autoridad de persona "{form.instance.apellidos_nombres}" creada exitosamente.'
        )
        return super().form_valid(form)


class EditarPersonaView(UpdateView):
    """Editar autoridad de persona existente"""
    model = AutoridadPersona
    template_name = 'autoridades/crear_persona.html'
    fields = [
        'apellidos_nombres',
        'codigo_autoridad',
        'fechas',
        'termino_asociado',
        'notas',
        'activo',
    ]
    success_url = reverse_lazy('autoridades:lista_personas')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Autoridad de persona "{form.instance.apellidos_nombres}" actualizada exitosamente.'
        )
        return super().form_valid(form)


class VerPersonaView(DetailView):
    """Ver detalles de una autoridad de persona"""
    model = AutoridadPersona
    template_name = 'autoridades/ver_persona.html'
    context_object_name = 'persona'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contar obras relacionadas
        context['obras_como_compositor'] = self.object.obras_compositor.count()
        context['obras_relacionadas'] = self.object.obras_relacionadas_700.count()
        
        return context


class EliminarPersonaView(DeleteView):
    """Eliminar autoridad de persona"""
    model = AutoridadPersona
    success_url = reverse_lazy('autoridades:lista_personas')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.apellidos_nombres
        
        # Verificar si tiene obras relacionadas
        obras_relacionadas = (
            self.object.obras_compositor.count() +
            self.object.obras_relacionadas_700.count()
        )
        
        if obras_relacionadas > 0:
            messages.warning(
                request,
                f'No se puede eliminar "{nombre}" porque tiene {obras_relacionadas} obra(s) relacionada(s).'
            )
            return redirect('autoridades:lista_personas')
        
        self.object.delete()
        messages.success(request, f'Autoridad de persona "{nombre}" eliminada exitosamente.')
        return redirect(self.success_url)


# =====================================================
# VIEWS DE ENTIDADES
# =====================================================

class ListaEntidadesView(ListView):
    """Listar todas las autoridades de entidades"""
    model = AutoridadEntidad
    template_name = 'autoridades/lista_entidades.html'
    context_object_name = 'entidades'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AutoridadEntidad.objects.all().order_by('nombre')
        
        # Filtro de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(codigo_autoridad__icontains=q) |
                Q(lugar__icontains=q)
            )
        
        return queryset


class CrearEntidadView(CreateView):
    """Crear nueva autoridad de entidad"""
    model = AutoridadEntidad
    template_name = 'autoridades/crear_entidad.html'
    fields = [
        'nombre',
        'codigo_autoridad',
        'lugar',
        'fechas',
        'notas',
        'activo',
    ]
    success_url = reverse_lazy('autoridades:lista_entidades')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Autoridad de entidad "{form.instance.nombre}" creada exitosamente.'
        )
        return super().form_valid(form)


class EditarEntidadView(UpdateView):
    """Editar autoridad de entidad existente"""
    model = AutoridadEntidad
    template_name = 'autoridades/crear_entidad.html'
    fields = [
        'nombre',
        'codigo_autoridad',
        'lugar',
        'fechas',
        'notas',
        'activo',
    ]
    success_url = reverse_lazy('autoridades:lista_entidades')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f'Autoridad de entidad "{form.instance.nombre}" actualizada exitosamente.'
        )
        return super().form_valid(form)


class VerEntidadView(DetailView):
    """Ver detalles de una autoridad de entidad"""
    model = AutoridadEntidad
    template_name = 'autoridades/ver_entidad.html'
    context_object_name = 'entidad'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contar obras relacionadas
        context['obras_relacionadas'] = self.object.obras_relacionadas_710.count()
        context['obras_ubicacion'] = self.object.obras_ubicadas.count()
        
        return context


class EliminarEntidadView(DeleteView):
    """Eliminar autoridad de entidad"""
    model = AutoridadEntidad
    success_url = reverse_lazy('autoridades:lista_entidades')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.nombre
        
        # Verificar si tiene obras relacionadas
        obras_relacionadas = (
            self.object.obras_relacionadas_710.count() +
            self.object.obras_ubicadas.count()
        )
        
        if obras_relacionadas > 0:
            messages.warning(
                request,
                f'No se puede eliminar "{nombre}" porque tiene {obras_relacionadas} obra(s) relacionada(s).'
            )
            return redirect('autoridades:lista_entidades')
        
        self.object.delete()
        messages.success(request, f'Autoridad de entidad "{nombre}" eliminada exitosamente.')
        return redirect(self.success_url)


class AutocompletarPersonaView(View):
    """
    API para autocompletar nombres de personas
    Retorna sugerencias basadas en el texto ingresado o por ID
    """
    def get(self, request):
        persona_id = request.GET.get('id')
        query = request.GET.get('q', '').strip()

        # ---- Buscar por ID ----
        if persona_id:
            try:
                persona = AutoridadPersona.objects.get(id=persona_id)
                result = {
                    'id': persona.id,
                    'text': persona.apellidos_nombres,
                    'apellidos_nombres': persona.apellidos_nombres,
                    'coordenadas_biograficas': persona.coordenadas_biograficas or '',
                }
                return JsonResponse({'results': [result]})
            except AutoridadPersona.DoesNotExist:
                return JsonResponse({'results': []})

        # ---- Buscar por texto ----
        if len(query) < 2:
            return JsonResponse({'results': []})

        personas = AutoridadPersona.objects.filter(
            Q(apellidos_nombres__icontains=query) |
            Q(coordenadas_biograficas__icontains=query)
        ).values(
            'id',
            'apellidos_nombres',
            'coordenadas_biograficas'
        )[:10]

        results = []
        for persona in personas:
            nombre_completo = persona['apellidos_nombres']
            if persona['coordenadas_biograficas']:
                nombre_completo += f" ({persona['coordenadas_biograficas']})"

            results.append({
                'id': persona['id'],
                'text': nombre_completo,
                'apellidos_nombres': persona['apellidos_nombres'],
                'coordenadas_biograficas': persona['coordenadas_biograficas'] or '',
            })

        return JsonResponse({'results': results})



class AutocompletarEntidadView(View):
    """
    API para autocompletar nombres de entidades
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()

        if len(query) < 2:
            return JsonResponse({'results': []})

        entidades = AutoridadEntidad.objects.filter(
            nombre__icontains=query
        ).values(
            'id',
            'nombre',
            'pais'
        )[:10]

        results = [{
            'id': entidad['id'],
            'text': entidad['nombre'] + (f" ({entidad['pais']})" if entidad['pais'] else ""),
            'nombre': entidad['nombre'],
            'pais': entidad['pais'] or ''
        } for entidad in entidades]

        return JsonResponse({'results': results})

class AutocompletarTituloUniformeView(View):
    """
    API para autocompletar títulos uniformes
    Soporta búsqueda por título y por ID
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()
        titulo_id = request.GET.get('id', None)
        
        # Si se busca por ID específico
        if titulo_id:
            try:
                titulo = AutoridadTituloUniforme.objects.get(id=titulo_id)
                return JsonResponse({
                    'results': [{
                        'id': titulo.id,
                        'text': titulo.titulo,
                        'titulo': titulo.titulo,
                    }]
                })
            except AutoridadTituloUniforme.DoesNotExist:
                return JsonResponse({'results': []})
        
        if len(query) < 2:
            return JsonResponse({'results': []})
        
        titulos = AutoridadTituloUniforme.objects.filter(
            titulo__icontains=query
        ).order_by('titulo')[:20]
        
        results = [
            {
                'id': t.id,
                'text': t.titulo,
                'titulo': t.titulo,
            }
            for t in titulos
        ]
        
        return JsonResponse({'results': results})
    
class AutocompletarMateriaView(View):
    def get(self, request):
        q = request.GET.get("q", "")
        resultados = []

        if q:
            materias = AutoridadMateria.objects.filter(
                termino__icontains=q
            ).order_by("termino")
        else:
            materias = AutoridadMateria.objects.all().order_by("termino")[:20]

        for m in materias:
            resultados.append({
                "id": m.id,
                "text": m.termino,
            })

        return JsonResponse({"results": resultados})

