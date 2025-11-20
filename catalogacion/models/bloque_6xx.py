from django.db import models

# ============================================================
# 📚 BLOQUE 6XX - Materias y Género/Forma
# ============================================================

class Materia650(models.Model):
    """
    650 04 — Materia (Temas)
    Campo repetible (R)
    Subcampos:
      $a Materia (NR)
      $x Subdivisión de materia (R)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_650',
    )

    materia = models.ForeignKey(
        'AutoridadMateria',
        on_delete=models.PROTECT,
        help_text="650 $a — Materia (NR)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "650 — Materia (Tema)"
        verbose_name_plural = "650 — Materias (Temas)"
        ordering = ['obra', 'id']

    def __str__(self):
        return str(self.materia)


class SubdivisionMateria650(models.Model):
    """
    650 $x — Subdivisión de materia (R)
    """
    materia650 = models.ForeignKey(
        Materia650,
        on_delete=models.CASCADE,
        related_name='subdivisiones',
    )

    subdivision = models.CharField(
        max_length=200,
        help_text="650 $x — Subdivisión de materia (R)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "650 $x — Subdivisión de materia"
        verbose_name_plural = "650 $x — Subdivisiones de materia (R)"
        ordering = ['materia650', 'id']

    def __str__(self):
        return self.subdivision


class MateriaGenero655(models.Model):
    """
    655 #4 — Materia (Género/Forma)
    Campo repetible (R)
    Subcampos:
      $a Término género/forma (NR)
      $x Subdivisión general (R)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_655',
    )

    materia = models.ForeignKey(
        'AutoridadFormaMusical',
        on_delete=models.PROTECT,
        help_text="655 $a — Género/Forma (NR)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "655 — Materia (Género/forma)"
        verbose_name_plural = "655 — Materias (Género/forma)"
        ordering = ['obra', 'id']

    def __str__(self):
        return str(self.materia)


class SubdivisionGeneral655(models.Model):
    """
    655 $x — Subdivisión general (R)
    """
    materia655 = models.ForeignKey(
        MateriaGenero655,
        on_delete=models.CASCADE,
        related_name='subdivisiones',
    )

    subdivision = models.CharField(
        max_length=200,
        help_text="655 $x — Subdivisión general (R)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "655 $x — Subdivisión general"
        verbose_name_plural = "655 $x — Subdivisiones generales (R)"
        ordering = ['materia655', 'id']

    def __str__(self):
        return self.subdivision
