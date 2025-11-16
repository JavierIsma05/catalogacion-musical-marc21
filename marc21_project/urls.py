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
    
    # Aplicación de catalogación (incluye index)
    path('', include('catalogacion.urls')),
    
    # Handlers de error personalizados (pendiente de implementar)
]

# Configurar páginas de error personalizadas (pendiente)
# handler404 = 'catalogacion.views.errors.error_404'
# handler500 = 'catalogacion.views.errors.error_500'

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
