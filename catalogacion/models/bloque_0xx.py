"""
Modelos MARC21 - Bloque 0XX
============================

Campos de control, números de identificación y códigos:
- Campo 020: ISBN
- Campo 024: ISMN
- Campo 028: Número de editor
- Campo 031: Íncipit musical
- Campo 041: Código de lengua
- Campo 044: Código de país
"""

from django.db import models


CODIGOS_LENGUAJE = [
    ("ger", "Alemán"),
    ("spa", "Español"),
    ("fre", "Francés"),
    ("eng", "Inglés"),
    ("ita", "Italiano"),
    ("por", "Portugués"),
]


# ================================================
# ? 📌 CAMPO 020: ISBN (R)
# ================================================


class ISBN(models.Model):
    """
    Campo 020 - ISBN (R)

    Permite múltiples ISBN para una obra.
    """

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="isbns",
        help_text="Obra a la que pertenece este ISBN",
    )

    # Subcampo $a - ISBN
    isbn = models.CharField(max_length=20, help_text="020 $a – ISBN")

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ISBN (020)"
        verbose_name_plural = "ISBN (020)"
        ordering = ["obra", "id"]

    def __str__(self):
        return self.isbn


# ================================================
# ? 📌 CAMPO 024: ISMN (R)
# ================================================


class ISMN(models.Model):
    """
    Campo 024 - ISMN (R)

    Permite múltiples ISMN para una obra.
    """

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="ismns",
        help_text="Obra a la que pertenece este ISMN",
    )

    # Subcampo $a - ISMN
    ismn = models.CharField(max_length=20, help_text="024 $a – ISMN")

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ISMN (024)"
        verbose_name_plural = "ISMN (024)"
        ordering = ["obra", "id"]

    def __str__(self):
        return self.ismn


# ================================================
# ? 📌 CAMPO 028: Número de editor (R)
# ================================================


class NumeroEditor(models.Model):
    """
    Campo 028 (R) - Número de editor, distribuidor, matriz, plancha, etc.
    Permite múltiples números para distinguir entre diferentes tipos
    (publicación, matriz, plancha, videograbación, etc.)
    """

    # Primer indicador: Tipo de número de editor
    TIPO_NUMERO = [
        ("0", "Número de publicación"),
        ("1", "Número de matriz"),
        ("2", "Número de plancha"),
        ("3", "Otro número de música"),
        ("4", "Número de videograbación"),
        ("5", "Otro número de editor"),
    ]

    # Segundo indicador: Control de nota/punto de acceso adicional
    CONTROL_NOTA = [
        ("0", "No hay nota ni punto de acceso adicional"),
        ("1", "Nota, hay punto de acceso adicional"),
        ("2", "Nota, no hay punto de acceso adicional"),
        ("3", "No hay nota, hay punto de acceso adicional"),
    ]

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="numeros_editor",
        help_text="Obra a la que pertenece este número de editor",
    )

    # Subcampo $a - Número de editor o distribuidor (NR dentro de cada instancia)
    numero_editor = models.CharField(
        max_length=100,
        help_text="028 $a – Número de editor, plancha, placa o código distintivo",
    )

    # Primer indicador
    tipo_numero = models.CharField(
        max_length=1,
        choices=TIPO_NUMERO,
        default="2",
        help_text="Primer indicador: Tipo de número de editor",
    )

    # Segundo indicador
    control_nota = models.CharField(
        max_length=1,
        choices=CONTROL_NOTA,
        default="0",
        help_text="Segundo indicador: Control de nota/punto de acceso adicional",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Número de Editor (028)"
        verbose_name_plural = "Números de Editor (028 - R)"
        ordering = ["obra", "id"]

    def __str__(self):
        tipo_display = self.get_tipo_numero_display()
        return f"{tipo_display}: {self.numero_editor}"

    def get_indicadores(self):
        """Retorna los indicadores en formato MARC"""
        return f"{self.tipo_numero}{self.control_nota}"

    def get_marc_format(self):
        """Retorna el campo completo en formato MARC"""
        return f"028 {self.get_indicadores()} $a{self.numero_editor}"


# ================================================
# ? 📌 CAMPO 031: ÍNCIPIT MUSICAL (R)
# ================================================


class IncipitMusical(models.Model):
    """
    Campo 031 (R) - Información del íncipit musical
    Permite múltiples íncipits para una obra (diferentes movimientos, pasajes, etc.)

    Un íncipit es una pequeña muestra musical del inicio de una obra,
    útil para identificación y catalogación.
    """

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="incipits_musicales",
        help_text="Obra a la que pertenece este íncipit",
    )

    # Subcampo $a - Número de la obra (NR)
    numero_obra = models.PositiveIntegerField(
        default=1, help_text="031 $a – Número de la obra (predeterminado: 1)"
    )

    # Subcampo $b - Número del movimiento (NR)
    numero_movimiento = models.PositiveIntegerField(
        default=1, help_text="031 $b – Número del movimiento (predeterminado: 1)"
    )

    # Subcampo $c - Número de pasaje/sistema (NR)
    numero_pasaje = models.PositiveIntegerField(
        default=1, help_text="031 $c – Número de pasaje o sistema (predeterminado: 1)"
    )

    # Subcampo $d - Título o encabezamiento (NR)
    titulo_encabezamiento = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="031 $d – Nombre del tempo o movimiento (ej: Aria, Allegro, Andante)",
    )
    #  Subcampo$e – Personaje
    personaje = models.CharField(
        max_length=200, blank=True, null=True, help_text="031 $e – Personaje"
    )

    # Subcampo $g – Clave musical (ej. G-2, F-4)
    clave = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="031 $g – Clave musical (ej.: G-2, F-4)",
    )

    # Subcampo $m - Voz/instrumento (NR)
    voz_instrumento = models.CharField(
        max_length=100,
        blank=True,
        default="piano",
        null=True,
        help_text="031 $m – Voz/instrumento",
    )

    # Subcampo $n – Armadura (ej. bBE)
    armadura = models.CharField(
        max_length=20, blank=True, null=True, help_text="031 $n – Armadura"
    )

    # Subcampo $p - Notación musical (PAE)
    notacion_musical = models.TextField(
        blank=True,
        null=True,
        help_text="031 $p – Íncipit musical codificado en PAE (Plaine & Easie)",
    )

    # Subcampo $q – Nota general
    nota_general = models.TextField(
        blank=True, null=True, help_text="031 $q – Nota general"
    )

    # Subcampo $r – Tonalidad o modo
    tonalidad_modo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="031 $r – Tonalidad o modo (ej.: g, C mayor)",
    )

    # Subcampo $s – Nota de validez codificada
    nota_validez_codificada = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="031 $s – Nota de validez codificada",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Íncipit Musical (031)"
        verbose_name_plural = "Íncipits Musicales (031 - R)"
        ordering = ["obra", "numero_obra", "numero_movimiento", "numero_pasaje"]
        unique_together = [
            ["obra", "numero_obra", "numero_movimiento", "numero_pasaje"]
        ]

    def __str__(self):
        partes = [
            f"Obra {self.numero_obra}",
            f"Mov. {self.numero_movimiento}",
            f"Pas. {self.numero_pasaje}",
        ]
        if self.titulo_encabezamiento:
            partes.append(f"- {self.titulo_encabezamiento}")
        return " ".join(partes)

    def get_marc_format(self):
        """Retorna el campo completo en formato MARC (sin URLs)."""
        marc = f"031 ## $a{self.numero_obra} $b{self.numero_movimiento} $c{self.numero_pasaje}"

        if self.titulo_encabezamiento:
            marc += f" $d{self.titulo_encabezamiento}"

        if self.personaje:
            marc += f" $e{self.personaje}"

        if self.clave:
            marc += f" $g{self.clave}"

        if self.voz_instrumento:
            marc += f" $m{self.voz_instrumento}"

        if self.armadura:
            marc += f" $n{self.armadura}"

        if self.notacion_musical:
            prev = (
                self.notacion_musical[:50] + "..."
                if len(self.notacion_musical) > 50
                else self.notacion_musical
            )
            marc += f" $p{prev}"

        if self.nota_general:
            marc += f" $q{self.nota_general}"

        if self.tonalidad_modo:
            marc += f" $r{self.tonalidad_modo}"

        if self.nota_validez_codificada:
            marc += f" $s{self.nota_validez_codificada}"

        return marc

    def get_identificador_completo(self):
        """Retorna el identificador completo del íncipit"""
        return f"{self.numero_obra}.{self.numero_movimiento}.{self.numero_pasaje}"


class IncipitURL(models.Model):
    """
    Campo 031 - Subcampo $u (R)
    URLs asociadas a un íncipit musical
    Permite múltiples URLs por íncipit
    """

    incipit = models.ForeignKey(
        IncipitMusical,
        on_delete=models.CASCADE,
        related_name="urls",
        help_text="Íncipit al que pertenece esta URL",
    )

    # Subcampo $u - URL (R)
    url = models.URLField(
        max_length=500,
        help_text="031 $u – URL del íncipit codificado en base de datos externa",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "URL de Íncipit (031 $u)"
        verbose_name_plural = "URLs de Íncipit (031 $u - R)"
        ordering = ["incipit", "id"]

    def __str__(self):
        return self.url


# ================================================
# ? 📌 CAMPO 041 - CÓDIGO DE LENGUA (R)
# ================================================


class CodigoLengua(models.Model):
    """
    Campo 041 (R) - Código de lengua
    Permite múltiples registros de idioma para una obra
    """

    # Primer indicador: Indicación de traducción
    INDICACION_TRADUCCION = [
        ("#", "No se proporciona información"),
        ("0", "El documento no es ni incluye una traducción"),
        ("1", "El documento es o incluye una traducción"),
    ]

    # Segundo indicador: Fuente del código
    FUENTE_CODIGO = [
        ("#", "Código MARC de lengua"),
        ("7", "Fuente especificada en el subcampo $2"),
    ]

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="codigos_lengua",
        help_text="Obra a la que pertenece este código de lengua",
    )

    # Primer indicador
    indicacion_traduccion = models.CharField(
        max_length=1,
        choices=INDICACION_TRADUCCION,
        default="0",
        help_text="Primer indicador: ¿Es traducción?",
    )

    # Segundo indicador
    fuente_codigo = models.CharField(
        max_length=1,
        choices=FUENTE_CODIGO,
        default="#",
        help_text="Segundo indicador: Fuente del código",
    )

    fuente_especificada = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="041 $2 – Fuente del código (solo si segundo indicador es 7)",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Código de Lengua (041)"
        verbose_name_plural = "Códigos de Lengua (041 - R)"
        ordering = ["obra", "id"]

    def __str__(self):
        indicadores = f"{self.indicacion_traduccion}{self.fuente_codigo}"
        idiomas = ", ".join(
            [idioma.get_codigo_idioma_display() for idioma in self.idiomas.all()]
        )
        return f"041 {indicadores} - {idiomas if idiomas else 'Sin idiomas'}"

    def get_indicadores(self):
        """Retorna los indicadores en formato MARC"""
        return f"{self.indicacion_traduccion}{self.fuente_codigo}"

    def es_traduccion(self):
        """Verifica si el documento es o incluye traducción"""
        return self.indicacion_traduccion == "1"


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
        related_name="idiomas",
        help_text="Registro 041 al que pertenece este idioma",
    )

    # Subcampo $a - Código de lengua (R)
    codigo_idioma = models.CharField(
        max_length=3,
        choices=CODIGOS_IDIOMA,
        default="spa",
        help_text="041 $a – Código ISO 639-2/B del idioma",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Idioma (041 $a)"
        verbose_name_plural = "Idiomas (041 $a - R)"
        ordering = ["codigo_lengua", "id"]

    def __str__(self):
        return self.get_codigo_idioma_display()

    def get_nombre_completo(self):
        """Retorna el nombre completo del idioma"""
        return self.get_codigo_idioma_display()


# ================================================
# ? 📌 CAMPO 044 - CÓDIGO DEL PAÍS (Subcampo $a R)
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
        ("ar", "Argentina"),
        ("bo", "Bolivia"),
        ("br", "Brasil"),
        ("cl", "Chile"),
        ("co", "Colombia"),
        ("cr", "Costa Rica"),
        ("cu", "Cuba"),
        ("ec", "Ecuador"),
        ("sv", "El Salvador"),
        ("gt", "Guatemala"),
        ("ho", "Honduras"),
        ("mx", "México"),
        ("nq", "Nicaragua"),
        ("pa", "Panamá"),
        ("pe", "Perú"),
        ("pr", "Puerto Rico"),
        ("dr", "República Dominicana"),
        ("uy", "Uruguay"),
        ("ve", "Venezuela"),
    ]

    obra = models.ForeignKey(
        "ObraGeneral",
        on_delete=models.CASCADE,
        related_name="codigos_pais_entidad",
        help_text="Obra a la que pertenece este código de país",
    )

    # Subcampo $a - Código MARC del país (R)
    codigo_pais = models.CharField(
        max_length=2,
        choices=CODIGOS_PAIS,
        default="ec",
        help_text="044 $a – Código ISO 3166-1 alfa-2 del país",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "País Editor/Productor (044 $a)"
        verbose_name_plural = "Países Editor/Productor (044 $a - R)"
        ordering = ["obra", "id"]
        unique_together = [["obra", "codigo_pais"]]

    def __str__(self):
        return self.get_codigo_pais_display()

    def get_nombre_completo(self):
        """Retorna el nombre completo del país"""
        return self.get_codigo_pais_display()

    def get_marc_format(self):
        """Retorna el subcampo en formato MARC"""
        return f"$a{self.codigo_pais}"
