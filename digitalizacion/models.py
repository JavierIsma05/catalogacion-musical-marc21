from django.db import models
from catalogacion.models.obra_general import ObraGeneral


class DigitalSet(models.Model):
    ESTADOS = (
        ("NUEVO", "Nuevo"),
        ("IMPORTADO", "Importado"),
        ("SEGMENTADO", "Segmentado"),
    )

    TIPOS = (
        ("COLECCION", "Colección"),
        ("OBRA_SUELTA", "Obra suelta"),
    )

    obra = models.OneToOneField(
        ObraGeneral,
        on_delete=models.CASCADE,
        related_name="digital_set",
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default="COLECCION")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="NUEVO")
    total_pages = models.PositiveIntegerField(default=0)

    # filesystem/NAS
    inbox_path = models.CharField(max_length=500, blank=True, default="")
    repository_path = models.CharField(max_length=500, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf_path = models.CharField(max_length=700, blank=True, default="")
    pdf_total_pages = models.PositiveIntegerField(default=0)

    def __str__(self):
        tipo_str = "Colección" if self.tipo == "COLECCION" else "Obra"
        return f"DigitalSet {tipo_str} {self.obra_id} ({self.total_pages} páginas)"

    @property
    def es_coleccion(self):
        """Indica si este DigitalSet es de una colección (requiere segmentación)"""
        return self.tipo == "COLECCION"

    @property
    def es_obra_suelta(self):
        """Indica si este DigitalSet es de una obra suelta (no requiere segmentación)"""
        return self.tipo == "OBRA_SUELTA"


class DigitalPage(models.Model):
    digital_set = models.ForeignKey(
        DigitalSet, on_delete=models.CASCADE, related_name="pages"
    )
    page_number = models.PositiveIntegerField()

    # Rutas de archivos (relativas a MEDIA_ROOT)
    source_path = models.CharField(
        max_length=700, blank=True, default=""
    )  # JPG original del escáner (source/)
    master_path = models.CharField(max_length=700, blank=True, default="")  # TIFF normalizado (master/)
    derivative_path = models.CharField(
        max_length=700, blank=True, default=""
    )  # JPG para visor (iiif/jpg/)

    class Meta:
        unique_together = ("digital_set", "page_number")
        ordering = ["page_number"]

    def __str__(self):
        return f"{self.digital_set_id} p{self.page_number:03d}"


class WorkSegment(models.Model):
    TIPOS = (
        ("OBRA", "Obra"),
        ("NOTAS", "Notas"),
        ("ANEXO", "Anexo"),
        ("EXCLUIDO", "Excluido"),
    )

    obra = models.ForeignKey(
        ObraGeneral,
        on_delete=models.CASCADE,
        related_name="segments",
    )
    digital_set = models.ForeignKey(
        DigitalSet,
        on_delete=models.CASCADE,
        related_name="segments",
    )
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default="OBRA")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_page", "end_page"]

    def __str__(self):
        return f"{self.obra_id} {self.start_page}-{self.end_page} ({self.tipo})"
