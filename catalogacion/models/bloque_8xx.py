from django.db import models

# ============================================================
# 📦 BLOQUE 8XX – UBICACIÓN Y DISPONIBILIDAD
# ============================================================

class Ubicacion852(models.Model):
    """
    852 ## Ubicación (R)
    - $a Institución o persona (NR)
    - $c Estantería (R)
    - $h Signatura original (NR)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ubicaciones_852'
    )

    institucion_persona = models.CharField(
        max_length=255,
        help_text="852 $a – Institución o persona (no repetible)"
    )

    signatura_original = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="852 $h – Signatura original (no repetible)"
    )

    def __str__(self):
        return f"{self.institucion_persona} ({self.signatura_original or 'sin signatura'})"

    class Meta:
        verbose_name = "852 - Ubicación"
        verbose_name_plural = "📍 852 - Ubicaciones"


class Estanteria852(models.Model):
    """
    Subcampo repetible 852 $c – Estantería (R)
    """
    ubicacion = models.ForeignKey(
        Ubicacion852,
        on_delete=models.CASCADE,
        related_name='estanterias'
    )

    estanteria = models.CharField(
        max_length=255,
        help_text="852 $c – Estantería (repetible)"
    )

    def __str__(self):
        return self.estanteria

    class Meta:
        verbose_name = "852 $c – Estantería"
        verbose_name_plural = "📚 852 $c – Estanterías"


class Disponible856(models.Model):
    """
    856 4# Disponible (R)
    - $u URL (R)
    - $y Texto del enlace (R)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='disponibles_856'
    )

    url = models.URLField(
        max_length=500,
        help_text="856 $u – URL del recurso disponible"
    )

    texto_enlace = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="856 $y – Texto del enlace (repetible)"
    )

    def __str__(self):
        return f"{self.texto_enlace or 'Recurso disponible'} → {self.url}"

    class Meta:
        verbose_name = "856 - Disponible"
        verbose_name_plural = "🌐 856 - Recursos disponibles"
