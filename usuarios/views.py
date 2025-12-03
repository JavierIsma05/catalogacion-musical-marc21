from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'registration/inicio_sesion.html'
    
    # Si el usuario ya está logueado y trata de entrar al login,
    # lo redirigimos a la página principal en vez de mostrarle el form de nuevo.
    redirect_authenticated_user = True
    
    # (Opcional) Si quisieras pasar datos extra al template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar Sesión'
        return context
