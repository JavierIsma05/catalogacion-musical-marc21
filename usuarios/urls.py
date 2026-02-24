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
    SolicitarCuentaView,
    AdminSolicitudesListView,
    DetalleSolicitudView,
    GenerarEnlaceResetView,
    AdminResetConfirmView,
    CrearClaveTemporalView,
    ProfileUpdateView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
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
    path('admin/catalogadores/<int:pk>/generar-reset/', GenerarEnlaceResetView.as_view(), name='generar_reset_catalogador'),
    path('admin/catalogadores/<int:pk>/generar-clave/', CrearClaveTemporalView.as_view(), name='generar_clave_catalogador'),
    
    # Dashboard Catalogador
    path('catalogador/dashboard/', CatalogadorDashboardView.as_view(), name='catalogador_dashboard'),
    # Perfil de usuario (editar datos y cambiar contraseña)
    path('perfil/', ProfileUpdateView.as_view(), name='perfil_editar'),
    path('perfil/password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('perfil/password/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    # Solicitar cuenta (público)
    path('solicitar-cuenta/', SolicitarCuentaView.as_view(), name='solicitar_cuenta'),

    # Gestión de solicitudes (admin)
    path('admin/solicitudes/', AdminSolicitudesListView.as_view(), name='admin_solicitudes'),
    path('admin/solicitudes/<int:pk>/', DetalleSolicitudView.as_view(), name='detalle_solicitud'),
    path('admin/reset-confirm/<uidb64>/<token>/', AdminResetConfirmView.as_view(), name='admin_reset_confirm'),
]
