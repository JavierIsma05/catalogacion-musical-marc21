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

# ================================================
#* 📌 CAMPO 020: ## ISBN (R)
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
    
    # Subcampo $2 - Fuente del código (solo si segundo indicador = 7)
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
# 📌 CAMPO 044 - CÓDIGO DEL PAÍS (Subcampo $a R)
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