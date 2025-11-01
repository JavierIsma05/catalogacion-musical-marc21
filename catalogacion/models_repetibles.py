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

CODIGOS_LENGUAJE = [
        ('ger', 'Alemán'),
        ('spa', 'Español'),
        ('fre', 'Francés'),
        ('eng', 'Inglés'),
        ('ita', 'Italiano'),
        ('por', 'Portugués'),
        # ('mul', 'Múltiples idiomas'),
        # ('und', 'Indeterminado'),
        # ('zxx', 'Sin contenido lingüístico'),
    ]

FORMAS_MUSICALES = [
        ('adaptación', 'Adaptación'),
        ('boceto', 'Boceto'),
        ('fragmento', 'Fragmento'),
        ('selección', 'Selección'),
        ('tema con variaciones', 'Tema con variaciones'),
    ]

# ================================================
#? 📌 CAMPO 020: ## ISBN (R)
# ================================================

class ISBN(models.Model):
    """
    Campo 020 - ISBN (R)
    
    Permite múltiples ISBN para una obra.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='isbns',
        help_text="Obra a la que pertenece este ISBN"
    )
    
    # Subcampo $a - ISBN
    isbn = models.CharField(
        max_length=20,
        help_text="020 $a – ISBN"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ISBN (020)"
        verbose_name_plural = "ISBN (020)"
        ordering = ['obra', 'id']
        
    def __str__(self):
        return self.isbn

# ================================================
#? 📌 CAMPO 024: ## ISMN (R)
# ================================================

class ISMN(models.Model):
    """
    Campo 024 - ISMN (R)

    Permite múltiples ISMN para una obra.
    """

    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ismns',
        help_text="Obra a la que pertenece este ISMN"
    )

    # Subcampo $a - ISMN
    ismn = models.CharField(
        max_length=20,
        help_text="024 $a – ISMN"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ISMN (024)"
        verbose_name_plural = "ISMN (024)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.ismn


# ================================================
#? 📌 CAMPO 028: 20 número de editor (R)
# ================================================

class NumeroEditor(models.Model):
    """
    Campo 028 (R) - Número de editor, distribuidor, matriz, plancha, etc.
    Permite múltiples números para distinguir entre diferentes tipos
    (publicación, matriz, plancha, videograbación, etc.)
    """
    
    # Primer indicador: Tipo de número de editor
    TIPO_NUMERO = [
        ('0', 'Número de publicación'),
        ('1', 'Número de matriz'),
        ('2', 'Número de plancha'),
        ('3', 'Otro número de música'),
        ('4', 'Número de videograbación'),
        ('5', 'Otro número de editor'),
    ]
    
    # Segundo indicador: Control de nota/punto de acceso adicional
    CONTROL_NOTA = [
        ('0', 'No hay nota ni punto de acceso adicional'),
        ('1', 'Nota, hay punto de acceso adicional'),
        ('2', 'Nota, no hay punto de acceso adicional'),
        ('3', 'No hay nota, hay punto de acceso adicional'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='numeros_editor',
        help_text="Obra a la que pertenece este número de editor"
    )
    
    # Subcampo $a - Número de editor o distribuidor (NR dentro de cada instancia)
    numero = models.CharField(
        max_length=100,
        help_text="028 $a – Número de editor, plancha, placa o código distintivo"
    )
    
    # Primer indicador
    tipo_numero = models.CharField(
        max_length=1,
        choices=TIPO_NUMERO,
        default='2',  # Predeterminado: Número de plancha
        help_text="Primer indicador: Tipo de número de editor"
    )
    
    # Segundo indicador
    control_nota = models.CharField(
        max_length=1,
        choices=CONTROL_NOTA,
        default='0',  # Predeterminado: Sin nota ni punto de acceso
        help_text="Segundo indicador: Control de nota/punto de acceso adicional"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Número de Editor (028)"
        verbose_name_plural = "Números de Editor (028 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        tipo_display = self.get_tipo_numero_display()
        return f"{tipo_display}: {self.numero}"
    
    def get_indicadores(self):
        """Retorna los indicadores en formato MARC"""
        return f"{self.tipo_numero}{self.control_nota}"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC"""
        return f"028 {self.get_indicadores()} $a{self.numero}"


# ================================================
#? 📌 CAMPO 031: ÍNCIPIT MUSICAL (R)
# ================================================

class IncipitMusical(models.Model):
    """
    Campo 031 (R) - Información del íncipit musical
    Permite múltiples íncipits para una obra (diferentes movimientos, pasajes, etc.)
    
    Un íncipit es una pequeña muestra musical del inicio de una obra,
    útil para identificación y catalogación.
    """
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='incipits_musicales',
        help_text="Obra a la que pertenece este íncipit"
    )
    
    # Subcampo $a - Número de la obra (NR)
    numero_obra = models.PositiveIntegerField(
        default=1,
        help_text="031 $a – Número de la obra (predeterminado: 1)"
    )
    
    # Subcampo $b - Número del movimiento (NR)
    numero_movimiento = models.PositiveIntegerField(
        default=1,
        help_text="031 $b – Número del movimiento (predeterminado: 1)"
    )
    
    # Subcampo $c - Número de pasaje/sistema (NR)
    numero_pasaje = models.PositiveIntegerField(
        default=1,
        help_text="031 $c – Número de pasaje o sistema (predeterminado: 1)"
    )
    
    # Subcampo $d - Título o encabezamiento (NR)
    titulo_encabezamiento = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="031 $d – Nombre del tempo o movimiento (ej: Aria, Allegro, Andante)"
    )
    
    # Subcampo $m - Voz/instrumento (NR)
    voz_instrumento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="031 $m – Voz/instrumento (usar solo si NO es para piano)"
    )
    
    # Subcampo $p - Notación musical (NR)
    notacion_musical = models.TextField(
        blank=True,
        null=True,
        help_text="031 $p – Íncipit musical codificado (ej: Plaine & Easie, MusicXML, ABC)"
    )
    
    #* Subcampo $u (R) - URL
    #* Este subcampo ES REPETIBLE, por lo que necesita su propio modelo intermedio
    #* Ver modelo: IncipitURL más abajo
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Íncipit Musical (031)"
        verbose_name_plural = "Íncipits Musicales (031 - R)"
        ordering = ['obra', 'numero_obra', 'numero_movimiento', 'numero_pasaje']
        unique_together = [
            ['obra', 'numero_obra', 'numero_movimiento', 'numero_pasaje']
        ]
    
    def __str__(self):
        partes = [
            f"Obra {self.numero_obra}",
            f"Mov. {self.numero_movimiento}",
            f"Pas. {self.numero_pasaje}"
        ]
        if self.titulo_encabezamiento:
            partes.append(f"- {self.titulo_encabezamiento}")
        return " ".join(partes)
    
    def get_identificador_completo(self):
        """Retorna el identificador completo del íncipit"""
        return f"{self.numero_obra}.{self.numero_movimiento}.{self.numero_pasaje}"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC (sin URLs)"""
        marc = f"031 ## $a{self.numero_obra} $b{self.numero_movimiento} $c{self.numero_pasaje}"
        
        if self.titulo_encabezamiento:
            marc += f" $d{self.titulo_encabezamiento}"
        
        if self.voz_instrumento:
            marc += f" $m{self.voz_instrumento}"
        
        if self.notacion_musical:
            # Truncar si es muy largo para el ejemplo
            notacion_preview = self.notacion_musical[:50] + "..." if len(self.notacion_musical) > 50 else self.notacion_musical
            marc += f" $p{notacion_preview}"
        
        return marc


class IncipitURL(models.Model):
    """
    Campo 031 - Subcampo $u (R)
    URLs asociadas a un íncipit musical
    Permite múltiples URLs por íncipit
    """
    
    incipit = models.ForeignKey(
        IncipitMusical,
        on_delete=models.CASCADE,
        related_name='urls',
        help_text="Íncipit al que pertenece esta URL"
    )
    
    # Subcampo $u - URL (R)
    url = models.URLField(
        max_length=500,
        help_text="031 $u – URL del íncipit codificado en base de datos externa"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "URL de Íncipit (031 $u)"
        verbose_name_plural = "URLs de Íncipit (031 $u - R)"
        ordering = ['incipit', 'id']
    
    def __str__(self):
        if self.descripcion:
            return f"{self.descripcion}: {self.url}"
        return self.url


# ================================================
#? 📌 CAMPO 041 - CÓDIGO DE LENGUA (R)
# ================================================

class CodigoLengua(models.Model):
    """
    Campo 041 (R) - Código de lengua
    Permite múltiples registros de idioma para una obra
    """
    
    # Primer indicador: Indicación de traducción
    INDICACION_TRADUCCION = [
        ('#', 'No se proporciona información'),
        ('0', 'El documento no es ni incluye una traducción'),
        ('1', 'El documento es o incluye una traducción'),
    ]
    
    # Segundo indicador: Fuente del código
    FUENTE_CODIGO = [
        ('#', 'Código MARC de lengua'),
        ('7', 'Fuente especificada en el subcampo $2'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='codigos_lengua',
        help_text="Obra a la que pertenece este código de lengua"
    )

    # Primer indicador
    indicacion_traduccion = models.CharField(
        max_length=1,
        choices=INDICACION_TRADUCCION,
        default='0',
        help_text="Primer indicador: ¿Es traducción?"
    )
    
    # Segundo indicador
    fuente_codigo = models.CharField(
        max_length=1,
        choices=FUENTE_CODIGO,
        default='#',
        help_text="Segundo indicador: Fuente del código"
    )
    
    #* 📌 Subcampo $a (R) - Código de lengua
    #* Este subcampo ES REPETIBLE, por lo que necesita su propio modelo intermedio
    
    fuente_especificada = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="041 $2 – Fuente del código (solo si segundo indicador es 7)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Código de Lengua (041)"
        verbose_name_plural = "Códigos de Lengua (041 - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        indicadores = f"{self.indicacion_traduccion}{self.fuente_codigo}"
        idiomas = ", ".join([idioma.get_codigo_display() for idioma in self.idiomas.all()])
        return f"041 {indicadores} - {idiomas if idiomas else 'Sin idiomas'}"
    
    def get_indicadores(self):
        """Retorna los indicadores en formato MARC"""
        return f"{self.indicacion_traduccion}{self.fuente_codigo}"
    
    def es_traduccion(self):
        """Verifica si el documento es o incluye traducción"""
        return self.indicacion_traduccion == '1'


class IdiomaObra(models.Model):
    """
    Campo 041 - Subcampo $a (R)
    Códigos de idioma asociados a un registro 041
    Permite múltiples idiomas por registro
    
    """
    
    CODIGOS_IDIOMA = CODIGOS_LENGUAJE
    
    codigo_lengua = models.ForeignKey(
        CodigoLengua,
        on_delete=models.CASCADE,
        related_name='idiomas',
        help_text="Registro 041 al que pertenece este idioma"
    )
    
    # Subcampo $a - Código de lengua (R)
    codigo = models.CharField(
        max_length=3,
        choices=CODIGOS_IDIOMA,
        default='spa',
        help_text="041 $a – Código ISO 639-2/B del idioma"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Idioma (041 $a)"
        verbose_name_plural = "Idiomas (041 $a - R)"
        ordering = ['codigo_lengua', 'id']
    
    def __str__(self):
        idioma_display = self.get_codigo_display()
        if self.nota_uso:
            return f"{idioma_display} ({self.nota_uso})"
        return idioma_display
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del idioma"""
        return self.get_codigo_display()


# ================================================
#? 📌 CAMPO 044 - CÓDIGO DEL PAÍS (Subcampo $a R)
# ================================================

class CodigoPaisEntidad(models.Model):
    """
    Campo 044 - Subcampo $a (R)
    Códigos de países asociados a la entidad editora/productora
    
    El campo 044 es NO REPETIBLE, pero el subcampo $a SÍ es repetible.
    Esto permite indicar múltiples países cuando una obra es coeditada
    o publicada en varios países simultáneamente.
    
    Nota: MARC usa códigos ISO 3166-1 alfa-2 (2 letras)
    """
    
    CODIGOS_PAIS = [
        ('ar', 'Argentina'),
        ('bo', 'Bolivia'),
        ('br', 'Brasil'),
        ('cl', 'Chile'),
        ('co', 'Colombia'),
        ('cr', 'Costa Rica'),
        ('cu', 'Cuba'),
        ('ec', 'Ecuador'),
        ('sv', 'El Salvador'),
        ('gt', 'Guatemala'),
        ('ho', 'Honduras'),
        ('mx', 'México'),
        ('nq', 'Nicaragua'),
        ('pa', 'Panamá'),
        ('pe', 'Perú'),
        ('pr', 'Puerto Rico'),
        ('dr', 'República Dominicana'),
        ('uy', 'Uruguay'),
        ('ve', 'Venezuela'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='codigos_pais_entidad',
        help_text="Obra a la que pertenece este código de país"
    )
    
    # Subcampo $a - Código MARC del país (R)
    codigo_pais = models.CharField(
        max_length=2,
        choices=CODIGOS_PAIS,
        default='ec',
        help_text="044 $a – Código ISO 3166-1 alfa-2 del país"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "País Editor/Productor (044 $a)"
        verbose_name_plural = "Países Editor/Productor (044 $a - R)"
        ordering = ['obra', 'id']
        unique_together = [['obra', 'codigo_pais']]  
    
    def __str__(self):
        pais_display = self.get_codigo_pais_display()
        if self.nota_rol:
            return f"{pais_display} ({self.nota_rol})"
        return pais_display
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del país"""
        return self.get_codigo_pais_display()
    
    def get_marc_format(self):
        """Retorna el subcampo en formato MARC"""
        return f"$a{self.codigo_pais}"


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
    
    FORMAS = FORMAS_MUSICALES
    
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
        return self.forma if isinstance(self.forma, str) else self.forma.forma


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
        default='0',  # Predeterminado: Producción
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
            return f"Copyright en {self.lugar} ({self.fecha})"
        
        return str(self)


# ================================================
# 📌 CAMPO 300: DESCRIPCIÓN FÍSICA (R)
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
    
    # Por por ahora solo $d, que es repetible y tiene su propio modelo
    
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
            marc += f" $d{tecnica.tecnica}"
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
# 📌 CAMPO 348: CARACTERÍSTICAS MÚSICA NOTADA (R)
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
        formatos = ", ".join([f.formato for f in self.formatos.all()])
        return formatos or "Sin formatos especificados"
    
    def get_marc_format(self):
        """Retorna el campo completo en formato MARC21"""
        marc = ""
        for formato in self.formatos.all():
            marc += f" $a{formato.formato}"
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
        # Evitar duplicados: mismo 348 no puede tener dos veces el mismo formato
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
        medios = ", ".join([m.medio for m in self.medios.all()])
        if medios:
            partes.append(f"Medios: {medios}")
        
        solistas = ", ".join([s.solista for s in self.solistas.all()])
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
            marc += f" $a{medio.medio}"
        
        # $b - Solistas
        for solista in self.solistas.all():
            marc += f" $b{solista.solista}"
        
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
        # Instrumentos de teclado
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
# 📌 CAMPO 383: DESIGNACIÓN NUMÉRICA OBRA MUSICAL (R)
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
        help_text=(
            "383 $a – Número de obra (ej: '1', '2', 'K. 545', 'BWV 1001', "
        )
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

# ================================================
#? 📌 CAMPO 490: MENCIÓN DE SERIE (R)
# ================================================

class MencionSerie490(models.Model):
    """
    Campo 490 (R) - Mención de serie
    Instancia de 490 que contiene título de serie e identificadores de volumen.
    El campo es REPETIBLE para obras que pertenecen a múltiples series.
    """
    
    RELACION_SERIE = [
        ('0', 'No relacionado (sin entrada secundaria)'),
        ('1', 'Relacionado (con entrada secundaria 800-830)'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='menciones_serie',
        help_text="Obra a la que pertenece"
    )
    
    # Primer indicador: relación de la serie
    relacion = models.CharField(
        max_length=1,
        choices=RELACION_SERIE,
        default='0',
        help_text="490 primer indicador – Relación: 0=no relacionado, 1=relacionado con 800-830"
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
        marc = f"490 {self.relacion}#"
        
        # $a - Títulos de serie
        for titulo in self.titulos.all():
            marc += f" $a{titulo.titulo_serie}"
        
        # $v - Volúmenes/designaciones
        for volumen in self.volumenes.all():
            marc += f" $v{volumen.volumen}"
        
        return marc if marc != f"490 {self.relacion}#" else ""


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
