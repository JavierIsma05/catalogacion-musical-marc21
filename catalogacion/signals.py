"""
Señales para lógica post-guardado
Separa responsabilidades del método save()
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import ObraGeneral


# @receiver(post_save, sender=ObraGeneral)
# def generar_medio_fisico_automatico(sender, instance, created, **kwargs):
#     """
#     Genera medio físico automático después de crear una obra.
#     Solo se ejecuta en creación, no en actualizaciones.
#     
#     NOTA: Deshabilitado - Los modelos MedioFisico y Tecnica340 no existen en bloque_3xx
#     """
#     pass


@receiver(pre_save, sender=ObraGeneral)
def actualizar_fecha_transaccion(sender, instance, **kwargs):
    """
    Actualiza el campo 005 (fecha_hora_ultima_transaccion) antes de cada guardado.
    """
    from datetime import datetime
    instance.fecha_hora_ultima_transaccion = datetime.now().strftime("%Y%m%d%H%M%S")


@receiver(post_save, sender=ObraGeneral)
def log_creacion_obra(sender, instance, created, **kwargs):
    """
    Registra en log cuando se crea una nueva obra.
    Útil para auditoría.
    """
    if created:
        import logging
        logger = logging.getLogger('marc21')
        logger.info(
            f"Nueva obra creada: {instance.num_control} - "
            f"{instance.tipo_obra_descripcion} - "
            f"{instance.titulo_principal}"
        )