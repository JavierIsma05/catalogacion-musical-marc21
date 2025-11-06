from django.db import models


class AutoridadPersona(models.Model):
    """
    Base de datos de autoridades para nombres de personas.
    Se usa en: Campo 100 (compositor), Campo 600 (materia-persona), 
    Campo 700 (colaborador), Campo 773/774/787 (enlaces)
    """
    apellidos_nombres = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Formato: Apellidos, Nombres (normalizado)"
    )
    fechas = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Coordenadas biográficas: año nacimiento - año muerte"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Persona"
        verbose_name_plural = "Autoridades - Personas"
        ordering = ['apellidos_nombres']
    
    def __str__(self):
        if self.fechas:
            return f"{self.apellidos_nombres} {self.fechas}"
        return self.apellidos_nombres


class AutoridadTituloUniforme(models.Model):
    """
    Base de datos de autoridades para títulos uniformes.
    Se usa en: Campo 130 (título principal), Campo 240 (título con compositor)
    """
    titulo = models.CharField(
        max_length=300, 
        unique=True,
        help_text="Título uniforme normalizado"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Título Uniforme"
        verbose_name_plural = "Autoridades - Títulos Uniformes"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo


class AutoridadFormaMusical(models.Model):
    """
    Base de datos de autoridades para formas musicales.
    Se usa en: Campo 130 $k, Campo 240 $k, Campo 655 (género/forma)
    """
    forma = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Forma o género musical (ej: Pasillo, Sinfonía, Vals)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Forma Musical"
        verbose_name_plural = "Autoridades - Formas Musicales"
        ordering = ['forma']
    
    def __str__(self):
        return self.forma


class AutoridadMateria(models.Model):
    """
    Base de datos de autoridades para términos de materia.
    Se usa en: Campo 650 (materia general)
    """
    termino = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Término de materia normalizado"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Materia"
        verbose_name_plural = "Autoridades - Materias"
        ordering = ['termino']
    
    def __str__(self):
        return self.termino

class AutoridadEntidad(models.Model):
    """Autoridad de entidades o instituciones (710 $a)"""
    nombre = models.CharField(max_length=300, unique=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Autoridad de entidad"
        verbose_name_plural = "Autoridades de entidades"

    def __str__(self):
        return self.nombre

