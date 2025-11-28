from django.db import models

# ============================================================
# 📦 BLOQUE 8XX – UBICACIÓN Y DISPONIBILIDAD
# ============================================================

class Ubicacion852(models.Model):
    """
    852 ## Ubicación (R)
      $a Institución o persona (NR)
      $c Estantería (R)
      $h Signatura original (NR)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ubicaciones_852'
    )

    institucion_persona = models.ForeignKey(
        'AutoridadEntidad',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='ubicaciones_852',
        help_text="852 $a — Institución o persona"
    )

    signatura_original = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="852 $h — Signatura original"
    )

    class Meta:
        verbose_name = "852 – Ubicación"
        verbose_name_plural = "📍 852 – Ubicaciones"
        ordering = ['obra', 'id']

    def __str__(self):
        if self.institucion_persona:
            return f"Ubicación: {self.institucion_persona}"
        if self.signatura_original:
            return f"Ubicación: {self.signatura_original}"
        return f"Ubicación ({self.estanterias.count()} estanterías)"


class Estanteria852(models.Model):
    """
    852 $c – Estantería (R)
    """
    ubicacion = models.ForeignKey(
        Ubicacion852,
        on_delete=models.CASCADE,
        related_name='estanterias'
    )

    estanteria = models.CharField(
        max_length=255,
        help_text="852 $c — Estantería (R)"
    )

    class Meta:
        verbose_name = "852 $c – Estantería"
        verbose_name_plural = "📚 852 $c – Estanterías"
        ordering = ['ubicacion', 'id']

    def __str__(self):
        return self.estanteria


class Disponible856(models.Model):
    """
    856 4# — Recurso disponible (R)
      $u URL (R)
      $y Texto del enlace (R)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='disponibles_856'
    )

    class Meta:
        verbose_name = "856 – Disponible"
        verbose_name_plural = "🌐 856 – Recursos disponibles"
        ordering = ['obra', 'id']

    def __str__(self):
        return f"Recurso disponible ({self.urls_856.count()} URLs)"


class URL856(models.Model):
    """
    856 $u – URL del recurso disponible (R)
    """
    disponible = models.ForeignKey(
        Disponible856,
        on_delete=models.CASCADE,
        related_name='urls_856'
    )

    url = models.URLField(
        max_length=500,
        help_text="856 $u – URL (R)"
    )

    class Meta:
        verbose_name = "856 $u – URL"
        verbose_name_plural = "🔗 856 $u – URLs"
        ordering = ['disponible', 'id']

    def __str__(self):
        return self.url[:50]


class TextoEnlace856(models.Model):
    """
    856 $y – Texto del enlace (R)
    """
    disponible = models.ForeignKey(
        Disponible856,
        on_delete=models.CASCADE,
        related_name='textos_enlace_856'
    )

    texto_enlace = models.CharField(
        max_length=255,
        help_text="856 $y – Texto del enlace (R)"
    )

    class Meta:
        verbose_name = "856 $y – Texto del enlace"
        verbose_name_plural = "📝 856 $y – Textos de enlaces"
        ordering = ['disponible', 'id']

    def __str__(self):
        return self.texto_enlace
