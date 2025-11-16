"""
Views para gestión de autoridades (Personas, Entidades, etc.)
"""
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

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
