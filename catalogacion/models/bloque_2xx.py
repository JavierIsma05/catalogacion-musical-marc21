"""
Modelos MARC21 - Bloque 2XX
============================

Campos de títulos, edición y publicación:
- Campo 246: Título alternativo
- Campo 250: Edición
- Campo 264: Producción/Publicación/Distribución/Fabricación/Copyright
"""

from django.db import models


# ================================================
#? 📌 CAMPO 246: TÍTULO ALTERNATIVO (R)
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
#? 📌 CAMPO 250: EDICIÓN (R)
# ================================================

class Edicion(models.Model):
    """
    Campo 250 - Edición (R)
    
    Permite múltiples ediciones para una obra.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ediciones',
        help_text="Obra a la que pertenece esta edición"
    )
    
    # Subcampo $a - Enunciado de edición
    edicion = models.CharField(
        max_length=500,
        help_text="250 $a – Edición"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Edición (250)"
        verbose_name_plural = "Ediciones (250 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.edicion
    
    def get_marc_format(self):
        """Retorna el campo en formato MARC21"""
        return f"250 ## $a{self.edicion}"


# ================================================
#? 📌 CAMPO 264: PRODUCCIÓN/PUBLICACIÓN (R)
# ================================================

class ProduccionPublicacion(models.Model):
    """
    Campo 264 (R) - Producción, publicación, distribución, fabricación, copyright
    
    Campo completo repetible que permite múltiples instancias
    para distinguir entre diferentes funciones de entidades.
    """
    
    # Función de la entidad (segundo indicador)
    FUNCIONES = [
        ('0', 'Producción'),
        ('1', 'Publicación'),
        ('2', 'Distribución'),
        ('3', 'Fabricación'),
        ('4', 'Copyright'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='producciones_publicaciones',
        help_text="Obra a la que pertenece"
    )
    
    # Segundo indicador: Función de entidad
    funcion = models.CharField(
        max_length=1,
        choices=FUNCIONES,
        default='0',
        help_text="264 segundo indicador – Función de la entidad"
    )
    
    # Subcampo $a - Lugar (R)
    lugar = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="264 $a – Lugar de producción/publicación (R)"
    )
    
    # Subcampo $b - Nombre (R)
    nombre_entidad = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="264 $b – Nombre del productor/editor/distribuidor (R)"
    )
    
    # Subcampo $c - Fecha (R)
    fecha = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="264 $c – Fecha de producción/publicación (R)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producción/Publicación (264)"
        verbose_name_plural = "Producciones/Publicaciones (264 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        funcion_display = self.get_funcion_display()
        partes = []
        if self.lugar:
            partes.append(self.lugar)
        if self.nombre_entidad:
            partes.append(self.nombre_entidad)
        if self.fecha:
            partes.append(self.fecha)
        info = " : ".join(partes) if partes else "Sin datos"
        return f"[{funcion_display}] {info}"
    
    def get_marc_format(self):
        """Retorna el campo en formato MARC21"""
        marc = f"264 #{self.funcion}"
        if self.lugar:
            marc += f" $a{self.lugar}"
        if self.nombre_entidad:
            marc += f" $b{self.nombre_entidad}"
        if self.fecha:
            marc += f" $c{self.fecha}"
        return marc
    
    def get_vista_usuario(self):
        """Retorna vista legible para el usuario"""
        funcion_display = self.get_funcion_display()
        
        if funcion_display == 'Producción':
            return f"Producido en {self.lugar} por {self.nombre_entidad} ({self.fecha})"
        elif funcion_display == 'Publicación':
            return f"Publicado en {self.lugar} por {self.nombre_entidad} ({self.fecha})"
        elif funcion_display == 'Distribución':
            return f"Distribuido en {self.lugar} por {self.nombre_entidad} ({self.fecha})"
        elif funcion_display == 'Fabricación':
            return f"Fabricado en {self.lugar} por {self.nombre_entidad} ({self.fecha})"
        elif funcion_display == 'Copyright':
            return f"Copyright © {self.fecha} {self.nombre_entidad}"
        else:
            return str(self)
