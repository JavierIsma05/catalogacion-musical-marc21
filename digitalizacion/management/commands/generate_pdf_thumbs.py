"""
Comando para generar thumbnails de todos los PDFs existentes.
Uso: python manage.py generate_pdf_thumbs
"""

from django.core.management.base import BaseCommand
from digitalizacion.models import DigitalSet, WorkSegment
from digitalizacion.services.thumbnail_service import (
    get_pdf_thumbnail_for_digital_set,
    get_pdf_thumbnail_for_segment
)


class Command(BaseCommand):
    help = 'Genera thumbnails para PDFs existentes sin thumbnail'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerar incluso si ya existe thumbnail',
        )

    def handle(self, *args, **options):
        force = options['force']
        ds_count = 0
        seg_count = 0

        self.stdout.write("Procesando DigitalSets con PDF...")

        # 1. DigitalSets con PDF
        for ds in DigitalSet.objects.exclude(pdf_path=""):
            if force or not ds.pdf_thumb_path:
                result = get_pdf_thumbnail_for_digital_set(ds)
                if result:
                    ds_count += 1
                    self.stdout.write(f"  [OK] DigitalSet {ds.id}: {result}")
                else:
                    self.stdout.write(self.style.WARNING(
                        f"  [SKIP] DigitalSet {ds.id}: no se pudo generar"
                    ))

        self.stdout.write("\nProcesando WorkSegments de colecciones con PDF...")

        # 2. WorkSegments de colecciones con PDF
        for seg in WorkSegment.objects.select_related('digital_set').all():
            if seg.digital_set and seg.digital_set.pdf_path:
                if force or not seg.cached_thumb_path:
                    result = get_pdf_thumbnail_for_segment(seg)
                    if result:
                        seg_count += 1
                        self.stdout.write(f"  [OK] Segment {seg.id}: {result}")

        self.stdout.write(self.style.SUCCESS(
            f"\nGenerados: {ds_count} DigitalSets, {seg_count} Segments"
        ))
