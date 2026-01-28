"""
Signals para invalidar cache de PDFs de segmentos.
"""

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from pathlib import Path
from django.conf import settings
from .models import WorkSegment


@receiver(pre_save, sender=WorkSegment)
def invalidate_segment_cache_on_change(sender, instance, **kwargs):
    """
    Invalida el cache del PDF cuando cambian los parámetros del segmento.
    """
    if instance.pk:
        try:
            old = WorkSegment.objects.get(pk=instance.pk)
            if (old.start_page != instance.start_page or
                old.end_page != instance.end_page or
                old.digital_set_id != instance.digital_set_id):
                _delete_cached_pdf(old.cached_pdf_path)
                instance.cached_pdf_path = ""
                instance.cached_pdf_generated_at = None
        except WorkSegment.DoesNotExist:
            pass


@receiver(pre_delete, sender=WorkSegment)
def delete_segment_cache_on_delete(sender, instance, **kwargs):
    """
    Elimina el archivo PDF cacheado cuando se elimina el segmento.
    """
    _delete_cached_pdf(instance.cached_pdf_path)


def _delete_cached_pdf(path: str) -> None:
    """
    Elimina un archivo PDF cacheado del disco.
    """
    if path:
        cached = Path(settings.MEDIA_ROOT) / path
        if cached.exists():
            cached.unlink()
