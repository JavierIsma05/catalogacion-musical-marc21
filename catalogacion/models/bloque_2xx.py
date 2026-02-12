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
# ? 📌 CAMPO 246: TÍTULO ALTERNATIVO (R)
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

    # Subcampo $a - Título alternativo (NR)
    titulo = models.CharField(
        max_length=500,
        help_text="246 $a – Título abreviado o alternativo"
    )

    # Subcampo $b - Subtítulo (NR)
    subtitulo = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="246 $b – Subtitulo"
    )

    # Subcampo $i - Texto de visualización (NR)
    texto_visualizacion = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="246 $i – Texto de visualización"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Título Alternativo (246)"
        verbose_name_plural = "Títulos Alternativos (246)"
        ordering = ['obra', 'id']

    def __str__(self):
        partes = [self.titulo]
        if self.subtitulo:
            partes.append(self.subtitulo)
        if self.texto_visualizacion:
            partes.append(f"[{self.texto_visualizacion}]")
        return " - ".join(filter(None, partes))


# ================================================
# ? 📌 CAMPO 250: EDICIÓN (R)
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
# ? 📌 CAMPO 264: PRODUCCIÓN/PUBLICACIÓN (R)
# ================================================

class ProduccionPublicacion(models.Model):
    """
    Campo 264 (R) - Producción, publicación, distribución, fabricación, copyright

    Campo completo repetible que permite múltiples instancias.
    Cada instancia puede tener múltiples lugares, entidades y fechas (subcampos R).
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
        help_text="264 segundo indicador – Función de la entidad (predeterminado: Producción para manuscritos)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producción/Publicación (264)"
        verbose_name_plural = "Producciones/Publicaciones (264 - R)"
        ordering = ['obra', 'id']

    def __str__(self):
        funcion_display = self.get_funcion_display()
        lugares = list(self.lugares.values_list('lugar', flat=True))
        entidades = list(self.entidades.values_list('nombre', flat=True))
        fechas = list(self.fechas.values_list('fecha', flat=True))

        partes = []
        if lugares:
            partes.append(", ".join(lugares))
        if entidades:
            partes.append(", ".join(entidades))
        if fechas:
            partes.append(", ".join(fechas))

        info = " : ".join(partes) if partes else "Sin datos"
        return f"[{funcion_display}] {info}"

    def get_marc_format(self):
        """Retorna el campo en formato MARC21"""
        marc = f"264 #{self.funcion}"

        for lugar in self.lugares.all():
            marc += f" $a{lugar.lugar}"
        for entidad in self.entidades.all():
            marc += f" $b{entidad.nombre}"
        for fecha in self.fechas.all():
            marc += f" $c{fecha.fecha}"

        return marc if marc != f"264 #{self.funcion}" else ""


class Lugar264(models.Model):
    """
    Subcampo $a de 264 (R)
    Lugar - REPETIBLE dentro de cada 264

    Ejemplos: "Quito", "Madrid", "New York"
    """

    produccion_publicacion = models.ForeignKey(
        ProduccionPublicacion,
        on_delete=models.CASCADE,
        related_name='lugares',
        help_text="Producción/Publicación a la que pertenece"
    )

    lugar = models.CharField(
        max_length=200,
        help_text="264 $a – Lugar de producción/publicación"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lugar (264 $a)"
        verbose_name_plural = "Lugares (264 $a - R)"
        ordering = ['produccion_publicacion', 'id']

    def __str__(self):
        return self.lugar


class NombreEntidad264(models.Model):
    """
    Subcampo $b de 264 (R)
    Nombre de entidad - REPETIBLE dentro de cada 264

    Ejemplos: "Editorial Música Andina", "Casa de la Cultura Ecuatoriana"
    """

    produccion_publicacion = models.ForeignKey(
        ProduccionPublicacion,
        on_delete=models.CASCADE,
        related_name='entidades',
        help_text="Producción/Publicación a la que pertenece"
    )

    nombre = models.CharField(
        max_length=300,
        help_text="264 $b – Nombre del productor/editor/distribuidor"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Nombre de Entidad (264 $b)"
        verbose_name_plural = "Nombres de Entidades (264 $b - R)"
        ordering = ['produccion_publicacion', 'id']

    def __str__(self):
        return self.nombre


class Fecha264(models.Model):
    """
    Subcampo $c de 264 (R)
    Fecha - REPETIBLE dentro de cada 264

    Ejemplos: "2023", "[2023]", "©2023"
    """

    produccion_publicacion = models.ForeignKey(
        ProduccionPublicacion,
        on_delete=models.CASCADE,
        related_name='fechas',
        help_text="Producción/Publicación a la que pertenece"
    )

    fecha = models.CharField(
        max_length=100,
        help_text="264 $c – Fecha de producción/publicación"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fecha (264 $c)"
        verbose_name_plural = "Fechas (264 $c - R)"
        ordering = ['produccion_publicacion', 'id']

    def __str__(self):
        return self.fecha
