"""
URLs principales del proyecto Django
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Interfaz Pública (home principal)
    path('', include('catalogo_publico.urls')),
    
    # Aplicación de catalogación (para catalogadores autenticados)
    path('catalogacion/', include('catalogacion.urls')),
    
    # Autoridades y APIs de autocomplete
    path('catalogacion/', include(('catalogacion.urls_autoridades', 'autoridades'), namespace='autoridades')),
    
    # Sistema de usuarios (login, gestión de catalogadores, dashboards)
    path('usuarios/', include('usuarios.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    # En desarrollo, usar django.contrib.staticfiles (finders) para servir estáticos
    # y evitar depender de STATIC_ROOT/collectstatic.
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
