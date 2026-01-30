"""
Servicio para generar thumbnails de PDFs.

Genera previsualizaciones de la primera página de PDFs para usar como portadas
en el catálogo público cuando no hay imágenes derivadas de TIFF.

Estructura de archivos:
- Thumbnail de PDF principal: {colección}/access/thumbs/
- Thumbnail de segmentos: {colección}/access/segment_thumbs/
"""

from pathlib import Path
from django.conf import settings


def get_or_create_pdf_thumbnail(
    pdf_path: str,
    page_number: int = 1,
    output_dir: Path = None,
    max_size: int = 400
) -> str | None:
    """
    Genera thumbnail de una página del PDF.

    Args:
        pdf_path: Ruta relativa al PDF (desde MEDIA_ROOT)
        page_number: Número de página (1-based)
        output_dir: Directorio de salida (opcional)
        max_size: Tamaño máximo del lado mayor en píxeles

    Returns:
        Ruta relativa del thumbnail o None si falla
    """
    source_pdf = Path(settings.MEDIA_ROOT) / pdf_path
    if not source_pdf.exists():
        return None

    try:
        import fitz  # PyMuPDF
    except ImportError:
        import logging
        logging.warning("PyMuPDF no instalado. Thumbnails de PDF no disponibles.")
        return None

    # Directorio de salida dentro de access/thumbs/
    if output_dir is None:
        # source_pdf está en: {colección}/access/pdf/nombre.pdf
        # Queremos: {colección}/access/thumbs/
        output_dir = source_pdf.parent.parent / "thumbs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Nombre del archivo
    thumb_name = f"{source_pdf.stem}_p{page_number:03d}_thumb.jpg"
    output_path = output_dir / thumb_name

    # Si ya existe, retornarlo
    if output_path.exists():
        return str(output_path.relative_to(Path(settings.MEDIA_ROOT))).replace("\\", "/")

    try:
        doc = fitz.open(str(source_pdf))
        page_idx = page_number - 1

        if page_idx < 0 or page_idx >= len(doc):
            doc.close()
            return None

        page = doc[page_idx]
        rect = page.rect
        scale = max_size / max(rect.width, rect.height)
        matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=matrix)

        from PIL import Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(output_path, "JPEG", quality=85, optimize=True)
        doc.close()

        return str(output_path.relative_to(Path(settings.MEDIA_ROOT))).replace("\\", "/")

    except Exception as e:
        import logging
        logging.error(f"Error generando thumbnail para {pdf_path}: {e}")
        return None


def _get_segment_thumb_output_dir(ds) -> Path:
    """
    Obtiene el directorio de salida para thumbnails de segmentos.
    Usa la carpeta de la colección para mantener la jerarquía.
    """
    if ds.repository_path:
        # Usar carpeta de la colección
        repo = Path(ds.repository_path)
    else:
        # Fallback: derivar del pdf_path
        # pdf_path es algo como: digitalizacion/UNL-xxx/access/pdf/nombre.pdf
        pdf_full = Path(settings.MEDIA_ROOT) / ds.pdf_path
        # Subir 2 niveles: pdf -> access, luego agregar segment_thumbs
        repo = pdf_full.parent.parent.parent

    output_dir = repo / "access" / "segment_thumbs"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_pdf_thumbnail_for_digital_set(ds) -> str | None:
    """
    Obtiene o genera thumbnail para un DigitalSet con PDF.

    Args:
        ds: Instancia de DigitalSet

    Returns:
        Ruta relativa del thumbnail o None
    """
    if not ds or not ds.pdf_path:
        return None

    # Verificar cache existente
    if getattr(ds, 'pdf_thumb_path', '') and ds.pdf_thumb_path:
        cached = Path(settings.MEDIA_ROOT) / ds.pdf_thumb_path
        if cached.exists():
            return ds.pdf_thumb_path

    # Generar thumbnail (se guardará en {colección}/access/thumbs/)
    thumb_path = get_or_create_pdf_thumbnail(ds.pdf_path, page_number=1)

    if thumb_path and hasattr(ds, 'pdf_thumb_path'):
        ds.pdf_thumb_path = thumb_path
        ds.save(update_fields=["pdf_thumb_path"])

    return thumb_path


def get_pdf_thumbnail_for_segment(segment) -> str | None:
    """
    Obtiene o genera thumbnail para un WorkSegment.
    Usa la primera página del rango del segmento.

    Args:
        segment: Instancia de WorkSegment

    Returns:
        Ruta relativa del thumbnail o None
    """
    ds = segment.digital_set
    if not ds or not ds.pdf_path:
        return None

    # Verificar cache existente
    if getattr(segment, 'cached_thumb_path', '') and segment.cached_thumb_path:
        cached = Path(settings.MEDIA_ROOT) / segment.cached_thumb_path
        if cached.exists():
            return segment.cached_thumb_path

    # Directorio de salida dentro de la carpeta de la colección
    output_dir = _get_segment_thumb_output_dir(ds)

    # Generar thumbnail usando la página de inicio del segmento
    thumb_path = get_or_create_pdf_thumbnail(
        ds.pdf_path,
        page_number=segment.start_page,
        output_dir=output_dir
    )

    if thumb_path and hasattr(segment, 'cached_thumb_path'):
        segment.cached_thumb_path = thumb_path
        segment.save(update_fields=["cached_thumb_path"])

    return thumb_path
