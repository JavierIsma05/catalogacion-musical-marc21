# catalogacion/models/bloque_5xx.py
from django.db import models


# ==========================================================
# 🟠 BLOQUE 5XX – Notas
# ==========================================================

class NotaGeneral500(models.Model):
    """
    500 ## Nota general (R)
    Puede repetirse para múltiples observaciones sobre la obra.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='notas_generales_500'
    )
    texto = models.TextField(help_text="500 ## $a Nota general (R)")

    def __str__(self):
        return f"500: {self.texto[:60]}..."

    class Meta:
        verbose_name = "Nota general (500)"
        verbose_name_plural = "Notas generales (500)"


class NotaContenido505(models.Model):
    """
    505 ## Nota de contenido (R)
    Describe partes, movimientos o secciones de la obra.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='notas_contenido_505'
    )
    contenido = models.TextField(help_text="505 ## $a Contenido (R)")

    def __str__(self):
        return f"505: {self.contenido[:60]}..."

    class Meta:
        verbose_name = "Nota de contenido (505)"
        verbose_name_plural = "Notas de contenido (505)"


class NotaBiografica545(models.Model):
    """
    545 ## Nota biográfica del compositor (R)
    Incluye información biográfica o histórica sobre el autor o compositor.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='notas_biograficas_545'
    )
    datos_biograficos = models.TextField(help_text="545 ## $a Datos biográficos del compositor (R)")
    url = models.URLField(blank=True, null=True, help_text="545 ## $u URL relacionada (R)")

    def __str__(self):
        return f"545: {self.datos_biograficos[:60]}..."

    class Meta:
        verbose_name = "Nota biográfica (545)"
        verbose_name_plural = "Notas biográficas (545)"

