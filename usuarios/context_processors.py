from .models import SolicitudUsuario


def solicitudes_pendientes(request):
    """Añade el contador de solicitudes pendientes al contexto para administradores."""
    context = {'solicitudes_pendientes_count': 0, 'notifications_unread_count': 0, 'recent_notifications': []}
    if request.user.is_authenticated and getattr(request.user, 'es_admin', False):
        pendientes = SolicitudUsuario.objects.filter(estado=SolicitudUsuario.ESTADO_PENDIENTE).count()
        context['solicitudes_pendientes_count'] = pendientes
        # Evitar import circular
        try:
            from .models import Notification
            unread = Notification.objects.filter(usuario=request.user, leido=False).count()
            recent = list(Notification.objects.filter(usuario=request.user).select_related('solicitud')[:5])
            context['notifications_unread_count'] = unread
            context['recent_notifications'] = recent
        except Exception:
            context['notifications_unread_count'] = 0
            context['recent_notifications'] = []
    return context
