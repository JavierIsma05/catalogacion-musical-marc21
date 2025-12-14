"""
Views base del sistema
"""
from django.views.generic import RedirectView
from django.urls import reverse


class IndexView(RedirectView):
    """
    Vista de redirección según el tipo de usuario.
    - Usuarios no autenticados -> Catálogo público
    - Catalogadores -> Dashboard del catalogador
    - Admins -> Dashboard de administración
    """
    
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        
        if user.is_authenticated:
            if user.es_admin:
                return reverse('usuarios:admin_dashboard')
            elif user.puede_catalogar:
                return reverse('usuarios:catalogador_dashboard')
        
        return reverse('catalogo_publico:home')
