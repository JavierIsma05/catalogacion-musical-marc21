# ============================================================
# 📚 BLOQUE 6XX - Materias y Género/Forma (R)
# ============================================================
from django.db import models


# ==========================================================
# 🟩 650 ## Materia (Temas) (R)
# ==========================================================
class Materia650(models.Model):
    """
    650 ## Materia (Temas) (R)
    Campo repetible para temas o tópicos principales asociados a la obra.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_650'
    )
    subdivision = models.CharField(
        max_length=200,
        help_text="650 $x – Subdivisión de materia (R)"
    )

    def __str__(self):
        return self.subdivision

    class Meta:
        verbose_name = "650 $x – Subdivisión de materia"
        verbose_name_plural = "650 $x – Subdivisiones de materia (R)"
        ordering = ['obra', 'id']


# ==========================================================
# 🟨 655 ## Materia (Género/Forma) (R)
# ==========================================================
class MateriaGenero655(models.Model):
    """
    655 ## Materia (Género/Forma) (R)
    Campo repetible para géneros o formas musicales relacionadas con la obra.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_genero_655'
    )
    subdivision_general = models.CharField(
        max_length=200,
        help_text="655 $x – Subdivisión general (R)"
    )

    def __str__(self):
        return self.subdivision_general

    class Meta:
        verbose_name = "655 $x – Subdivisión general"
        verbose_name_plural = "655 $x – Subdivisiones generales (R)"
        ordering = ['obra', 'id']
