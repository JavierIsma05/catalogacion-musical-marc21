"""
Modelos MARC21 - Bloque 1XX
============================

Puntos de acceso principales (asientos principales):
- Campo 100: Compositor (subcampos $e, $j)
- Campo 130: Título uniforme (subcampos $k, $m, $n, $p)
- Campo 240: Título uniforme con compositor (subcampos $k, $m, $n, $p)
"""

from django.db import models


FORMAS_MUSICALES = [
    ('adaptación', 'Adaptación'),
    ('boceto', 'Boceto'),
    ('fragmento', 'Fragmento'),
    ('selección', 'Selección'),
    ('tema con variaciones', 'Tema con variaciones'),
]


# ================================================
#? 📌 CAMPO 100 - SUBCAMPOS REPETIBLES (R)
# ================================================

class FuncionCompositor(models.Model):
    """
    Campo 100 - Subcampo $e (R)
    Término indicativo de función del compositor
    Permite múltiples funciones para un compositor en una obra
    """
    
    FUNCIONES = [
        ('arreglista', 'Arreglista'),
        ('coeditor', 'Coeditor'),
        ('compilador', 'Compilador'),
        ('compositor', 'Compositor'),
        ('copista', 'Copista'),
        ('dedicatario', 'Dedicatario'),
        ('editor', 'Editor'),
        ('prologuista', 'Prologuista'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='funciones_compositor',
        help_text="Obra a la que pertenece esta función"
    )
    
    # Subcampo $e - Función (R)
    funcion = models.CharField(
        max_length=20,
        choices=FUNCIONES,
        default='compositor',
        help_text="100 $e – Función del compositor (predeterminado: compositor)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Función Compositor (100 $e)"
        verbose_name_plural = "Funciones Compositor (100 $e - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.get_funcion_display()


class AtribucionCompositor(models.Model):
    """
    Campo 100 - Subcampo $j (R)
    Calificador de atribución de autoría
    Permite múltiples calificadores de autoría
    """
    
    ATRIBUCIONES = [
        ('atribuida', 'Atribuida'),
        ('certificada', 'Certificada'),
        ('erronea', 'Erronea'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='atribuciones_compositor',
        help_text="Obra a la que pertenece esta atribución"
    )
    
    # Subcampo $j - Atribución (R)
    atribucion = models.CharField(
        max_length=15,
        choices=ATRIBUCIONES,
        default='certificada',
        help_text="100 $j – Calificador de atribución (predeterminado: certificada)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Atribución Compositor (100 $j)"
        verbose_name_plural = "Atribuciones Compositor (100 $j - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.get_atribucion_display()


# ================================================
#? 📌 CAMPO 130 - SUBCAMPOS REPETIBLES (R)
# ================================================

class Forma130(models.Model):
    """
    Campo 130 - Subcampo $k (R)
    Subencabezamiento de forma
    Permite múltiples formas para un título uniforme
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='formas_130',
        help_text="Obra a la que pertenece"
    )
    
    forma = models.ForeignKey(
        'AutoridadFormaMusical',
        on_delete=models.PROTECT,
        help_text="130 $k – Forma normalizada"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Forma (130 $k)"
        verbose_name_plural = "Formas (130 $k - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.forma if isinstance(self.forma, str) else self.forma.forma


class MedioInterpretacion130(models.Model):
    """
    Campo 130 - Subcampo $m (R)
    Medio de interpretación para música
    Permite múltiples medios de interpretación
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='medios_interpretacion_130',
        help_text="Obra a la que pertenece"
    )
    
    # Subcampo $m - Medio de interpretación (R)
    medio = models.CharField(
        max_length=100,
        default='piano',
        help_text="130 $m – Medio de interpretación (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio de Interpretación (130 $m)"
        verbose_name_plural = "Medios de Interpretación (130 $m - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.medio


class NumeroParteSección130(models.Model):
    """
    Campo 130 - Subcampo $n (R)
    Número de parte o sección de la obra
    Permite múltiples números (ej: obra con varias partes)
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='numeros_parte_130',
        help_text="Obra a la que pertenece"
    )
    
    # Subcampo $n - Número de parte (R)
    numero = models.CharField(
        max_length=50,
        help_text="130 $n – Número de parte/sección (ej: I, II, III o 1, 2, 3)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Parte/Sección (130 $n)"
        verbose_name_plural = "Números de Parte/Sección (130 $n - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.numero


class NombreParteSección130(models.Model):
    """
    Campo 130 - Subcampo $p (R)
    Nombre de parte o sección de la obra
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='nombres_parte_130',
        help_text="Obra a la que pertenece"
    )
    
    # Subcampo $p - Nombre de parte (R)
    nombre = models.CharField(
        max_length=200,
        help_text="130 $p – Nombre de parte/sección (ej: Allegro, Andante, Finale)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Nombre de Parte/Sección (130 $p)"
        verbose_name_plural = "Nombres de Parte/Sección (130 $p - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.nombre


# ================================================
#? 📌 CAMPO 240 - SUBCAMPOS REPETIBLES (R)
# ================================================

class Forma240(models.Model):
    """
    Campo 240 - Subcampo $k (R)
    Subencabezamiento de forma (cuando hay compositor)
    """
    
    FORMAS = FORMAS_MUSICALES
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='formas_240',
        help_text="Obra a la que pertenece"
    )
    
    forma = models.CharField(
        max_length=50,
        choices=FORMAS,
        help_text="240 $k – Forma (cruzar con campo 655)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Forma (240 $k)"
        verbose_name_plural = "Formas (240 $k - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.get_forma_display()


class MedioInterpretacion240(models.Model):
    """
    Campo 240 - Subcampo $m (R)
    Medio de interpretación para música (cuando hay compositor)
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='medios_interpretacion_240',
        help_text="Obra a la que pertenece"
    )
    
    medio = models.CharField(
        max_length=100,
        default='piano',
        help_text="240 $m – Medio de interpretación (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio de Interpretación (240 $m)"
        verbose_name_plural = "Medios de Interpretación (240 $m - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.medio


class NumeroParteSección240(models.Model):
    """
    Campo 240 - Subcampo $n (R)
    Número de parte o sección de la obra (cuando hay compositor)
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='numeros_parte_240',
        help_text="Obra a la que pertenece"
    )
    
    numero = models.CharField(
        max_length=50,
        help_text="240 $n – Número de parte/sección (ej: I, II, III o 1, 2, 3)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Parte/Sección (240 $n)"
        verbose_name_plural = "Números de Parte/Sección (240 $n - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.numero


class NombreParteSección240(models.Model):
    """
    Campo 240 - Subcampo $p (R)
    Nombre de parte o sección de la obra (cuando hay compositor)
    Paralelo a NombreParteSección130 pero para campo 240
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='nombres_parte_240',
        help_text="Obra a la que pertenece"
    )
    
    nombre = models.CharField(
        max_length=200,
        help_text="240 $p – Nombre de parte/sección (ej: Allegro, Andante, Finale)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Nombre de Parte/Sección (240 $p)"
        verbose_name_plural = "Nombres de Parte/Sección (240 $p - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.nombre
