from django.db import models
from .obra_general import ObraGeneral

# ============================================================
# 📚 BLOQUE 6XX - Materias y Género/Forma
# ============================================================
# BLOQUE 6XX – Materias y Géneros

class Materia650(models.Model):
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_650',
    )
    materia = models.CharField(max_length=200, help_text="650 $a – Materia principal")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "650 – Materia (Tema)"
        verbose_name_plural = "650 – Materias (Temas)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.materia


class SubdivisionMateria650(models.Model):
    materia650 = models.ForeignKey(
        Materia650,
        on_delete=models.CASCADE,
        related_name='subdivisiones',
    )
    subdivision = models.CharField(max_length=200, help_text="650 $x – Subdivisión de materia")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "650 $x – Subdivisión de materia"
        verbose_name_plural = "650 $x – Subdivisiones de materia (R)"
        ordering = ['materia650', 'id']

    def __str__(self):
        return self.subdivision


class MateriaGenero655(models.Model):
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='materias_655',
    )
    materia = models.CharField(max_length=200, help_text="655 $a – Materia (género/forma)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "655 – Materia (Género/forma)"
        verbose_name_plural = "655 – Materias (Género/forma)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.materia


class SubdivisionGeneral655(models.Model):
    materia655 = models.ForeignKey(
        MateriaGenero655,
        on_delete=models.CASCADE,
        related_name='subdivisiones',
    )
    subdivision = models.CharField(max_length=200, help_text="655 $x – Subdivisión general")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "655 $x – Subdivisión general"
        verbose_name_plural = "655 $x – Subdivisiones generales (R)"
        ordering = ['materia655', 'id']

    def __str__(self):
        return self.subdivision
