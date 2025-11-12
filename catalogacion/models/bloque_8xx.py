# ============================================================
# 📦 BLOQUE 8XX – UBICACIÓN Y DISPONIBILIDAD (R)
# ============================================================
from django.db import models
from .obra_general import ObraGeneral


# ============================================================
# 🗂️ 852 ## Ubicación (R)
# ============================================================
class Estanteria852(models.Model):
    """
    852 $c – Estantería (R)
    Puede haber múltiples ubicaciones físicas o estanterías por obra.
    """
    obra = models.ForeignKey(
        ObraGeneral,
        on_delete=models.CASCADE,
        related_name='estanterias_852'
    )

    estanteria = models.CharField(
        max_length=255,
        help_text="852 $c – Estantería (R)"
    )

    def __str__(self):
        return self.estanteria

    class Meta:
        verbose_name = "852 $c – Estantería"
        verbose_name_plural = "📚 852 $c – Estanterías"


# ============================================================
# 🌐 856 ## Disponible (R)
# ============================================================
class Disponible856(models.Model):
    """
    856 4# – Recurso electrónico disponible (R)
    Puede repetirse para múltiples enlaces o formatos digitales.
    """
    obra = models.ForeignKey(
        ObraGeneral,
        on_delete=models.CASCADE,
        related_name='recursos_disponibles_856'
    )

    url = models.URLField(
        max_length=500,
        help_text="856 $u – URL del recurso (R)"
    )

    texto_enlace = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="856 $y – Texto del enlace (R)"
    )

    def __str__(self):
        return f"{self.texto_enlace or 'Recurso disponible'} → {self.url}"

    class Meta:
        verbose_name = "856 – Recurso disponible"
        verbose_name_plural = "🌐 856 – Recursos disponibles"
