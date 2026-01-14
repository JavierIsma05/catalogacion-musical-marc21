import io
import logging
import sys
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction

import requests
import fitz  # PyMuPDF

from catalogacion.models import ObraGeneral

logger = logging.getLogger(__name__)


def get_first_856_url(obra):
    """Return the first URL from disponibles_856 (if any)."""
    for disp in obra.disponibles_856.all():
        for u in disp.urls_856.all():
            if u.url:
                return u.url.strip()
    return None


class Command(BaseCommand):
    help = 'Genera portadas para obras a partir de la primera URL 856 (imagen o PDF -> PNG)'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=0, help='Número máximo de obras a procesar')
        parser.add_argument('--dry-run', action='store_true', help='No guarda archivos, solo reporta')

    def handle(self, *args, **options):
        limit = options.get('limit', 0) or 0
        dry = options.get('dry_run', False)

        qs = ObraGeneral.objects.activos().filter(portada__isnull=True)
        if limit > 0:
            qs = qs[:limit]

        total = qs.count() if hasattr(qs, 'count') else len(list(qs))
        self.stdout.write(f"Procesando hasta {limit or 'todos'} obras (sin portada), encontrados: {total}")

        for obra in qs:
            url = obra.first_portada_url or get_first_856_url(obra)
            if not url:
                self.stdout.write(f"Obra {obra.pk}: sin URL 856");
                continue

            self.stdout.write(f"Obra {obra.pk}: procesando URL {url}")

            try:
                resp = requests.get(url, timeout=20)
                if resp.status_code != 200:
                    self.stdout.write(f"  -> HTTP {resp.status_code} para {url}")
                    continue

                content_type = (resp.headers.get('Content-Type') or '').lower()
                data = resp.content

                if ('image' in content_type) or url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    # Guardar la imagen tal cual
                    ext = 'png'
                    if 'jpeg' in content_type or url.lower().endswith(('.jpg', '.jpeg')):
                        ext = 'jpg'
                    elif 'png' in content_type or url.lower().endswith('.png'):
                        ext = 'png'
                    elif 'gif' in content_type or url.lower().endswith('.gif'):
                        ext = 'gif'
                    elif 'webp' in content_type or url.lower().endswith('.webp'):
                        ext = 'webp'

                    filename = f'obra_{obra.pk}.{ext}'
                    if dry:
                        self.stdout.write(f"  (dry) would save image {filename}")
                    else:
                        obra.portada.save(filename, ContentFile(data), save=True)
                        self.stdout.write(f"  -> portada guardada {filename}")

                elif ('pdf' in content_type) or url.lower().endswith('.pdf'):
                    # Convertir primera página del PDF a PNG usando PyMuPDF
                    try:
                        doc = fitz.open(stream=data, filetype='pdf')
                        if doc.page_count <= 0:
                            self.stdout.write(f"  -> PDF sin páginas: {url}")
                            continue
                        page = doc.load_page(0)
                        # Escala: 2.0 -> mejor resolución
                        mat = fitz.Matrix(2.0, 2.0)
                        pix = page.get_pixmap(matrix=mat, alpha=False)
                        img_bytes = pix.tobytes('png')
                        filename = f'obra_{obra.pk}.png'
                        if dry:
                            self.stdout.write(f"  (dry) would save PDF->PNG {filename}")
                        else:
                            obra.portada.save(filename, ContentFile(img_bytes), save=True)
                            self.stdout.write(f"  -> portada generada desde PDF: {filename}")

                    except Exception as e:
                        self.stdout.write(f"  -> error convirtiendo PDF: {e}")
                        continue

                else:
                    self.stdout.write(f"  -> tipo desconocido ({content_type}), intentando heurística de extensión")
                    # Intentar heurística por extensión
                    if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        filename = f'obra_{obra.pk}.png'
                        if not dry:
                            obra.portada.save(filename, ContentFile(data), save=True)
                            self.stdout.write(f"  -> portada guardada por heurística {filename}")
                    else:
                        self.stdout.write("  -> no se puede procesar este recurso automáticamente")

            except Exception as exc:
                self.stdout.write(f"  -> excepción al descargar/procesar URL: {exc}")
                continue

        self.stdout.write("Proceso completado.")
