"""
Views para gestión de autoridades (Personas, Entidades, etc.)
"""
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import ProtectedError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from catalogacion.models import (
    AutoridadPersona,
    AutoridadEntidad,
    AutoridadTituloUniforme,
    AutoridadMateria,
    AutoridadFormaMusical,
)
from catalogacion.forms import (
    AutoridadPersonaForm,
    AutoridadEntidadForm,
    AutoridadFormaMusicalForm,
    AutoridadMateriaForm,
    AutoridadTituloUniformeForm,
)


# =====================================================
# VIEWS DE PERSONAS
# =====================================================

class ListaPersonasView(ListView):
    """Listar todas las autoridades de personas"""
    model = AutoridadPersona
    template_name = 'usuarios/catalogador/autoridades/lista_personas.html'
    context_object_name = 'personas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')
        
        # Filtro de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(apellidos_nombres__icontains=q) |
                Q(coordenadas_biograficas__icontains=q)
            )
        
        return queryset


class CrearPersonaView(CreateView):
    """Crear nueva autoridad de persona"""
    model = AutoridadPersona
    template_name = 'usuarios/catalogador/autoridades/crear_persona.html'
    form_class = AutoridadPersonaForm
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
    template_name = 'usuarios/catalogador/autoridades/crear_persona.html'
    form_class = AutoridadPersonaForm
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
    template_name = 'usuarios/catalogador/autoridades/ver_persona.html'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.apellidos_nombres

        try:
            self.object.delete()
            messages.success(request, f'Autoridad de persona "{nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ProtectedError as e:
            # Extraer los objetos que referencian a esta persona
            objetos_relacionados = e.protected_objects

            # Construir mensaje detallado
            detalles = []
            for obj in list(objetos_relacionados)[:5]:  # Máximo 5 ejemplos
                if hasattr(obj, 'num_control'):
                    detalles.append(f"Obra: {obj.num_control}")
                elif hasattr(obj, 'titulo_texto'):
                    detalles.append(f"Enlace 773: {obj.titulo_texto or 'Sin título'}")
                else:
                    detalles.append(str(obj))

            mensaje = f'No se puede eliminar "{nombre}" porque está siendo utilizada en: {", ".join(detalles)}'
            if len(objetos_relacionados) > 5:
                mensaje += f" y {len(objetos_relacionados) - 5} registro(s) más."

            messages.error(request, mensaje)
            return redirect('autoridades:lista_personas')


# =====================================================
# VIEWS DE ENTIDADES
# =====================================================

class ListaEntidadesView(ListView):
    """Listar todas las autoridades de entidades"""
    model = AutoridadEntidad
    template_name = 'usuarios/catalogador/autoridades/lista_entidades.html'
    context_object_name = 'entidades'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AutoridadEntidad.objects.all().order_by('nombre')
        
        # Filtro de búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(pais__icontains=q) |
                Q(descripcion__icontains=q)
            )
        
        return queryset


class CrearEntidadView(CreateView):
    """Crear nueva autoridad de entidad"""
    model = AutoridadEntidad
    template_name = 'usuarios/catalogador/autoridades/crear_entidad.html'
    form_class = AutoridadEntidadForm
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
    template_name = 'usuarios/catalogador/autoridades/crear_entidad.html'
    form_class = AutoridadEntidadForm
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
    template_name = 'usuarios/catalogador/autoridades/ver_entidad.html'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.nombre

        try:
            self.object.delete()
            messages.success(request, f'Autoridad de entidad "{nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ProtectedError as e:
            # Extraer los objetos que referencian a esta entidad
            objetos_relacionados = e.protected_objects

            # Construir mensaje detallado
            detalles = []
            for obj in list(objetos_relacionados)[:5]:
                if hasattr(obj, 'num_control'):
                    detalles.append(f"Obra: {obj.num_control}")
                else:
                    detalles.append(str(obj))

            mensaje = f'No se puede eliminar "{nombre}" porque está siendo utilizada en: {", ".join(detalles)}'
            if len(objetos_relacionados) > 5:
                mensaje += f" y {len(objetos_relacionados) - 5} registro(s) más."

            messages.error(request, mensaje)
            return redirect('autoridades:lista_entidades')


# =====================================================
# VIEWS DE FORMAS MUSICALES
# =====================================================


class ListaFormasMusicalesView(ListView):
    model = AutoridadFormaMusical
    template_name = 'usuarios/catalogador/autoridades/lista_formas_musicales.html'
    context_object_name = 'formas'
    paginate_by = 20

    def get_queryset(self):
        queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(forma__icontains=q)
        return queryset


class CrearFormaMusicalView(CreateView):
    model = AutoridadFormaMusical
    template_name = 'usuarios/catalogador/autoridades/crear_forma_musical.html'
    form_class = AutoridadFormaMusicalForm
    success_url = reverse_lazy('autoridades:lista_formas_musicales')

    def form_valid(self, form):
        messages.success(self.request, f'Forma musical "{form.instance.forma}" creada exitosamente.')
        return super().form_valid(form)


class EditarFormaMusicalView(UpdateView):
    model = AutoridadFormaMusical
    template_name = 'usuarios/catalogador/autoridades/crear_forma_musical.html'
    form_class = AutoridadFormaMusicalForm
    success_url = reverse_lazy('autoridades:lista_formas_musicales')

    def form_valid(self, form):
        messages.success(self.request, f'Forma musical "{form.instance.forma}" actualizada exitosamente.')
        return super().form_valid(form)


class EliminarFormaMusicalView(DeleteView):
    model = AutoridadFormaMusical
    success_url = reverse_lazy('autoridades:lista_formas_musicales')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.forma
        self.object.delete()
        messages.success(request, f'Forma musical "{nombre}" eliminada exitosamente.')
        return redirect(self.success_url)


# =====================================================
# VIEWS DE MATERIAS
# =====================================================


class ListaMateriasView(ListView):
    model = AutoridadMateria
    template_name = 'usuarios/catalogador/autoridades/lista_materias.html'
    context_object_name = 'materias'
    paginate_by = 20

    def get_queryset(self):
        queryset = AutoridadMateria.objects.all().order_by('termino')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(termino__icontains=q)
        return queryset


class CrearMateriaView(CreateView):
    model = AutoridadMateria
    template_name = 'usuarios/catalogador/autoridades/crear_materia.html'
    form_class = AutoridadMateriaForm
    success_url = reverse_lazy('autoridades:lista_materias')

    def form_valid(self, form):
        messages.success(self.request, f'Término de materia "{form.instance.termino}" creado exitosamente.')
        return super().form_valid(form)


class EditarMateriaView(UpdateView):
    model = AutoridadMateria
    template_name = 'usuarios/catalogador/autoridades/crear_materia.html'
    form_class = AutoridadMateriaForm
    success_url = reverse_lazy('autoridades:lista_materias')

    def form_valid(self, form):
        messages.success(self.request, f'Término de materia "{form.instance.termino}" actualizado exitosamente.')
        return super().form_valid(form)


class EliminarMateriaView(DeleteView):
    model = AutoridadMateria
    success_url = reverse_lazy('autoridades:lista_materias')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.termino
        self.object.delete()
        messages.success(request, f'Término de materia "{nombre}" eliminado exitosamente.')
        return redirect(self.success_url)


# =====================================================
# VIEWS DE TÍTULOS UNIFORMES
# =====================================================


class ListaTitulosUniformesView(ListView):
    model = AutoridadTituloUniforme
    template_name = 'usuarios/catalogador/autoridades/lista_titulos_uniformes.html'
    context_object_name = 'titulos'
    paginate_by = 20

    def get_queryset(self):
        queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(titulo__icontains=q)
        return queryset


class CrearTituloUniformeView(CreateView):
    model = AutoridadTituloUniforme
    template_name = 'usuarios/catalogador/autoridades/crear_titulo_uniforme.html'
    form_class = AutoridadTituloUniformeForm
    success_url = reverse_lazy('autoridades:lista_titulos_uniformes')

    def form_valid(self, form):
        messages.success(self.request, f'Título uniforme "{form.instance.titulo}" creado exitosamente.')
        return super().form_valid(form)


class EditarTituloUniformeView(UpdateView):
    model = AutoridadTituloUniforme
    template_name = 'usuarios/catalogador/autoridades/crear_titulo_uniforme.html'
    form_class = AutoridadTituloUniformeForm
    success_url = reverse_lazy('autoridades:lista_titulos_uniformes')

    def form_valid(self, form):
        messages.success(self.request, f'Título uniforme "{form.instance.titulo}" actualizado exitosamente.')
        return super().form_valid(form)


class EliminarTituloUniformeView(DeleteView):
    model = AutoridadTituloUniforme
    success_url = reverse_lazy('autoridades:lista_titulos_uniformes')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.titulo
        self.object.delete()
        messages.success(request, f'Título uniforme "{nombre}" eliminado exitosamente.')
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


class AutocompletarAutoridadView(View):
    """
    API combinada para autocompletar autoridades (personas + entidades)
    Retorna resultados intercalados con campo `model` indicando 'persona' o 'entidad'
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()

        if len(query) < 2:
            return JsonResponse({'results': []})

        personas = list(AutoridadPersona.objects.filter(
            Q(apellidos_nombres__icontains=query) |
            Q(coordenadas_biograficas__icontains=query)
        ).values('id', 'apellidos_nombres', 'coordenadas_biograficas')[:10])

        entidades = list(AutoridadEntidad.objects.filter(
            nombre__icontains=query
        ).values('id', 'nombre', 'pais')[:10])

        # Construir listas formateadas
        p_results = []
        for p in personas:
            texto = p['apellidos_nombres']
            if p.get('coordenadas_biograficas'):
                texto += f" ({p.get('coordenadas_biograficas')})"
            p_results.append({'id': p['id'], 'model': 'persona', 'text': texto})

        e_results = []
        for e in entidades:
            texto = e['nombre'] + (f" ({e['pais']} )" if e.get('pais') else "")
            e_results.append({'id': e['id'], 'model': 'entidad', 'text': texto})

        # Intercalar resultados: persona, entidad, persona, entidad...
        results = []
        i = 0
        while len(results) < 10 and (i < len(p_results) or i < len(e_results)):
            if i < len(p_results):
                results.append(p_results[i])
            if i < len(e_results) and len(results) < 10:
                results.append(e_results[i])
            i += 1

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


class AutocompletarGeneroView(View):
    """
    API para autocompletar géneros/formas musicales (campo 655)
    """
    def get(self, request):
        q = request.GET.get("q", "")
        resultados = []

        if q:
            generos = AutoridadFormaMusical.objects.filter(
                forma__icontains=q
            ).order_by("forma")
        else:
            generos = AutoridadFormaMusical.objects.all().order_by("forma")[:20]

        for g in generos:
            resultados.append({
                "id": g.id,
                "text": g.forma,
            })

        return JsonResponse({"results": resultados})

