"""
Signals para invalidar cache de PDFs y thumbnails de segmentos.
"""

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from pathlib import Path
from django.conf import settings
from .models import WorkSegment, DigitalSet


def _delete_cached_file(path: str) -> None:
    """
    Elimina un archivo cacheado del disco.
    """
    if path:
        cached = Path(settings.MEDIA_ROOT) / path
        if cached.exists():
            cached.unlink()


# === WorkSegment signals ===

@receiver(pre_save, sender=WorkSegment)
def invalidate_segment_cache_on_change(sender, instance, **kwargs):
    """
    Invalida el cache del PDF y thumbnail cuando cambian los parámetros del segmento.
    """
    if instance.pk:
        try:
            old = WorkSegment.objects.get(pk=instance.pk)
            if (old.start_page != instance.start_page or
                old.end_page != instance.end_page or
                old.digital_set_id != instance.digital_set_id):
                # Invalidar PDF cache
                _delete_cached_file(old.cached_pdf_path)
                instance.cached_pdf_path = ""
                instance.cached_pdf_generated_at = None
                # Invalidar thumbnail cache
                _delete_cached_file(old.cached_thumb_path)
                instance.cached_thumb_path = ""
        except WorkSegment.DoesNotExist:
            pass


@receiver(pre_delete, sender=WorkSegment)
def delete_segment_cache_on_delete(sender, instance, **kwargs):
    """
    Elimina archivos cacheados cuando se elimina el segmento.
    """
    _delete_cached_file(instance.cached_pdf_path)
    _delete_cached_file(instance.cached_thumb_path)


# === DigitalSet signals ===

@receiver(pre_save, sender=DigitalSet)
def invalidate_ds_thumb_on_pdf_change(sender, instance, **kwargs):
    """
    Invalida el thumbnail cuando cambia el PDF.
    """
    if instance.pk:
        try:
            old = DigitalSet.objects.get(pk=instance.pk)
            if old.pdf_path != instance.pdf_path:
                _delete_cached_file(old.pdf_thumb_path)
                instance.pdf_thumb_path = ""
        except DigitalSet.DoesNotExist:
            pass


@receiver(pre_delete, sender=DigitalSet)
def delete_ds_thumb_on_delete(sender, instance, **kwargs):
    """
    Elimina el thumbnail cuando se elimina el DigitalSet.
    """
    _delete_cached_file(instance.pdf_thumb_path)
