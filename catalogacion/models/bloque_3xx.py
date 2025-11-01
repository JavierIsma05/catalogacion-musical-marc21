"""
Modelos MARC21 - Bloque 3XX
============================

Campos de descripción física y características técnicas:
- Campo 300: Descripción física
- Campo 340: Medio físico (técnica)
- Campo 348: Características de música notada
- Campo 382: Medio de interpretación
- Campo 383: Designación numérica de obra musical
"""

from django.db import models


# ================================================
#? 📌 CAMPO 300: DESCRIPCIÓN FÍSICA (R)
# ================================================

class DescripcionFisica(models.Model):
    """
    Campo 300 (R) - Descripción física
    
    Instancia completa de 300 con subcampos NR ($b, $e) integrados
    y subcampos R ($a, $c) en modelos separados (Extension300, Dimension300).
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='descripciones_fisicas',
        help_text="Obra a la que pertenece"
    )
    
    # Subcampo $b - Características (NR)
    otras_caracteristicas_fisicas = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $b – Otras características físicas (NR)"
    )
    
    # Subcampo $e - Material acompañante (NR)
    material_acompanante = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $e – Material acompañante (NR)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Descripción Física (300)"
        verbose_name_plural = "Descripciones Físicas (300 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        extensiones = ", ".join([e.extension for e in self.extensiones.all()])
        if self.otras_caracteristicas_fisicas:
            extensiones += f" ; {self.otras_caracteristicas_fisicas}"
        if self.dimensiones_set.exists():
            dims = ", ".join([d.dimension for d in self.dimensiones_set.all()])
            extensiones += f" ; {dims}"
        return extensiones or "Sin descripción"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        
        # Agregar todas las extensiones ($a - R)
        for ext in self.extensiones.all():
            marc += f" $a{ext.extension}"
        
        # Agregar características ($b - NR)
        if self.otras_caracteristicas_fisicas:
            marc += f" $b{self.otras_caracteristicas_fisicas}"
        
        # Agregar todas las dimensiones ($c - R)
        for dim in self.dimensiones_set.all():
            marc += f" $c{dim.dimension}"
        
        # Agregar material acompañante ($e - NR)
        if self.material_acompanante:
            marc += f" $e{self.material_acompanante}"
        
        return f"300 ##" + marc if marc else ""


class Extension300(models.Model):
    """
    Subcampo $a de 300 (R)
    Extensión - REPETIBLE dentro de cada 300
    
    Ejemplos: "1 partitura (24 p.)", "32 páginas", "1 cuadernillo (12 p.)"
    """
    
    descripcion_fisica = models.ForeignKey(
        DescripcionFisica,
        on_delete=models.CASCADE,
        related_name='extensiones',
        help_text="Descripción física a la que pertenece"
    )
    
    extension = models.CharField(
        max_length=500,
        help_text="300 $a – Extensión (ej: '1 partitura (24 p.)')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Extensión (300 $a)"
        verbose_name_plural = "Extensiones (300 $a - R)"
        ordering = ['descripcion_fisica', 'id']
    
    def __str__(self):
        return self.extension


class Dimension300(models.Model):
    """
    Subcampo $c de 300 (R)
    Dimensiones - REPETIBLE dentro de cada 300
    
    Ejemplos: "30 cm", "23 cm", "2.5 MB", "25 x 30 cm"
    """
    
    descripcion_fisica = models.ForeignKey(
        DescripcionFisica,
        on_delete=models.CASCADE,
        related_name='dimensiones_set',
        help_text="Descripción física a la que pertenece"
    )
    
    dimension = models.CharField(
        max_length=200,
        help_text="300 $c – Dimensión (ej: '30 cm', '2.5 MB')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Dimensión (300 $c)"
        verbose_name_plural = "Dimensiones (300 $c - R)"
        ordering = ['descripcion_fisica', 'id']
    
    def __str__(self):
        return self.dimension


# ================================================
#? 📌 CAMPO 340: MEDIO FÍSICO (R)
# ================================================

class MedioFisico(models.Model):
    """
    Campo 340 (R) - Instancia de 340
    
    Contenedor para técnicas de registro (340 $d).
    El campo 340 puede repetirse múltiples veces.
    Dentro de cada 340, el subcampo $d es también REPETIBLE.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='medios_fisicos',
        help_text="Obra a la que pertenece"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio Físico (340)"
        verbose_name_plural = "Medios Físicos (340 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        tecnicas = ", ".join([t.tecnica for t in self.tecnicas.all()])
        return tecnicas or "Sin técnicas"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        for tecnica in self.tecnicas.all():
            marc += f" $d{tecnica.get_tecnica_display()}"
        return f"340 ##" + marc if marc else ""


class Tecnica340(models.Model):
    """
    Subcampo $d de 340 (R)
    Técnica en que se registra la información - REPETIBLE dentro de cada 340
    
    Ejemplos:
    - Una obra puede ser: "manuscrito" + "autógrafo"
    - Una obra puede ser: "impreso" + "fotocopia de impreso"
    """
    
    TECNICAS = [
        ('autógrafo', 'Autógrafo'),
        ('posible autógrafo', 'Posible autógrafo'),
        ('manuscrito', 'Manuscrito'),
        ('manuscrito de copista no identificado', 'Manuscrito de copista no identificado'),
        ('impreso', 'Impreso'),
        ('fotocopia de manuscrito', 'Fotocopia de manuscrito'),
        ('fotocopia de impreso', 'Fotocopia de impreso'),
    ]
    
    medio_fisico = models.ForeignKey(
        MedioFisico,
        on_delete=models.CASCADE,
        related_name='tecnicas',
        help_text="Medio físico al que pertenece"
    )
    
    # Subcampo $d - Técnica (R)
    tecnica = models.CharField(
        max_length=50,
        choices=TECNICAS,
        help_text="340 $d – Técnica de registro (repetible dentro de cada 340)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Técnica (340 $d)"
        verbose_name_plural = "Técnicas (340 $d - R)"
        ordering = ['medio_fisico', 'id']
    
    def __str__(self):
        return self.get_tecnica_display()


# ================================================
#? 📌 CAMPO 348: CARACTERÍSTICAS MÚSICA NOTADA (R)
# ================================================

class CaracteristicaMusicaNotada(models.Model):
    """
    Campo 348 (R) - Instancia de 348
    
    Contenedor para formatos de presentación de música notada (348 $a).
    El campo 348 puede repetirse múltiples veces.
    Dentro de cada 348, el subcampo $a es también REPETIBLE.
    
    NOTA IMPORTANTE: No se usa este campo si la música es para piano
    en doble pauta tradicional (es el formato estándar y no necesita especificarse).
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='caracteristicas_musica_notada',
        help_text="Obra a la que pertenece"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Característica Música Notada (348)"
        verbose_name_plural = "Características Música Notada (348 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        formatos = ", ".join([f.get_formato_display() for f in self.formatos.all()])
        return formatos or "Sin formatos especificados"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        for formato in self.formatos.all():
            marc += f" $a{formato.get_formato_display()}"
        return f"348 ##" + marc if marc else ""


class Formato348(models.Model):
    """
    Subcampo $a de 348 (R)
    Término del formato de música notada - REPETIBLE dentro de cada 348

    NOTA: No usar este campo si es piano en doble pauta tradicional
    """
    
    FORMATOS = [
        ('parte', 'Parte'),
        ('partitura', 'Partitura'),
        ('partitura de coro', 'Partitura de coro'),
        ('partitura piano vocal', 'Partitura piano-vocal')
    ]
    
    caracteristica = models.ForeignKey(
        CaracteristicaMusicaNotada,
        on_delete=models.CASCADE,
        related_name='formatos',
        help_text="Característica a la que pertenece"
    )
    
    # Subcampo $a - Formato (R)
    formato = models.CharField(
        max_length=50,
        choices=FORMATOS,
        help_text="348 $a – Formato de presentación (repetible dentro de cada 348)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Formato (348 $a)"
        verbose_name_plural = "Formatos (348 $a - R)"
        ordering = ['caracteristica', 'id']
        unique_together = [['caracteristica', 'formato']]
    
    def __str__(self):
        return self.get_formato_display()


# ================================================
#? 📌 CAMPO 382: MEDIO DE INTERPRETACIÓN (R)
# ================================================

class MedioInterpretacion382(models.Model):
    """
    Campo 382 (R) - Medio de interpretación
    
    Instancia de 382 que agrupa subcampos $a, $b, $n que describen
    los instrumentos/voces y solistas de una obra.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='medios_interpretacion_382',
        help_text="Obra a la que pertenece"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio de Interpretación (382)"
        verbose_name_plural = "Medios de Interpretación (382 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        partes = []
        medios = ", ".join([m.get_medio_display() for m in self.medios.all()])
        if medios:
            partes.append(f"Medios: {medios}")
        
        solistas = ", ".join([s.get_solista_display() for s in self.solistas.all()])
        if solistas:
            partes.append(f"Solistas: {solistas}")
        
        numeros = ", ".join([str(n.numero) for n in self.numeros_interpretes.all()])
        if numeros:
            partes.append(f"Cantidad: {numeros}")
        
        return " | ".join(partes) or "Sin especificar"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        
        # $a - Medios
        for medio in self.medios.all():
            marc += f" $a{medio.get_medio_display()}"
        
        # $b - Solistas
        for solista in self.solistas.all():
            marc += f" $b{solista.get_solista_display()}"
        
        # $n - Números
        for numero in self.numeros_interpretes.all():
            marc += f" $n{numero.numero}"
        
        return f"382 ##" + marc if marc else ""


class MedioInterpretacion382_a(models.Model):
    """
    Subcampo $a de 382 (R)
    Medio de interpretación - instrumento, voz o conjunto
    """
    
    MEDIOS = [
        ('piano', 'Piano'),
        ('dos pianos', 'Dos pianos'),
        ('piano a cuatro manos', 'Piano a cuatro manos'),
        ('piano con acompañamiento', 'Piano con acompañamiento'),
    ]
    
    medio_interpretacion = models.ForeignKey(
        MedioInterpretacion382,
        on_delete=models.CASCADE,
        related_name='medios',
        help_text="Medio de interpretación al que pertenece"
    )
    
    # Subcampo $a
    medio = models.CharField(
        max_length=50,
        choices=MEDIOS,
        default='piano',
        help_text="382 $a – Medio de interpretación (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medio (382 $a)"
        verbose_name_plural = "Medios (382 $a - R)"
        ordering = ['medio_interpretacion', 'id']
    
    def __str__(self):
        return self.get_medio_display()


class Solista382(models.Model):
    """
    Subcampo $b de 382 (R)
    Solista - voz o instrumento solista específico
    """
    
    SOLISTAS = [
        ('piano', 'Piano'),
    ]
    
    medio_interpretacion = models.ForeignKey(
        MedioInterpretacion382,
        on_delete=models.CASCADE,
        related_name='solistas',
        help_text="Medio de interpretación al que pertenece"
    )
    
    # Subcampo $b
    solista = models.CharField(
        max_length=50,
        choices=SOLISTAS,
        default='piano',
        help_text="382 $b – Solista (predeterminado: piano)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Solista (382 $b)"
        verbose_name_plural = "Solistas (382 $b - R)"
        ordering = ['medio_interpretacion', 'id']
    
    def __str__(self):
        return self.get_solista_display()


class NumeroInterpretes382(models.Model):
    """
    Subcampo $n de 382 (R)
    Número de intérpretes de un mismo medio
    """
    
    medio_interpretacion = models.ForeignKey(
        MedioInterpretacion382,
        on_delete=models.CASCADE,
        related_name='numeros_interpretes',
        help_text="Medio de interpretación al que pertenece"
    )
    
    # Subcampo $n
    numero = models.PositiveIntegerField(
        help_text="382 $n – Número de intérpretes de un mismo medio (ej: 2, 4, 8)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número Intérpretes (382 $n)"
        verbose_name_plural = "Números Intérpretes (382 $n - R)"
        ordering = ['medio_interpretacion', 'id']
    
    def __str__(self):
        return f"{self.numero} intérpretes"


# ================================================
#? 📌 CAMPO 383: DESIGNACIÓN NUMÉRICA OBRA MUSICAL (R)
# ================================================

class DesignacionNumericaObra(models.Model):
    """
    Campo 383 (R) - Designación numérica de obra musical
    Instancia de 383 que agrupa subcampos $a (número de obra) y
    $b (opus) que identifican numéricamente una composición musical.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='designaciones_numericas',
        help_text="Obra a la que pertenece"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Designación Numérica (383)"
        verbose_name_plural = "Designaciones Numéricas (383 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        partes = []
        
        numeros = self.numeros_obra.all()
        if numeros.exists():
            nums = ", ".join([n.numero_obra for n in numeros])
            partes.append(f"Número: {nums}")
        
        opus = self.opus.all()
        if opus.exists():
            opus_vals = ", ".join([o.opus for o in opus])
            partes.append(f"Opus: {opus_vals}")
        
        return " | ".join(partes) or "Sin designación"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        
        # $a - Números de obra
        for numero in self.numeros_obra.all():
            marc += f" $a{numero.numero_obra}"
        
        # $b - Opus
        for opus_obj in self.opus.all():
            marc += f" $b{opus_obj.opus}"
        
        return f"383 ##" + marc if marc else ""


class NumeroObra383(models.Model):
    """
    Subcampo $a de 383 (R)
    Número de obra o serie - identificador numérico
    """
    
    designacion_numerica = models.ForeignKey(
        DesignacionNumericaObra,
        on_delete=models.CASCADE,
        related_name='numeros_obra',
        help_text="Designación a la que pertenece"
    )
    
    # Subcampo $a
    numero_obra = models.CharField(
        max_length=100,
        help_text="383 $a – Número de obra (ej: '1', '2', 'K. 545', 'BWV 1001')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Obra (383 $a)"
        verbose_name_plural = "Números de Obra (383 $a - R)"
        ordering = ['designacion_numerica', 'id']
    
    def __str__(self):
        return self.numero_obra


class Opus383(models.Model):
    """
    Subcampo $b de 383 (R)
    Número de Opus - designación opus estándar
    """
    
    designacion_numerica = models.ForeignKey(
        DesignacionNumericaObra,
        on_delete=models.CASCADE,
        related_name='opus',
        help_text="Designación a la que pertenece"
    )
    
    # Subcampo $b
    opus = models.CharField(
        max_length=100,
        help_text="383 $b – Número de Opus (ej: 'Op. 27, No. 2', 'Op. 131')"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Opus (383 $b)"
        verbose_name_plural = "Opus (383 $b - R)"
        ordering = ['designacion_numerica', 'id']
    
    def __str__(self):
        return self.opus
