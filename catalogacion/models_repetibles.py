"""
Modelos para campos MARC21 repetibles (R)
==========================================

Este archivo contiene los modelos que representan campos MARC21 marcados como 
repetibles (R), que permiten múltiples registros por obra.

Campos incluidos:
- 246: Títulos alternativos
- 250: Ediciones
- 264: Producción/Publicación/Distribución/Fabricación/Copyright
"""

from django.db import models


# ================================================
# 📌 CAMPO 246: TÍTULO ALTERNATIVO (R)
# ================================================

class TituloAlternativo(models.Model):
    """
    Campo 246 - Forma variante del título (R)
    
    Permite múltiples títulos alternativos para una obra.
    Ejemplos: títulos abreviados, títulos en otros idiomas, títulos paralelos.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='titulos_alternativos',
        help_text="Obra a la que pertenece este título alternativo"
    )
    
    # Subcampo $a - Título alternativo
    titulo = models.CharField(
        max_length=500,
        help_text="246 $a – Título abreviado o alternativo"
    )
    
    # Subcampo $b - Resto del título variante
    resto_titulo = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="246 $b – Resto del título variante"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Título Alternativo (246)"
        verbose_name_plural = "Títulos Alternativos (246)"
        ordering = ['obra', 'id']
        
    def __str__(self):
        if self.resto_titulo:
            return f"{self.titulo} {self.resto_titulo}"
        return self.titulo


# ================================================
# 📌 CAMPO 250: EDICIÓN (R)
# ================================================

class Edicion(models.Model):
    """
    Campo 250 - Edición (R)
    
    Permite múltiples ediciones para una obra.
    Ejemplos: "2a ed.", "Primera edición revisada", "Ed. crítica"
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ediciones',
        help_text="Obra a la que pertenece esta edición"
    )
    
    # Subcampo $a - Enunciado de edición
    edicion = models.CharField(
        max_length=200,
        help_text="250 $a – Edición"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Edición (250)"
        verbose_name_plural = "Ediciones (250)"
        ordering = ['obra', 'id']
        
    def __str__(self):
        return self.edicion


# ================================================
# 📌 CAMPO 264: PRODUCCIÓN/PUBLICACIÓN (R)
# ================================================

class ProduccionPublicacion(models.Model):
    """
    Campo 264 - Producción, publicación, distribución, fabricación y copyright (R)
    
    Permite múltiples entradas para distinguir entre productor, editor, distribuidor, etc.
    El segundo indicador identifica la función de la entidad:
    - 0: Producción (manuscritos)
    - 1: Publicación (material impreso)
    - 2: Distribución
    - 3: Fabricación
    - 4: Copyright
    """
    
    # Opciones para el segundo indicador (función de la entidad)
    FUNCIONES_264 = [
        ('0', 'Producción'),
        ('1', 'Publicación'),
        ('2', 'Distribución'),
        ('3', 'Fabricación'),
        ('4', 'Copyright'),
    ]
    
    # Relación con la obra principal
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='produccion_publicacion',
        help_text="Obra a la que pertenece este registro 264"
    )
    
    # Subcampo $a - Lugar
    lugar = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="264 $a – Lugar de producción, publicación, distribución o fabricación"
    )
    
    # Subcampo $b - Nombre del productor/editor/distribuidor/fabricante
    nombre_entidad = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="264 $b – Nombre del productor, editor, distribuidor o fabricante"
    )
    
    # Subcampo $c - Fecha
    fecha = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="264 $c – Fecha de producción, publicación, distribución, fabricación o copyright"
    )
    
    # Segundo indicador - Función de la entidad
    funcion = models.CharField(
        max_length=1,
        choices=FUNCIONES_264,
        default='0',
        help_text="Segundo indicador: función de la entidad (0=Producción para manuscritos)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Producción/Publicación (264)"
        verbose_name_plural = "Producciones/Publicaciones (264)"
        ordering = ['obra', 'id']
        
    def __str__(self):
        partes = []
        if self.lugar:
            partes.append(self.lugar)
        if self.nombre_entidad:
            partes.append(self.nombre_entidad)
        if self.fecha:
            partes.append(self.fecha)
        
        funcion_display = self.get_funcion_display()
        info = " : ".join(partes) if partes else "Sin datos"
        
        return f"[{funcion_display}] {info}"

#===============================================
# 📌 CAMPO 300: DESCRIPCIÓN FÍSICA 
# ================================================
# TODO: Revisar subcampos repetibles
class DescripcionFisica(models.Model):
    """
    Campo 300 - Descripción física (R)
    
    Permite múltiples descripciones físicas para una obra.
    Ejemplos: diferentes formatos o características físicas de la obra.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='descripciones_fisicas',
        help_text="Obra a la que pertenece esta descripción física"
    )
    
    # Subcampo $a - Extensión
    extension = models.CharField(
        max_length=200,
        help_text="300 $a – Extensión (ej: 1 partitura (24 p.))"
    )
    
    # Subcampo $b - Otras características físicas
    otras_caracteristicas_fisicas = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="300 $b – Otras características físicas (ej: ilustraciones, notas)"
    )
    
    # Subcampo $c - Dimensiones
    dimensiones = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="300 $c – Dimensiones (ej: 30 cm)"
    )
    
    # Subcampo $e - Material acompañante
    material_acompanante = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="300 $e – Material acompañante (ej: 1 CD)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Descripción Física (300)"
        verbose_name_plural = "Descripciones Físicas (300)"
        ordering = ['obra', 'id']
        
    def __str__(self):
        return self.extension