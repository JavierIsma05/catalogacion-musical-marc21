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
    
    # Autoridades y APIs de autocomplete
    path('catalogacion/', include('catalogacion.urls_autoridades')),
    
    # Handlers de error personalizados (pendiente de implementar)
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
