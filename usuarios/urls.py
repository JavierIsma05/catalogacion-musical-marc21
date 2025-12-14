from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView,
    AdminDashboardView,
    CatalogadorDashboardView,
    ListaCatalogadoresView,
    CrearCatalogadorView,
    EditarCatalogadorView,
    EliminarCatalogadorView,
    ToggleActivoCatalogadorView,
)

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Dashboard Admin
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # Gestión de Catalogadores (solo admin)
    path('admin/catalogadores/', ListaCatalogadoresView.as_view(), name='lista_catalogadores'),
    path('admin/catalogadores/crear/', CrearCatalogadorView.as_view(), name='crear_catalogador'),
    path('admin/catalogadores/<int:pk>/editar/', EditarCatalogadorView.as_view(), name='editar_catalogador'),
    path('admin/catalogadores/<int:pk>/eliminar/', EliminarCatalogadorView.as_view(), name='eliminar_catalogador'),
    path('admin/catalogadores/<int:pk>/toggle-activo/', ToggleActivoCatalogadorView.as_view(), name='toggle_activo_catalogador'),
    
    # Dashboard Catalogador
    path('catalogador/dashboard/', CatalogadorDashboardView.as_view(), name='catalogador_dashboard'),
]
