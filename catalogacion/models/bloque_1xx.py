"""
Modelos MARC21 - Bloque 1XX
============================

Puntos de acceso principales (asientos principales):
- Campo 100: Compositor (subcampos $e, $j)
- Campo 130: Titulo uniforme (subcampos $k, $m, $n, $p)
- Campo 240: Titulo uniforme con compositor (subcampos $k, $m, $n, $p)
"""

from django.db import models


FORMAS_MUSICALES = [
    ('adaptacion', 'Adaptacion'),
    ('boceto', 'Boceto'),
    ('fragmento', 'Fragmento'),
    ('seleccion', 'Seleccion'),
    ('tema con variaciones', 'Tema con variaciones'),
]


# ================================================
#? 📌 CAMPO 100 - SUBCAMPOS REPETIBLES (R)
# ================================================

class FuncionCompositor(models.Model):
    """
    Campo 100 - Subcampo $e (R)
    Termino indicativo de funcion del compositor
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
        help_text="Obra a la que pertenece esta funcion"
    )
    
    # Subcampo $e - Funcion (R)
    funcion = models.CharField(
        max_length=20,
        choices=FUNCIONES,
        default='compositor',
        help_text="100 $e – Funcion del compositor (predeterminado: compositor)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Funcion Compositor (100 $e)"
        verbose_name_plural = "Funciones Compositor (100 $e - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.get_funcion_display()


class AtribucionCompositor(models.Model):
    """
    Campo 100 - Subcampo $j (R)
    Calificador de atribucion de autoria
    Permite múltiples calificadores de autoria
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
        help_text="Obra a la que pertenece esta atribucion"
    )
    
    # Subcampo $j - Atribucion (R)
    atribucion = models.CharField(
        max_length=15,
        choices=ATRIBUCIONES,
        default='certificada',
        help_text="100 $j – Calificador de atribucion (predeterminado: certificada)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Atribucion Compositor (100 $j)"
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
    Permite múltiples formas para un titulo uniforme
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
    Medio de interpretacion para música
    Permite múltiples medios de interpretacion
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='medios_interpretacion_130',
        help_text="Obra a la que pertenece"
    )
    
    # Subcampo $m - Medio de interpretacion (R)
    medio = models.CharField(
        max_length=100,
        default='piano',
        help_text="130 $m – Medio de interpretacion (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio de Interpretacion (130 $m)"
        verbose_name_plural = "Medios de Interpretacion (130 $m - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.medio


class NumeroParteSeccion130(models.Model):
    """
    Campo 130 - Subcampo $n (R)
    Número de parte o seccion de la obra
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
        help_text="130 $n – Número de parte/seccion (ej: I, II, III o 1, 2, 3)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Parte/Seccion (130 $n)"
        verbose_name_plural = "Números de Parte/Seccion (130 $n - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.numero


class NombreParteSeccion130(models.Model):
    """
    Campo 130 - Subcampo $p (R)
    Nombre de parte o seccion de la obra
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
        help_text="130 $p – Nombre de parte/seccion (ej: Allegro, Andante, Finale)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Nombre de Parte/Seccion (130 $p)"
        verbose_name_plural = "Nombres de Parte/Seccion (130 $p - R)"
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
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='formas_240',
        help_text="Obra a la que pertenece"
    )
    
    # Usa clave foranea a AutoridadFormaMusical 
    forma = models.ForeignKey(
        'AutoridadFormaMusical',
        on_delete=models.PROTECT,
        help_text="240 $k – Forma normalizada (igual que 130 $k)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Forma (240 $k)"
        verbose_name_plural = "Formas (240 $k - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.forma.forma if self.forma else ""


class MedioInterpretacion240(models.Model):
    """
    Campo 240 - Subcampo $m (R)
    Medio de interpretacion para música (cuando hay compositor)
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
        help_text="240 $m – Medio de interpretacion (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio de Interpretacion (240 $m)"
        verbose_name_plural = "Medios de Interpretacion (240 $m - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.medio


class NumeroParteSeccion240(models.Model):
    """
    Campo 240 - Subcampo $n (R)
    Número de parte o seccion de la obra (cuando hay compositor)
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='numeros_parte_240',
        help_text="Obra a la que pertenece"
    )
    
    numero = models.CharField(
        max_length=50,
        help_text="240 $n – Número de parte/seccion (ej: I, II, III o 1, 2, 3)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Parte/Seccion (240 $n)"
        verbose_name_plural = "Números de Parte/Seccion (240 $n - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.numero


class NombreParteSeccion240(models.Model):
    """
    Campo 240 - Subcampo $p (R)
    Nombre de parte o seccion de la obra (cuando hay compositor)
    Paralelo a NombreParteSeccion130 pero para campo 240
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='nombres_parte_240',
        help_text="Obra a la que pertenece"
    )
    
    nombre = models.CharField(
        max_length=200,
        help_text="240 $p – Nombre de parte/seccion (ej: Allegro, Andante, Finale)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Nombre de Parte/Seccion (240 $p)"
        verbose_name_plural = "Nombres de Parte/Seccion (240 $p - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.nombre
