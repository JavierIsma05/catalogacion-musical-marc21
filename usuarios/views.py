from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm, ProfileForm
from .forms import SolicitudUsuarioForm
from .models import SolicitudUsuario
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.utils import timezone
import secrets
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views import View
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django import forms
from django.http import Http404


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


class GenerarEnlaceResetView(AdminRequiredMixin, View):
    """Genera un token de restablecimiento y muestra al admin un enlace que el usuario puede usar para fijar nueva contraseña."""

    def post(self, request, pk):
        usuario = get_object_or_404(CustomUser, pk=pk)
        uid = urlsafe_base64_encode(force_bytes(usuario.pk))
        token = default_token_generator.make_token(usuario)
        # Construir URL absoluta para confirmación de restablecimiento
        # Usamos una ruta interna `usuarios:admin_reset_confirm` que implementamos abajo
        reset_path = reverse('usuarios:admin_reset_confirm', args=[uid, token])
        reset_url = request.build_absolute_uri(reset_path)

        # Registrar notificación interna (sin incluir token completo en la notificación pública)
        try:
            from .models import Notification
            Notification.objects.create(usuario=request.user, solicitud=None, mensaje=f"Enlace de restablecimiento generado para {usuario.email}")
        except Exception:
            pass

        return render(request, 'usuarios/admin/mostrar_enlace_reset.html', {'usuario': usuario, 'reset_url': reset_url})


class CrearClaveTemporalView(AdminRequiredMixin, View):
    """Genera una contraseña temporal segura, la asigna al usuario y la muestra UNA vez al administrador."""

    def post(self, request, pk):
        usuario = get_object_or_404(CustomUser, pk=pk)
        # Generar contraseña segura
        nueva_clave = secrets.token_urlsafe(10)
        # Aplicar la contraseña al usuario
        usuario.set_password(nueva_clave)
        usuario.save()

        # Registrar notificación interna (sin almacenar la contraseña)
        try:
            from .models import Notification
            Notification.objects.create(usuario=request.user, solicitud=None, mensaje=f"Se generó una contraseña temporal para {usuario.email}")
        except Exception:
            pass

        # Mostrar la contraseña UNA vez al admin
        return render(request, 'usuarios/admin/mostrar_clave.html', {'usuario': usuario, 'clave': nueva_clave})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Permite al usuario autenticado editar su propio perfil."""
    model = CustomUser
    form_class = ProfileForm
    template_name = 'usuarios/perfil/editar_perfil.html'
    success_url = reverse_lazy('usuarios:catalogador_dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuarios/perfil/password_change_form.html'
    success_url = reverse_lazy('usuarios:password_change_done')


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'usuarios/perfil/password_change_done.html'


class AdminResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Nueva contraseña')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Repetir contraseña')


class AdminResetConfirmView(View):
    """Permite al usuario (o admin que tenga el enlace) fijar una nueva contraseña usando token generado."""

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return CustomUser.objects.get(pk=uid)
        except Exception:
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is None or not default_token_generator.check_token(user, token):
            raise Http404('Enlace inválido o expirado')
        form = AdminResetPasswordForm()
        return render(request, 'usuarios/admin/admin_reset_confirm.html', {'form': form, 'usuario': user})

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is None or not default_token_generator.check_token(user, token):
            raise Http404('Enlace inválido o expirado')
        form = AdminResetPasswordForm(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data['new_password1']
            p2 = form.cleaned_data['new_password2']
            if p1 != p2:
                form.add_error('new_password2', 'Las contraseñas no coinciden')
                return render(request, 'usuarios/admin/admin_reset_confirm.html', {'form': form, 'usuario': user})
            user.set_password(p1)
            user.save()
            messages.success(request, 'Contraseña actualizada correctamente. El usuario puede iniciar sesión con la nueva contraseña.')
            return redirect('usuarios:lista_catalogadores')
        return render(request, 'usuarios/admin/admin_reset_confirm.html', {'form': form, 'usuario': user})


# ============================================================================
# SOLICITUDES DE CUENTA (PÚBLICO + ADMIN)
# ============================================================================


class SolicitarCuentaView(CreateView):
    model = SolicitudUsuario
    form_class = SolicitudUsuarioForm
    template_name = 'usuarios/solicitud/solicitar_cuenta.html'
    success_url = reverse_lazy('usuarios:solicitar_cuenta')

    def form_valid(self, form):
        # Guardar solicitud
        response = super().form_valid(form)
        messages.success(self.request, 'Su solicitud ha sido enviada correctamente y será revisada por el administrador')

        # Crear notificaciones internas para administradores
        try:
            from .models import Notification
            admins = CustomUser.objects.filter(rol=CustomUser.ROL_ADMIN)
            texto = f"Nueva solicitud de cuenta de {self.object.nombres} ({self.object.correo})"
            for a in admins:
                Notification.objects.create(usuario=a, solicitud=self.object, mensaje=texto)
        except Exception:
            # No bloquear al usuario si falla la notificación interna
            pass

        return response


class AdminSolicitudesListView(AdminRequiredMixin, ListView):
    model = SolicitudUsuario
    template_name = 'usuarios/admin/solicitudes_list.html'
    context_object_name = 'solicitudes'
    paginate_by = 20

    def get_queryset(self):
        estado = self.request.GET.get('estado')
        qs = SolicitudUsuario.objects.all()
        if estado in (SolicitudUsuario.ESTADO_PENDIENTE, SolicitudUsuario.ESTADO_APROBADO, SolicitudUsuario.ESTADO_RECHAZADO):
            qs = qs.filter(estado=estado)
        else:
            qs = qs.filter(estado=SolicitudUsuario.ESTADO_PENDIENTE)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitudes de Cuenta'
        context['pendientes_count'] = SolicitudUsuario.objects.filter(estado=SolicitudUsuario.ESTADO_PENDIENTE).count()
        return context


class DetalleSolicitudView(AdminRequiredMixin, DetailView):
    model = SolicitudUsuario
    template_name = 'usuarios/admin/detalle_solicitud.html'
    context_object_name = 'solicitud'

    def get(self, request, *args, **kwargs):
        # Marcar notificaciones relacionadas como leídas para este admin
        self.object = self.get_object()
        try:
            from .models import Notification
            Notification.objects.filter(usuario=request.user, solicitud=self.object, leido=False).update(leido=True)
        except Exception:
            pass
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')
        if action == 'aprobar':
            # Evitar la creación si ya existe usuario
            if CustomUser.objects.filter(email__iexact=self.object.correo).exists():
                messages.error(request, 'Ya existe un usuario con ese correo. No se creó la cuenta.')
            else:
                # Generar contraseña segura
                password = secrets.token_urlsafe(10)
                # Mapear tipo de usuario a rol
                tipo = self.object.tipo_usuario
                rol = CustomUser.ROL_CATALOGADOR
                if tipo == SolicitudUsuario.TIPO_ADMIN:
                    rol = CustomUser.ROL_ADMIN

                usuario = CustomUser.objects.create_user(
                    email=self.object.correo,
                    password=password,
                    nombre_completo=self.object.nombres,
                )
                usuario.rol = rol
                usuario.activo = True
                usuario.save()

                # Marcar solicitud aprobada
                self.object.marcar_aprobada(respondido_por=request.user)

                messages.success(request, f'Solicitud aprobada. Usuario creado: {usuario.email} (contraseña generada).')
            return redirect(reverse('usuarios:detalle_solicitud', args=[self.object.pk]))

        if action == 'rechazar':
            self.object.marcar_rechazada(respondido_por=request.user)
            messages.success(request, 'Solicitud rechazada correctamente.')
            return redirect(reverse('usuarios:admin_solicitudes'))

        messages.error(request, 'Acción no reconocida.')
        return redirect(reverse('usuarios:admin_solicitudes'))
