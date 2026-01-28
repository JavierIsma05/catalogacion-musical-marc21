"""
Servicio para generar y cachear PDFs de segmentos.

Prioridad:
1. Generar desde imágenes JPG (derivative_path)
2. Extraer del PDF de la colección (fallback)
"""

from pathlib import Path
from django.conf import settings
from django.utils import timezone
from PIL import Image


def get_or_create_segment_pdf(segment) -> str | None:
    """
    Extrae páginas del PDF de la colección para crear PDF del segmento.
    Retorna ruta relativa del PDF generado.
    """
    from pypdf import PdfReader, PdfWriter

    ds = segment.digital_set
    if not ds or not ds.pdf_path:
        return None

    source_pdf = Path(settings.MEDIA_ROOT) / ds.pdf_path
    if not source_pdf.exists():
        return None

    # Verificar cache existente
    if segment.cached_pdf_path:
        cached = Path(settings.MEDIA_ROOT) / segment.cached_pdf_path
        if cached.exists():
            return segment.cached_pdf_path

    # Generar PDF parcial
    output_dir = Path(settings.MEDIA_ROOT) / "digitalizacion" / "segment_pdfs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_name = f"segment_{segment.id}_p{segment.start_page}-{segment.end_page}.pdf"
    output_path = output_dir / output_name

    reader = PdfReader(str(source_pdf))
    writer = PdfWriter()

    # pypdf usa índices 0-based
    for page in reader.pages[segment.start_page - 1 : segment.end_page]:
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    # Guardar en modelo
    rel_path = str(output_path.relative_to(Path(settings.MEDIA_ROOT))).replace("\\", "/")
    segment.cached_pdf_path = rel_path
    segment.cached_pdf_generated_at = timezone.now()
    segment.save(update_fields=["cached_pdf_path", "cached_pdf_generated_at"])

    return rel_path


def get_or_create_segment_pdf_from_images(segment) -> str | None:
    """
    Genera PDF a partir de imágenes JPG (derivative_path).
    Retorna ruta relativa del PDF generado.
    """
    from digitalizacion.models import DigitalPage

    ds = segment.digital_set
    if not ds:
        return None

    # Verificar cache existente
    if segment.cached_pdf_path:
        cached = Path(settings.MEDIA_ROOT) / segment.cached_pdf_path
        if cached.exists():
            return segment.cached_pdf_path

    # Obtener imágenes del rango
    pages = DigitalPage.objects.filter(
        digital_set=ds,
        page_number__gte=segment.start_page,
        page_number__lte=segment.end_page
    ).order_by("page_number")

    if not pages.exists():
        return None

    # Recolectar rutas de imágenes existentes
    image_paths = []
    for p in pages:
        if p.derivative_path:
            img_path = Path(settings.MEDIA_ROOT) / p.derivative_path
            if img_path.exists():
                image_paths.append(img_path)

    if not image_paths:
        return None

    # Generar PDF
    output_dir = Path(settings.MEDIA_ROOT) / "digitalizacion" / "segment_pdfs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_name = f"segment_{segment.id}_p{segment.start_page}-{segment.end_page}_fromjpg.pdf"
    output_path = output_dir / output_name

    # Convertir imágenes a PDF
    images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        images.append(img)

    if images:
        # Guardar primera imagen como PDF, agregar el resto
        images[0].save(
            output_path,
            "PDF",
            save_all=True,
            append_images=images[1:] if len(images) > 1 else []
        )

    # Guardar en modelo
    rel_path = str(output_path.relative_to(Path(settings.MEDIA_ROOT))).replace("\\", "/")
    segment.cached_pdf_path = rel_path
    segment.cached_pdf_generated_at = timezone.now()
    segment.save(update_fields=["cached_pdf_path", "cached_pdf_generated_at"])

    return rel_path


def get_segment_pdf(segment) -> str | None:
    """
    Obtiene PDF del segmento.

    Prioridad:
    1. Generar desde imágenes JPG (derivative_path)
    2. Extraer del PDF de la colección (fallback)
    """
    from digitalizacion.models import DigitalPage

    ds = segment.digital_set
    if not ds:
        return None

    # Prioridad 1: Generar desde imágenes si existen
    has_images = DigitalPage.objects.filter(
        digital_set=ds,
        page_number__gte=segment.start_page,
        page_number__lte=segment.end_page
    ).exclude(derivative_path="").exists()

    if has_images:
        return get_or_create_segment_pdf_from_images(segment)

    # Prioridad 2: Extraer del PDF si existe
    if ds.pdf_path:
        return get_or_create_segment_pdf(segment)

    return None
