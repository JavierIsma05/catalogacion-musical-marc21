from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm


class CustomLoginView(LoginView):
    """Vista personalizada de login"""
    template_name = 'registration/inicio_sesion.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar Sesión'
        return context
    
    def form_valid(self, form):
        """Verificar si el usuario está activo antes de permitir login"""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # Buscar el usuario por email
        try:
            user = CustomUser.objects.get(email=username)
            # Verificar si el usuario existe y la contraseña es correcta
            if user.check_password(password):
                # Verificar si está activo
                if not user.activo:
                    # Usuario desactivado - mostrar mensaje especial
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            cuenta_desactivada=True,
                            usuario_nombre=user.nombre_completo or user.email
                        )
                    )
        except CustomUser.DoesNotExist:
            pass
        
        # Continuar con el login normal
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirige según el rol del usuario"""
        user = self.request.user
        if user.es_admin:
            return reverse_lazy('usuarios:admin_dashboard')
        return reverse_lazy('usuarios:catalogador_dashboard')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin que verifica que el usuario sea administrador"""
    
    def test_func(self):
        return self.request.user.es_admin
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('usuarios:login')


class CatalogadorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin que verifica que el usuario pueda catalogar"""
    
    def test_func(self):
        return self.request.user.puede_catalogar
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('usuarios:login')


# ============================================================================
# VISTAS DE DASHBOARD
# ============================================================================

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Dashboard principal para administradores"""
    template_name = 'usuarios/admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel de Administración'
        context['total_catalogadores'] = CustomUser.objects.filter(
            rol=CustomUser.ROL_CATALOGADOR
        ).count()
        context['catalogadores_activos'] = CustomUser.objects.filter(
            rol=CustomUser.ROL_CATALOGADOR,
            activo=True
        ).count()
        return context


class CatalogadorDashboardView(CatalogadorRequiredMixin, TemplateView):
    """Dashboard principal para catalogadores"""
    template_name = 'usuarios/catalogador/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel del Catalogador'
        return context


# ============================================================================
# GESTIÓN DE CATALOGADORES (SOLO ADMIN)
# ============================================================================

class ListaCatalogadoresView(AdminRequiredMixin, ListView):
    """Lista de catalogadores para administradores"""
    model = CustomUser
    template_name = 'usuarios/admin/lista_catalogadores.html'
    context_object_name = 'catalogadores'
    paginate_by = 10
    
    def get_queryset(self):
        return CustomUser.objects.filter(rol=CustomUser.ROL_CATALOGADOR)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Catalogadores'
        return context


class CrearCatalogadorView(AdminRequiredMixin, CreateView):
    """Crear nuevo catalogador"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'usuarios/admin/form_catalogador.html'
    success_url = reverse_lazy('usuarios:lista_catalogadores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Catalogador'
        context['accion'] = 'Crear'
        return context
    
    def form_valid(self, form):
        form.instance.rol = CustomUser.ROL_CATALOGADOR
        messages.success(self.request, 'Catalogador creado exitosamente.')
        return super().form_valid(form)


class EditarCatalogadorView(AdminRequiredMixin, UpdateView):
    """Editar catalogador existente"""
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'usuarios/admin/form_catalogador.html'
    success_url = reverse_lazy('usuarios:lista_catalogadores')
    
    def get_queryset(self):
        return CustomUser.objects.filter(rol=CustomUser.ROL_CATALOGADOR)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Catalogador'
        context['accion'] = 'Actualizar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Catalogador actualizado exitosamente.')
        return super().form_valid(form)


class EliminarCatalogadorView(AdminRequiredMixin, DeleteView):
    """Eliminar catalogador"""
    model = CustomUser
    template_name = 'usuarios/admin/confirmar_eliminar.html'
    success_url = reverse_lazy('usuarios:lista_catalogadores')
    
    def get_queryset(self):
        return CustomUser.objects.filter(rol=CustomUser.ROL_CATALOGADOR)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Catalogador eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


class ToggleActivoCatalogadorView(AdminRequiredMixin, UpdateView):
    """Activar/desactivar catalogador"""
    model = CustomUser
    fields = []
    success_url = reverse_lazy('usuarios:lista_catalogadores')
    
    def get_queryset(self):
        return CustomUser.objects.filter(rol=CustomUser.ROL_CATALOGADOR)
    
    def form_valid(self, form):
        self.object.activo = not self.object.activo
        self.object.save()
        estado = 'activado' if self.object.activo else 'desactivado'
        messages.success(self.request, f'Catalogador {estado} exitosamente.')
        return redirect(self.success_url)
