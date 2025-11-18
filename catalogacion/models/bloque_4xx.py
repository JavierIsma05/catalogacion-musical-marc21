"""
Modelos MARC21 - Bloque 4XX
============================

Campos de series:
- Campo 490: Mención de serie
"""

from django.db import models


# ================================================
#? 📌 CAMPO 490: MENCIÓN DE SERIE (R)
# ================================================

class MencionSerie490(models.Model):
    """
    Campo 490 (R) - Mención de serie
    Instancia de 490 que contiene título de serie e identificadores de volumen.
    El campo es REPETIBLE para obras que pertenecen a múltiples series.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='menciones_serie',
        help_text="Obra a la que pertenece"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mención de Serie (490)"
        verbose_name_plural = "Menciones de Serie (490 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        titulos = ", ".join([t.titulo_serie for t in self.titulos.all()])
        volumenes = " ; ".join([v.volumen for v in self.volumenes.all()])
        
        if titulos and volumenes:
            return f"{titulos} ; {volumenes}"
        return titulos or volumenes or "Sin especificar"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = "490 ##"
        
        # $a - Títulos de serie
        for titulo in self.titulos.all():
            marc += f" $a{titulo.titulo_serie}"
        
        # $v - Volúmenes/designaciones
        for volumen in self.volumenes.all():
            marc += f" $v{volumen.volumen}"
        
        return marc if marc != "490 ##" else ""


class TituloSerie490(models.Model):
    """
    Subcampo $a de 490 (R)
    Mención/título de la serie
    """
    
    mencion_serie = models.ForeignKey(
        MencionSerie490,
        on_delete=models.CASCADE,
        related_name='titulos',
        help_text="Mención de serie a la que pertenece"
    )
    
    # Subcampo $a
    titulo_serie = models.CharField(
        max_length=300,
        help_text="490 $a – Título/mención de la serie (ej: 'Colección Támesis. Serie A')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Título Serie (490 $a)"
        verbose_name_plural = "Títulos Serie (490 $a - R)"
        ordering = ['mencion_serie', 'id']
    
    def __str__(self):
        return self.titulo_serie


class VolumenSerie490(models.Model):
    """
    Subcampo $v de 490 (R)
    Designación de volumen o número secuencial
    """
    
    mencion_serie = models.ForeignKey(
        MencionSerie490,
        on_delete=models.CASCADE,
        related_name='volumenes',
        help_text="Mención de serie a la que pertenece"
    )
    
    # Subcampo $v
    volumen = models.CharField(
        max_length=100,
        help_text="490 $v – Designación de volumen (ej: '260', 'Vol. 5', 'Tomo III')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Volumen (490 $v)"
        verbose_name_plural = "Volúmenes (490 $v - R)"
        ordering = ['mencion_serie', 'id']
    
    def __str__(self):
        return self.volumen
