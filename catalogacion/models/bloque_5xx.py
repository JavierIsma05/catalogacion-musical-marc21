from django.db import models


class NotaGeneral500(models.Model):
    """500 ## Nota general (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='notas_generales_500',
    )
    nota_general = models.TextField(
        help_text="500 $a – Nota general (R)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "500 – Nota general"
        verbose_name_plural = "500 – Notas generales (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return f"Nota general: {self.nota_general[:60]}..." if self.nota_general else "Sin nota"


class Contenido505(models.Model):
    """505 00 Contenido (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='contenidos_505',
    )
    contenido = models.TextField(
        help_text="505 $a – Contenido (R)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "505 – Contenido"
        verbose_name_plural = "505 – Contenidos (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return f"Contenido: {self.contenido[:60]}..." if self.contenido else "Sin contenido"


class Sumario520(models.Model):
    """520 ## Sumario (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='sumarios_520',
    )
    sumario = models.TextField(
        help_text="520 $a – Sumario (NR)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "520 – Sumario"
        verbose_name_plural = "520 – Sumarios (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return f"Sumario: {self.sumario[:60]}..." if self.sumario else "Sin sumario"

class DatosBiograficos545(models.Model):
    """
    545 0# Datos biográficos del compositor (NR)
    Subcampos:
        $a Datos biográficos del compositor (NR)
        $u URL (NR)
    """
    obra = models.OneToOneField(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='datos_biograficos_545'
    )

    texto_biografico = models.TextField(
        help_text="545 $a – Datos biográficos del compositor (NR)",
        blank=True,
        null=True
    )

    uri = models.URLField(
        help_text="545 $u – URL con información adicional (NR)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "545 – Datos biográficos del compositor"
        verbose_name_plural = "545 – Datos biográficos del compositor"
        ordering = ['obra']

    def __str__(self):
        if self.texto_biografico:
            return f"{self.texto_biografico[:60]}..."
        return "Datos biográficos del compositor"

    def get_marc_format(self):
        """Genera el formato MARC21 correctamente formateado."""
        parts = []

        if self.texto_biografico:
            parts.append(f"$a {self.texto_biografico}")

        if self.uri:
            parts.append(f"$u {self.uri}")

        if not parts:
            return "545 0#"

        return "545 0# " + " ".join(parts)
