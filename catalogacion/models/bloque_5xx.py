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
    """545 0# Datos biográficos del compositor (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='datos_biograficos_545',
    )

    class Meta:
        verbose_name = "545 – Datos biográficos del compositor"
        verbose_name_plural = "545 – Datos biográficos del compositor (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        textos = self.textos_biograficos_545.all()
        if textos.exists():
            return f"Datos biográficos: {textos.first().texto[:60]}..."
        return "Datos biográficos (sin texto)"
    
    def get_marc_format(self):
        """Retorna el formato MARC21 del campo 545"""
        marc_parts = []
        
        # Subcampo $a - Datos biográficos (repetible)
        for texto in self.textos_biograficos_545.all():
            if texto.texto:
                marc_parts.append(f"$a {texto.texto}")
        
        # Subcampo $u - URI (repetible)
        for uri in self.uris_545.all():
            if uri.uri:
                marc_parts.append(f"$u {uri.uri}")
        
        return f"545 0# {' '.join(marc_parts)}" if marc_parts else "545 0#"


class TextoBiografico545(models.Model):
    """Subcampo $a de 545 - Datos biográficos (R)"""
    dato_biografico = models.ForeignKey(
        'DatosBiograficos545',
        on_delete=models.CASCADE,
        related_name='textos_biograficos_545',
    )
    texto = models.TextField(
        help_text="545 $a – Datos biográficos del compositor (R)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "545 $a – Texto biográfico"
        verbose_name_plural = "545 $a – Textos biográficos (R)"
        ordering = ['id']

    def __str__(self):
        return f"{self.texto[:60]}..." if self.texto else "Sin texto"


class URI545(models.Model):
    """Subcampo $u de 545 - URI (R)"""
    dato_biografico = models.ForeignKey(
        'DatosBiograficos545',
        on_delete=models.CASCADE,
        related_name='uris_545',
    )
    uri = models.URLField(
        help_text="545 $u – URI (R)",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "545 $u – URI"
        verbose_name_plural = "545 $u – URIs (R)"
        ordering = ['id']

    def __str__(self):
        return self.uri if self.uri else "Sin URI"
