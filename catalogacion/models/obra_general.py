"""
Modelo principal de Obra General MARC21
Versión refactorizada con un solo modelo concreto
Incluye soft-delete, validadores especializados y auditoría
"""

from django.core.exceptions import ValidationError
from django.db import models

from .autoridades import (
    AutoridadFormaMusical,
    AutoridadPersona,
    AutoridadTituloUniforme,
)
from .auxiliares import SoftDeleteMixin
from .constantes import (
    FORMATOS,
    MEDIOS_INTERPRETACION,
    TECNICAS,
    TIPO_OBRA_MAP,
    TONALIDADES,
)
from .managers import ObraGeneralManager
from .utils import (
    actualizar_fecha_hora_transaccion,
    generar_codigo_informacion,
    generar_numero_control,
    generar_signatura_completa,
)
from .validadores import obtener_validador


class NumeroControlSecuencia(models.Model):
    """
    Modelo auxiliar para generar números de control de forma atómica.
    Previene race conditions en entornos concurrentes.
    """

    tipo_registro = models.CharField(
        max_length=1,
        choices=[("c", "Impreso"), ("d", "Manuscrito")],
        unique=True,
        help_text="Tipo de registro para esta secuencia",
    )
    ultimo_numero = models.PositiveIntegerField(
        default=0, help_text="Último número asignado"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Secuencia de Número de Control"
        verbose_name_plural = "Secuencias de Números de Control"

    def __str__(self):
        tipo_nombre = "Manuscrito" if self.tipo_registro == "d" else "Impreso"
        return f"{tipo_nombre}: {self.ultimo_numero}"


class ObraGeneral(SoftDeleteMixin, models.Model):
    """
    Modelo unificado para obras musicales MARC21.
    Maneja todos los tipos mediante validaciones condicionales.
    Incluye soft-delete y auditoría de cambios.
    """

    # ===========================================
    # CAMPOS DE LÍDER Y CONTROL (Leader/00X)
    # ===========================================

    estado_registro = models.CharField(
        max_length=1,
        default="n",
        editable=False,
        help_text="Posición 05: Estado del registro (n=nuevo)",
    )

    tipo_registro = models.CharField(
        max_length=1,
        choices=[("c", "Música impresa"), ("d", "Música manuscrita")],
        default="d",
        help_text="Posición 06: Tipo de registro",
    )

    nivel_bibliografico = models.CharField(
        max_length=1,
        choices=[
            ("a", "Parte componente"),
            ("c", "Colección"),
            ("m", "Obra independiente"),
        ],
        default="m",
        help_text="Posición 07: Nivel bibliográfico",
    )

    num_control = models.CharField(
        max_length=7,
        unique=True,
        editable=False,
        db_index=True,
        help_text="001 - Número de control (formato: M000001 o I000001)",
    )

    fecha_hora_ultima_transaccion = models.CharField(
        max_length=14,
        editable=False,
        help_text="005 - Fecha y hora de última modificación",
    )

    codigo_informacion = models.CharField(
        max_length=40, editable=False, help_text="008 - Información codificada"
    )

    # ===========================================
    # CAMPOS DE IDENTIFICACIÓN (020/024/028)
    # ===========================================

    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="020 $a — ISBN (solo obras impresas)",
    )

    ismn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="024 $a — ISMN (solo obras impresas)",
    )

    tipo_numero_028 = models.CharField(
        max_length=1,
        choices=[
            ("0", "Número de publicación"),
            ("1", "Número de matriz"),
            ("2", "Número de plancha"),
            ("3", "Otro número de música"),
            ("4", "Número de videograbación"),
            ("5", "Otro número de editor"),
        ],
        default="2",
        blank=True,
        null=True,
        help_text="028 Primer indicador — Tipo de número de editor (predeterminado: Número de plancha)",
    )

    control_nota_028 = models.CharField(
        max_length=1,
        choices=[
            ("0", "No hay nota ni punto de acceso adicional"),
            ("1", "Nota, hay punto de acceso adicional"),
            ("2", "Nota, no hay punto de acceso adicional"),
            ("3", "No hay nota, hay punto de acceso adicional"),
        ],
        default="0",
        blank=True,
        null=True,
        help_text="028 Segundo indicador — Control de nota (predeterminado: No hay nota ni punto de acceso adicional)",
    )

    numero_editor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="028 $a — Número de editor, plancha o placa",
    )

    # ===========================================
    # CAMPO 040 - CENTRO CATALOGADOR
    # ===========================================

    centro_catalogador = models.CharField(
        max_length=10, default="UNL", help_text="040 $a — Centro catalogador"
    )

    # ===========================================
    # CAMPOS 100/130/240 - PUNTO DE ACCESO PRINCIPAL
    # ===========================================

    compositor = models.ForeignKey(
        AutoridadPersona,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="obras_como_compositor",
        db_index=True,
        help_text="100 $a y $d — Compositor principal",
    )

    termino_asociado = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="100 $c — Término asociado al nombre",
    )

    autoria = models.CharField(
        max_length=50,
        choices=[
            ("atribuida", "Atribuida"),
            ("certificada", "Certificada"),
            ("erronea", "Errónea"),
        ],
        default="certificada",
        blank=True,
        null=True,
        help_text="100 $j — Autoría del compositor",
    )

    # Campo 130 - Título uniforme principal
    titulo_uniforme = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="obras_130",
        db_index=True,
        help_text="130 $a — Título uniforme normalizado (solo sin compositor)",
    )

    forma_130 = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="obras_forma_130",
        help_text="130 $k — Forma musical",
    )

    medio_interpretacion_130 = models.CharField(
        max_length=200,
        choices=MEDIOS_INTERPRETACION,
        default="piano",
        blank=True,
        null=True,
        help_text="130 $m — Medio de interpretación (predeterminado: piano)",
    )

    numero_parte_130 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="130 $n — Número de parte/sección",
    )

    arreglo_130 = models.CharField(
        max_length=10,
        choices=[("arreglo", "Arreglo")],
        default="arreglo",
        blank=True,
        null=True,
        help_text="130 $o — Arreglo (predeterminado: Arreglo)",
    )

    nombre_parte_130 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="130 $p — Nombre de parte/sección",
    )

    tonalidad_130 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="130 $r — Tonalidad",
    )

    # Campo 240 - Título uniforme secundario (cuando SÍ hay compositor)
    titulo_240 = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="obras_240",
        help_text="240 $a — Título uniforme (solo con compositor)",
    )

    forma_240 = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="obras_forma_240",
        help_text="240 $k — Forma musical",
    )

    medio_interpretacion_240 = models.CharField(
        max_length=200,
        choices=MEDIOS_INTERPRETACION,
        default="piano",
        blank=True,
        null=True,
        help_text="240 $m — Medio de interpretación (predeterminado: piano)",
    )

    numero_parte_240 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="240 $n — Número de parte/sección",
    )

    nombre_parte_240 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="240 $p — Nombre de parte/sección",
    )

    arreglo_240 = models.CharField(
        max_length=10,
        choices=[("arreglo", "Arreglo")],
        default="arreglo",
        blank=True,
        null=True,
        help_text="240 $o — Arreglo (predeterminado: Arreglo)",
    )

    tonalidad_240 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="240 $r — Tonalidad",
    )

    # ===========================================
    # CAMPO 245 - TÍTULO PRINCIPAL
    # ===========================================

    titulo_principal = models.CharField(
        max_length=500, db_index=True, help_text="245 $a — Título principal"
    )

    subtitulo = models.CharField(
        max_length=500, blank=True, null=True, help_text="245 $b — Subtítulo"
    )

    mencion_responsabilidad = models.TextField(
        blank=True, null=True, help_text="245 $c — Nombres en fuente"
    )

    # ===========================================
    # CAMPO 300 - DESCRIPCIÓN FÍSICA
    # ===========================================

    extension = models.CharField(
        max_length=300, blank=True, null=True, help_text="300 $a — Extensión"
    )

    otras_caracteristicas = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $b — Otras características físicas",
    )

    dimension = models.CharField(
        max_length=100, blank=True, null=True, help_text="300 $c — Dimensión"
    )

    material_acompanante = models.CharField(
        max_length=300, blank=True, null=True, help_text="300 $e — Material acompañante"
    )

    # ===========================================
    # CAMPOS 340/348 - CARACTERÍSTICAS TÉCNICAS
    # ===========================================

    ms_imp = models.CharField(
        max_length=200,
        choices=TECNICAS,
        blank=True,
        null=True,
        help_text="340 $d — Técnica",
    )

    formato = models.CharField(
        max_length=100,
        choices=FORMATOS,
        blank=True,
        null=True,
        help_text="348 $a — Formato de la música notada",
    )

    # ===========================================
    # CAMPOS 382/383/384 - MEDIO Y DESIGNACIÓN
    # ===========================================
    # NOTA: El campo 382 (Medio de Interpretación) ahora usa el modelo
    # MedioInterpretacion382 con subcampos $a (medios, repetibles) y
    # $b (solista, no repetible). Ver bloque_3xx.py

    numero_obra = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="383 $a — Número serial de obra musical",
    )

    opus = models.CharField(
        max_length=100, blank=True, null=True, help_text="383 $b — Número de opus"
    )

    tonalidad_384 = models.CharField(
        max_length=20,
        choices=TONALIDADES,
        blank=True,
        null=True,
        help_text="384 $a — Tonalidad",
    )

    # ===========================================
    # CAMPOS 773/774/787 - ENLACES JERÁRQUICOS
    # ===========================================
    # NOTA: Los enlaces jerárquicos ahora usan modelos relacionados
    # con encabezamientos polimórficos (ver bloque_7xx.py)
    # Los campos 773/774/787 se manejan completamente mediante relaciones

    # ===========================================
    # CAMPO 852 - UBICACIÓN
    # ===========================================
    # Los campos 852 ($a, $h, $c) se manejan completamente mediante
    # el modelo Ubicacion852 y sus relaciones (ver bloque_8xx.py)

    # ===========================================
    # METADATOS DEL SISTEMA
    # ===========================================

    fecha_creacion_sistema = models.DateTimeField(auto_now_add=True)
    fecha_modificacion_sistema = models.DateTimeField(auto_now=True)
    
    # Manager personalizado
    objects = ObraGeneralManager()

    # ===========================================
    # META
    # ===========================================

    class Meta:
        verbose_name = "Obra Musical"
        verbose_name_plural = "Obras Musicales"
        db_table = "catalogacion_obra_general"
        ordering = ["-num_control"]
        indexes = [
            models.Index(fields=["num_control"]),
            models.Index(fields=["tipo_registro"]),
            models.Index(fields=["nivel_bibliografico"]),
            models.Index(fields=["tipo_registro", "nivel_bibliografico"]),
            models.Index(fields=["-fecha_creacion_sistema"]),
            models.Index(fields=["titulo_principal"]),
        ]

    # ===========================================
    # PROPIEDADES COMPUTADAS
    # ===========================================

    @property
    def tipo_obra(self):
        """Retorna el tipo de obra basado en tipo_registro y nivel_bibliografico"""
        key = (self.tipo_registro, self.nivel_bibliografico)
        tipo_info = TIPO_OBRA_MAP.get(key)
        return tipo_info[0] if tipo_info else "DESCONOCIDO"

    @property
    def tipo_obra_descripcion(self):
        """Retorna la descripción completa del tipo de obra"""
        key = (self.tipo_registro, self.nivel_bibliografico)
        tipo_info = TIPO_OBRA_MAP.get(key)
        return tipo_info[1] if tipo_info else "Tipo desconocido"

    @property
    def es_manuscrita(self):
        """Retorna True si la obra es manuscrita"""
        return self.tipo_registro == "d"

    @property
    def es_impresa(self):
        """Retorna True si la obra es impresa"""
        return self.tipo_registro == "c"

    @property
    def es_coleccion(self):
        """Retorna True si es una colección"""
        return self.nivel_bibliografico == "c"

    @property
    def es_obra_independiente(self):
        """Retorna True si es obra independiente"""
        return self.nivel_bibliografico == "m"

    @property
    def es_parte_de_coleccion(self):
        """Retorna True si forma parte de una colección"""
        return self.nivel_bibliografico == "a"

    @property
    def signatura_completa(self):
        """Retorna la signatura completa (campo 092)"""
        return generar_signatura_completa(self)

    @property
    def campo_092_marc(self):
        """Retorna el campo 092 en formato MARC"""
        from .utils import obtener_pais_principal

        pais = obtener_pais_principal(self)
        ms_imp = "Ms" if self.tipo_registro == "d" else "Imp"

        return (
            f"092 ## "
            f"$a{self.centro_catalogador} "
            f"$bBLMP "
            f"$c{pais} "
            f"$d{ms_imp} "
            f"$0{self.num_control}"
        )

    # ===========================================
    # PROPIEDADES DE PRESENTACIÓN PÚBLICA
    # ===========================================

    @staticmethod
    def _construir_materia_descripcion(registros):
        """Arma una descripción concatenada de materias con subdivisiones."""
        descripciones = []
        for registro in registros:
            descriptor = str(getattr(registro, "materia", registro))
            subdivisiones = [sub.subdivision for sub in registro.subdivisiones.all()]
            if subdivisiones:
                descriptor = f"{descriptor} -- {' -- '.join(subdivisiones)}"
            descriptor = descriptor.strip()
            if descriptor:
                descripciones.append(descriptor)
        return "; ".join(descripciones)

    def _titulo_uniforme_componentes(
        self, base, forma, medio, numero_parte, nombre_parte, tonalidad, arreglo
    ):
        if not base:
            return ""
        partes = [str(base)]
        if forma:
            partes.append(str(forma))
        if medio:
            partes.append(medio)
        if numero_parte:
            partes.append(numero_parte)
        if nombre_parte:
            partes.append(nombre_parte)
        if tonalidad:
            partes.append(tonalidad)
        if arreglo:
            partes.append(arreglo)
        return ", ".join(partes)

    @property
    def titulo_destacado_display(self):
        """Título prioritario para vistas públicas (240 > 130 > 245)."""
        if self.titulo_240:
            return str(self.titulo_240)
        if self.titulo_uniforme:
            return str(self.titulo_uniforme)
        return self.titulo_245_display

    @property
    def titulo_uniforme_130_display(self):
        medio = (
            self.get_medio_interpretacion_130_display()
            if self.medio_interpretacion_130
            else ""
        )
        tonalidad = self.get_tonalidad_130_display() if self.tonalidad_130 else ""
        return self._titulo_uniforme_componentes(
            self.titulo_uniforme,
            self.forma_130,
            medio,
            self.numero_parte_130,
            self.nombre_parte_130,
            tonalidad,
            self.arreglo_130,
        )

    @property
    def titulo_uniforme_240_display(self):
        medio = (
            self.get_medio_interpretacion_240_display()
            if self.medio_interpretacion_240
            else ""
        )
        tonalidad = self.get_tonalidad_240_display() if self.tonalidad_240 else ""
        return self._titulo_uniforme_componentes(
            self.titulo_240,
            self.forma_240,
            medio,
            self.numero_parte_240,
            self.nombre_parte_240,
            tonalidad,
            self.arreglo_240,
        )

    @property
    def titulo_245_display(self):
        titulo = self.titulo_principal or ""
        if self.subtitulo:
            titulo = f"{titulo} : {self.subtitulo}" if titulo else self.subtitulo
        if self.mencion_responsabilidad:
            separador = " / " if titulo else ""
            titulo = (
                f"{titulo}{separador}{self.mencion_responsabilidad}"
                if titulo
                else self.mencion_responsabilidad
            )
        return titulo.strip() or "Sin título registrado"

    @property
    def autor_publico_principal(self):
        if self.compositor:
            texto = self.compositor.apellidos_nombres
            if self.compositor.coordenadas_biograficas:
                texto = f"{texto} ({self.compositor.coordenadas_biograficas})"
            return texto
        return "[s.n.]"

    @property
    def autor_publico_nota(self):
        return self.get_autoria_display() if self.autoria else ""

    @property
    def publicacion_publica_display(self):
        produccion = next(iter(self.producciones_publicaciones.all()), None)
        if not produccion:
            return "Sin datos de publicación"
        partes = []
        lugares = [l.lugar for l in produccion.lugares.all()]
        entidades = [e.nombre for e in produccion.entidades.all()]
        fechas = [f.fecha for f in produccion.fechas.all()]
        texto = ""
        if lugares:
            texto += ", ".join(filter(None, lugares))
        if entidades:
            texto += (" : " if texto else "") + ", ".join(filter(None, entidades))
        if fechas:
            texto += (", " if texto else "") + ", ".join(filter(None, fechas))
        texto = texto.strip()
        return texto + "." if texto else "Sin datos de publicación"

    @property
    def instrumento_publico_display(self):
        descripciones = []
        for medio in self.medios_interpretacion_382.all():
            instrumentos = [m.get_medio_display() for m in medio.medios.all()]
            descripcion = ", ".join(filter(None, instrumentos))
            if medio.solista:
                descripcion = (
                    f"{descripcion} (Solista: {medio.solista})"
                    if descripcion
                    else f"Solista: {medio.solista}"
                )
            if descripcion:
                descripciones.append(descripcion)
        return (
            "; ".join(descripciones)
            if descripciones
            else "Sin instrumentos registrados"
        )

    @property
    def materia_publica_display(self):
        descripcion = self._construir_materia_descripcion(self.materias_650.all())
        return descripcion or "Sin materias registradas"

    @property
    def temas_publico_display(self):
        descripcion = self._construir_materia_descripcion(self.materias_655.all())
        if descripcion:
            return descripcion
        return self.materia_publica_display

    @property
    def coleccion_publica_display(self):
        colecciones = [
            str(enlace.titulo) for enlace in self.enlaces_documento_fuente_773.all()
        ]
        return "; ".join(colecciones)

    @property
    def tiene_incipit(self):
        return self.incipits_musicales.exists()

    @property
    def primer_incipit_resumen(self):
        incipit = next(iter(self.incipits_musicales.all()), None)
        if not incipit:
            return ""
        partes = [incipit.identificador_completo]
        if incipit.voz_instrumento:
            partes.append(incipit.voz_instrumento)
        return " · ".join(partes)

    @property
    def signatura_publica_display(self):
        from .utils import obtener_pais_principal

        if not self.centro_catalogador or not self.num_control:
            return "Sin signatura"

        pais = obtener_pais_principal(self)
        ms_imp = "Ms" if self.tipo_registro == "d" else "Imp"
        return f"{self.centro_catalogador}. BLMP. {pais}. {ms_imp}.{self.num_control}"

    @property
    def tipo_soporte_publico_display(self):
        return "Manuscrito" if self.tipo_registro == "d" else "Impreso"

    @property
    def tecnica_340_publica_display(self):
        if self.ms_imp:
            return dict(TECNICAS).get(self.ms_imp, self.ms_imp)
        return self.tipo_soporte_publico_display

    @property
    def primer_incipit_detalle(self):
        """Formato detallado para el 031 según especificación."""
        incipit = next(iter(self.incipits_musicales.all()), None)
        if not incipit:
            return "", ""

        def formato(valor):
            return valor if valor else "—"

        firma = incipit.tiempo or incipit.clave or incipit.armadura
        linea_superior = (
            f"{formato(incipit.numero_obra)}."
            f"{formato(incipit.numero_movimiento)}."
            f"{formato(incipit.numero_pasaje)}; "
            f"{formato(incipit.titulo_encabezamiento)}; "
            f"{formato(incipit.voz_instrumento)}; "
            f"{formato(firma)}"
        )

        linea_inferior = formato(incipit.notacion_musical)
        return linea_superior, linea_inferior

    @property
    def descripcion_fisica_publica_display(self):
        texto = self.extension or ""
        if self.otras_caracteristicas:
            texto = (
                f"{texto} : {self.otras_caracteristicas}"
                if texto
                else self.otras_caracteristicas
            )
        if self.dimension:
            texto = f"{texto} ; {self.dimension}" if texto else self.dimension
        if self.material_acompanante:
            texto = (
                f"{texto} + {self.material_acompanante}"
                if texto
                else self.material_acompanante
            )
        return texto or "Sin descripción física"

    @property
    def tonalidad_publica_display(self):
        return self.get_tonalidad_384_display() if self.tonalidad_384 else ""

    @property
    def medios_interpretacion_resumen(self):
        medios = []
        solistas = []
        for registro in self.medios_interpretacion_382.all():
            nombres = ", ".join(
                filter(None, [m.get_medio_display() for m in registro.medios.all()])
            )
            if nombres:
                medios.append(nombres)
            if registro.solista:
                solistas.append(registro.solista)
        medios_texto = "; ".join(medios) if medios else "Sin medios registrados"
        solistas_texto = "; ".join(solistas)
        return medios_texto, solistas_texto

    @property
    def nota_general_resumen(self):
        nota = next(iter(self.notas_generales_500.all()), None)
        if nota and nota.nota_general:
            return nota.nota_general.strip()
        return ""


    # ===========================================
    # MÉTODOS DE PREPARACIÓN
    # ===========================================

    def _preparar_para_creacion(self):
        """Prepara campos automáticos antes de la primera creación"""
        # Generar número de control si no existe
        if not self.num_control:
            self.num_control = generar_numero_control(self.tipo_registro)

        # Generar código de información (008) si no existe
        if not self.codigo_informacion:
            self.codigo_informacion = generar_codigo_informacion()

        # Establecer estado del registro (Leader/05)
        if not self.estado_registro:
            self.estado_registro = "n"

        # Generar fecha/hora de última transacción (005)
        self.fecha_hora_ultima_transaccion = actualizar_fecha_hora_transaccion()

    def generar_leader(self):
        """
        Genera la cabecera MARC21 completa (24 caracteres)
        Formato: |||||[estado][tipo][nivel]||||||||||||4500
        """
        leader = "|" * 5  # Posiciones 00-04 (longitud del registro, calculado después)
        leader += self.estado_registro or "n"  # Posición 05
        leader += self.tipo_registro or "|"  # Posición 06
        leader += self.nivel_bibliografico or "|"  # Posición 07
        leader += "|" * 12  # Posiciones 08-19 (datos técnicos)
        leader += "4500"  # Posiciones 20-23 (constante MARC21)

        return leader

    # ===========================================
    # MÉTODOS DE VALIDACIÓN
    # ===========================================

    def clean(self):
        """Validación de campos y reglas de negocio usando validadores especializados"""
        # Si es creación inicial (no tiene pk), solo validar lo mínimo
        if not self.pk:
            errores = {}

            # Validación de tipo_registro
            if self.tipo_registro not in ("c", "d"):
                errores["tipo_registro"] = "Tipo de registro inválido (use 'c' o 'd')."

            # Validación de nivel_bibliografico
            if self.nivel_bibliografico not in ("a", "c", "m"):
                errores["nivel_bibliografico"] = "Nivel bibliográfico inválido."

            if errores:
                raise ValidationError(errores)
            return

        # Usar validador especializado para edición
        validador = obtener_validador(self)
        validador.validar()

    # ===========================================
    # MÉTODOS DE PERSISTENCIA
    # ===========================================

    def save(self, *args, **kwargs):
        """Guarda la obra con inicialización automática"""
        from .utils import actualizar_fecha_hora_transaccion

        # Solo en creación
        if not self.pk:
            self._preparar_para_creacion()
        else:
            # En actualización, solo actualizar campo 005
            self.fecha_hora_ultima_transaccion = actualizar_fecha_hora_transaccion()

        # Guardar
        super().save(*args, **kwargs)

    # ===========================================
    # MÉTODOS DE REPRESENTACIÓN
    # ===========================================

    def __str__(self):
        compositor = self.compositor
        titulo_uniforme = self.titulo_uniforme

        if compositor:
            return f"{self.num_control or 'Sin N°'}: {self.titulo_principal} - {compositor}"
        if titulo_uniforme:
            return f"{self.num_control or 'Sin N°'}: {titulo_uniforme}"
        return f"{self.num_control or 'Sin N°'}: {self.titulo_principal}"

    def get_absolute_url(self):
        """Retorna la URL canónica de la obra"""
        from django.urls import reverse

        return reverse("catalogacion:detalle_obra", kwargs={"pk": self.pk})

    def campo_005_marc(self):
        """
        Retorna el campo 005 en formato MARC
        Formato: ddmmaaaahhmmss
        """
        return self.fecha_hora_ultima_transaccion

    def campo_008_marc(self):
        """
        Retorna el campo 008 completo (40 posiciones)
        """
        return self.codigo_informacion

    def test_guardado_264(self):
        """
        Función de prueba para verificar si el 264 se guarda correctamente
        """
        print("🧪 TEST DE GUARDADO 264")
        
        # Importar modelos
        from .bloque_2xx import ProduccionPublicacion, Lugar264, NombreEntidad264, Fecha264
        
        # Verificar estado actual
        print(f"📊 Estado actual del 264 para obra {self.pk}:")
        print(f"   ProduccionPublicacion: {ProduccionPublicacion.objects.filter(obra=self).count()}")
        print(f"   Lugar264: {Lugar264.objects.filter(produccion_publicacion__obra=self).count()}")
        print(f"   NombreEntidad264: {NombreEntidad264.objects.filter(produccion_publicacion__obra=self).count()}")
        print(f"   Fecha264: {Fecha264.objects.filter(produccion_publicacion__obra=self).count()}")
        
        # Simular guardado
        print("\n🔧 Simulando guardado del 264...")
        
        # Crear una ProduccionPublicacion de prueba
        try:
            prod = ProduccionPublicacion.objects.create(
                obra=self,
                funcion='0'  # Producción para manuscritos
            )
            print(f"✅ ProduccionPublicacion creada: ID={prod.pk}")
            
            # Crear subcampos de prueba
            lugar = Lugar264.objects.create(
                produccion_publicacion=prod,
                lugar="CIUDAD DE PRUEBA"
            )
            print(f"✅ Lugar264 creado: ID={lugar.pk}")
            
            entidad = NombreEntidad264.objects.create(
                produccion_publicacion=prod,
                nombre="EDITORIAL DE PRUEBA"
            )
            print(f"✅ NombreEntidad264 creado: ID={entidad.pk}")
            
            fecha = Fecha264.objects.create(
                produccion_publicacion=prod,
                fecha="2023"
            )
            print(f"✅ Fecha264 creado: ID={fecha.pk}")
            
            print("\n🎯 VERIFICACIÓN FINAL:")
            print(f"   ProduccionPublicacion: {ProduccionPublicacion.objects.filter(obra=self).count()}")
            print(f"   Lugar264: {Lugar264.objects.filter(produccion_publicacion__obra=self).count()}")
            print(f"   NombreEntidad264: {NombreEntidad264.objects.filter(produccion_publicacion__obra=self).count()}")
            print(f"   Fecha264: {Fecha264.objects.filter(produccion_publicacion__obra=self).count()}")
            
            # Limpiar datos de prueba
            print("\n🧹 Limpiando datos de prueba...")
            fecha.delete()
            entidad.delete()
            lugar.delete()
            prod.delete()
            print("✅ Datos de prueba eliminados")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
            return False

    def test_diagnostico_264(self):
        """
        Función de prueba rápida para diagnosticar el 264 sin afectar el autocompletado
        """
        print("🧪 TEST RÁPIDO - DIAGNÓSTICO 264")
        return self.diagnosticar_guardado_264()

    def diagnosticar_guardado_264(self):
        """
        Diagnóstico específico para verificar si los datos del 264 se guardan correctamente
        """
        print("=" * 80)
        print("🔍 DIAGNÓSTICO DE GUARDADO 264 - VERIFICACIÓN DE BASE DE DATOS")
        print("=" * 80)
        print(f"📋 Obra: {self.titulo_principal} (ID: {self.pk})")
        print()
        
        # Importar modelos necesarios
        try:
            from .bloque_2xx import ProduccionPublicacion, Lugar264, NombreEntidad264, Fecha264
        except ImportError as e:
            print(f"❌ Error importando modelos: {e}")
            return
        
        # 1. Verificar ProduccionPublicacion
        print("🔍 1. PRODUCCIÓN PUBLICACIÓN (264 principal):")
        producciones = ProduccionPublicacion.objects.filter(obra=self)
        print(f"   📊 Total ProduccionPublicacion para esta obra: {producciones.count()}")
        
        if producciones.exists():
            for i, prod in enumerate(producciones, 1):
                print(f"   ✅ Producción {i}: ID={prod.pk}, función='{prod.funcion}'")
                print(f"      📝 Creada: {prod.fecha_creacion}")
                print(f"      📝 Modificada: {prod.fecha_actualizacion if hasattr(prod, 'fecha_actualizacion') else 'N/A'}")
        else:
            print("   ❌ NO HAY ProduccionPublicacion para esta obra")
            print("   🔹 Esto explica por qué el autocompletado del 264 no funciona")
        print()
        
        # 2. Verificar Lugar264
        print("🔍 2. LUGARES (264$a):")
        if producciones.exists():
            for prod in producciones:
                lugares = Lugar264.objects.filter(produccion_publicacion=prod)
                print(f"   📊 Lugares para Producción ID={prod.pk}: {lugares.count()}")
                
                if lugares.exists():
                    for i, lugar in enumerate(lugares, 1):
                        print(f"      ✅ Lugar {i}: ID={lugar.pk}, texto='{lugar.lugar}'")
                        print(f"         📝 Creado: {lugar.fecha_creacion}")
                else:
                    print(f"      ❌ NO hay lugares para esta producción")
        else:
            print("   ❌ No se pueden verificar lugares porque no hay producciones")
        print()
        
        # 3. Verificar NombreEntidad264
        print("🔍 3. ENTIDADES (264$b):")
        if producciones.exists():
            for prod in producciones:
                entidades = NombreEntidad264.objects.filter(produccion_publicacion=prod)
                print(f"   📊 Entidades para Producción ID={prod.pk}: {entidades.count()}")
                
                if entidades.exists():
                    for i, entidad in enumerate(entidades, 1):
                        print(f"      ✅ Entidad {i}: ID={entidad.pk}, nombre='{entidad.nombre}'")
                        print(f"         📝 Creada: {entidad.fecha_creacion}")
                else:
                    print(f"      ❌ NO hay entidades para esta producción")
        else:
            print("   ❌ No se pueden verificar entidades porque no hay producciones")
        print()
        
        # 4. Verificar Fecha264
        print("🔍 4. FECHAS (264$c):")
        if producciones.exists():
            for prod in producciones:
                fechas = Fecha264.objects.filter(produccion_publicacion=prod)
                print(f"   📊 Fechas para Producción ID={prod.pk}: {fechas.count()}")
                
                if fechas.exists():
                    for i, fecha in enumerate(fechas, 1):
                        print(f"      ✅ Fecha {i}: ID={fecha.pk}, texto='{fecha.fecha}'")
                        print(f"         📝 Creada: {fecha.fecha_creacion}")
                else:
                    print(f"      ❌ NO hay fechas para esta producción")
        else:
            print("   ❌ No se pueden verificar fechas porque no hay producciones")
        print()
        
        # 5. Verificación total en toda la BD
        print("🔍 5. VERIFICACIÓN TOTAL EN TODA LA BASE DE DATOS:")
        total_prods = ProduccionPublicacion.objects.all().count()
        total_lugares = Lugar264.objects.all().count()
        total_entidades = NombreEntidad264.objects.all().count()
        total_fechas = Fecha264.objects.all().count()
        
        print(f"   📊 Total ProduccionPublicacion en BD: {total_prods}")
        print(f"   📊 Total Lugar264 en BD: {total_lugares}")
        print(f"   📊 Total NombreEntidad264 en BD: {total_entidades}")
        print(f"   📊 Total Fecha264 en BD: {total_fechas}")
        print()
        
        # 6. Diagnóstico final
        print("🔍 6. DIAGNÓSTICO FINAL:")
        problemas = []
        
        if producciones.count() == 0:
            problemas.append("❌ No hay ProduccionPublicacion - DEBES CREARLA PRIMERO")
        else:
            prod = producciones.first()
            if Lugar264.objects.filter(produccion_publicacion=prod).count() == 0:
                problemas.append("❌ No hay Lugar264 (264$a) - DEBES AGREGAR")
            if NombreEntidad264.objects.filter(produccion_publicacion=prod).count() == 0:
                problemas.append("❌ No hay NombreEntidad264 (264$b) - DEBES AGREGAR")
            if Fecha264.objects.filter(produccion_publicacion=prod).count() == 0:
                problemas.append("❌ No hay Fecha264 (264$c) - DEBES AGREGAR")
        
        if problemas:
            print("   🚨 PROBLEMAS ENCONTRADOS:")
            for problema in problemas:
                print(f"      {problema}")
        else:
            print("   ✅ Todos los datos del 264 están presentes - Debería funcionar")
        
        print("=" * 80)
        return len(problemas) == 0

    def diagnosticar_datos_faltantes_773(self):
        """
        Función de diagnóstico para mostrar qué datos faltan para el autocompletado 773
        """
        print("=" * 80)
        print("🔍 DIAGNÓSTICO COMPLETO DE DATOS FALTANTES PARA AUTOCOMPLETADO 773")
        print("=" * 80)
        print(f"📋 Obra: {self.titulo_principal} (ID: {self.pk})")
        print()
        
        # 264 - Producción/Publicación
        print("🔍 CAMPO 264 - Producción/Publicación:")
        prod_count = self.producciones_publicaciones.count()
        print(f"   📊 Total ProduccionPublicacion: {prod_count}")
        
        if prod_count == 0:
            print("   ❌ NO HAY DATOS - Debes agregar:")
            print("      • 1 ProduccionPublicacion")
            print("      • 1+ Lugar264 (264$a)")
            print("      • 1+ NombreEntidad264 (264$b)")
            print("      • 1+ Fecha264 (264$c)")
        else:
            prod = self.producciones_publicaciones.first()
            print(f"   ✅ ProduccionPublicacion encontrada (ID: {prod.pk})")
            print(f"   📍 Lugares: {prod.lugares.count()}")
            print(f"   🏢 Entidades: {prod.entidades.count()}")
            print(f"   📅 Fechas: {prod.fechas.count()}")
        print()
        
        # 382 - Medium de interpretación
        print("🔍 CAMPO 382 - Medium de interpretación:")
        medios_count = self.medios_interpretacion_382.count()
        print(f"   📊 Total MedioInterpretacion382: {medios_count}")
        
        if medios_count == 0:
            print("   ❌ NO HAY DATOS - Debes agregar:")
            print("      • 1 MedioInterpretacion382")
            print("      • 1+ MedioInterpretacion382_a (382$a)")
            print("      • solista (382$b)")
        else:
            medio = self.medios_interpretacion_382.first()
            print(f"   ✅ MedioInterpretacion382 encontrado (ID: {medio.pk})")
            print(f"   🎵 Medios (382$a): {medio.medios.count()}")
            print(f"   🎤 Solista (382$b): '{medio.solista}'")
            
            if medio.medios.count() == 0:
                print("   ❌ FALTAN LOS MEDIOS (382$a) - Debes agregar MedioInterpretacion382_a")
        print()
        
        # 545 - Datos biográficos
        print("🔍 CAMPO 545 - Datos biográficos:")
        tiene_545 = hasattr(self, 'datos_biograficos_545') and self.datos_biograficos_545
        print(f"   📊 Tiene DatosBiograficos545: {tiene_545}")
        
        if tiene_545:
            nota = self.datos_biograficos_545
            print(f"   ✅ DatosBiograficos545 encontrado (ID: {nota.pk})")
            print(f"   📝 Texto: '{nota.texto_biografico[:50]}...'")
            print(f"   🔗 URI: '{nota.uri}'")
        else:
            print("   ❌ NO HAY DATOS - Debes agregar:")
            print("      • 1 DatosBiograficos545")
            print("      • texto_biografico (545$a)")
            print("      • uri (545$u) - opcional")
        print()
        
        # Resumen
        print("📋 RESUMEN DE ACCIONES NECESARIAS:")
        acciones = []
        
        if prod_count == 0:
            acciones.append("🔹 Agregar ProduccionPublicacion con lugares, entidades y fechas")
        
        if medios_count == 0:
            acciones.append("🔹 Agregar MedioInterpretacion382 con medios y solista")
        elif medios_count > 0 and self.medios_interpretacion_382.first().medios.count() == 0:
            acciones.append("🔹 Agregar MedioInterpretacion382_a al MedioInterpretacion382 existente")
        
        if not tiene_545:
            acciones.append("🔹 Agregar DatosBiograficos545 con texto_biografico")
        
        if acciones:
            for accion in acciones:
                print(f"   {accion}")
        else:
            print("   ✅ Todos los datos están presentes para autocompletado")
        
        print("=" * 80)
        return acciones

    def obtener_campos_para_heredar_773(self):
        """
        Devuelve los campos heredables para el formulario 773 desde la obra padre.
        Solo devuelve los campos reales que existen en el formulario.
        """
        # Llamar al diagnóstico específico del 264 para verificar guardado
        print("🔍 DIAGNÓSTICO ESPECÍFICO 264 - VERIFICANDO GUARDADO EN BD:")
        self.diagnosticar_guardado_264()
        
        # Llamar al diagnóstico general para mostrar qué datos faltan
        self.diagnosticar_datos_faltantes_773()
        
        campos_heredables = {}
        
        print(f"🔍 DEBUG GENERAL: ObraGeneral ID = {self.pk}")
        print(f"🔍 DEBUG GENERAL: Título = {self.titulo_principal}")
        
        # 100 - Autor/Compositor principal (SIEMPRE devolver, aunque sea vacío)
        campos_heredables['100'] = {
            'compositor_id': self.compositor.pk if self.compositor else None,
            'compositor_texto': str(self.compositor) if self.compositor else None,
            'apellidos_nombres': self.compositor.apellidos_nombres if self.compositor else None,
            'coordenadas_biograficas': self.compositor.coordenadas_biograficas if self.compositor else None,
            'funciones': []
        }
        
        # Agregar funciones del compositor (subcampo $e - repetible)
        if self.compositor:
            funciones = self.funciones_compositor.all()
            if funciones.exists():
                campos_heredables['100']['funciones'] = [
                    {
                        'funcion': func.funcion,
                        'funcion_display': func.get_funcion_display()
                    } for func in funciones
                ]
        
        # 245 - Título principal (SOLO los campos reales del formulario)
        campos_heredables['245'] = {
            'titulo_principal': self.titulo_principal or None,
            'subtitulo': self.subtitulo or None,
            'mencion_responsabilidad': self.mencion_responsabilidad or None,
        }
        
        # 264 - Producción/Publicación (SOLO los campos reales del formset)
        print(f"🔍 DEBUG 264: Verificando producciones_publicaciones...")
        prod_264 = self.producciones_publicaciones.first()
        campos_heredables['264'] = {
            'lugar_produccion_264': None,
            'entidad_produccion_264': None,
            'fecha_produccion_264': None
        }
        
        # Debug: verificar si hay datos en la base de datos
        prod_count = self.producciones_publicaciones.count()
        print(f"🔍 DEBUG 264: Total producciones_publicaciones = {prod_count}")
        
        if prod_264:
            # Debug: mostrar qué encontramos
            print(f"🔍 DEBUG 264: prod_264 encontrado = {prod_264} (ID: {prod_264.pk})")
            
            # Lugar (264$a) - ACCESO DIRECTO
            try:
                lugares_count = prod_264.lugares.count()
                print(f"🔍 DEBUG 264: Total lugares = {lugares_count}")
                lugar_264 = prod_264.lugares.first()
                if lugar_264:
                    campos_heredables['264']['lugar_produccion_264'] = lugar_264.lugar
                    print(f"🔍 DEBUG 264: lugar encontrado = {lugar_264.lugar} (ID: {lugar_264.pk})")
                else:
                    print("🔍 DEBUG 264: No hay lugares (first() returned None)")
            except Exception as e:
                print(f"🔍 DEBUG 264: Error accediendo a lugares = {e}")
            
            # Entidad (264$b) - ACCESO DIRECTO
            try:
                entidades_count = prod_264.entidades.count()
                print(f"🔍 DEBUG 264: Total entidades = {entidades_count}")
                entidad_264 = prod_264.entidades.first()
                if entidad_264:
                    campos_heredables['264']['entidad_produccion_264'] = entidad_264.nombre
                    print(f"🔍 DEBUG 264: entidad encontrada = {entidad_264.nombre} (ID: {entidad_264.pk})")
                else:
                    print("🔍 DEBUG 264: No hay entidades (first() returned None)")
            except Exception as e:
                print(f"🔍 DEBUG 264: Error accediendo a entidades = {e}")
            
            # Fecha (264$c) - ACCESO DIRECTO
            try:
                fechas_count = prod_264.fechas.count()
                print(f"🔍 DEBUG 264: Total fechas = {fechas_count}")
                fecha_264 = prod_264.fechas.first()
                if fecha_264:
                    campos_heredables['264']['fecha_produccion_264'] = fecha_264.fecha
                    print(f"🔍 DEBUG 264: fecha encontrada = {fecha_264.fecha} (ID: {fecha_264.pk})")
                else:
                    print("🔍 DEBUG 264: No hay fechas (first() returned None)")
            except Exception as e:
                print(f"🔍 DEBUG 264: Error accediendo a fechas = {e}")
        else:
            print("🔍 DEBUG 264: No hay producciones_publicaciones")
            
            # Verificación adicional: si hay producciones en la base de datos
            try:
                from .bloque_2xx import ProduccionPublicacion
                total_prods = ProduccionPublicacion.objects.filter(obra=self).count()
                print(f"🔍 DEBUG 264: Verificación directa - Total ProduccionPublicacion para esta obra = {total_prods}")
                
                if total_prods > 0:
                    prod_direct = ProduccionPublicacion.objects.filter(obra=self).first()
                    print(f"🔍 DEBUG 264: ProduccionPublicacion directa encontrada = {prod_direct} (ID: {prod_direct.pk})")
                    print(f"🔍 DEBUG 264: Lugares directos = {prod_direct.lugares.count()}")
                    print(f"🔍 DEBUG 264: Entidades directas = {prod_direct.entidades.count()}")
                    print(f"🔍 DEBUG 264: Fechas directas = {prod_direct.fechas.count()}")
            except Exception as e:
                print(f"🔍 DEBUG 264: Error en verificación directa = {e}")
        
        # 382 - Medium de interpretación (SOLO los campos reales del formset)
        print(f"🔍 DEBUG 382: Verificando medios_interpretacion_382...")
        medios_382 = self.medios_interpretacion_382.all()
        campos_heredables['382'] = {
            'solista': None,
            'medio_interpretacion_382': None,
            'medio_display': None
        }
        
        # Debug: verificar si hay datos en la base de datos
        print(f"🔍 DEBUG 382: Total medios_interpretacion_382 = {medios_382.count()}")
        
        if medios_382.exists():
            primer_medio = medios_382.first()
            print(f"🔍 DEBUG 382: primer_medio encontrado = {primer_medio} (ID: {primer_medio.pk})")
            
            # Solista (382$b) - ACCESO DIRECTO
            try:
                campos_heredables['382']['solista'] = primer_medio.solista
                print(f"🔍 DEBUG 382: solista = {primer_medio.solista}")
            except Exception as e:
                print(f"🔍 DEBUG 382: Error accediendo a solista = {e}")
            
            # Medio (382$a) - ACCESO DIRECTO
            try:
                primer_subcampo = primer_medio.medios.first()
                if primer_subcampo:
                    campos_heredables['382']['medio_interpretacion_382'] = primer_subcampo.medio
                    campos_heredables['382']['medio_display'] = str(primer_subcampo)
                    print(f"🔍 DEBUG 382: medio encontrado = {primer_subcampo.medio} (ID: {primer_subcampo.pk})")
                    print(f"🔍 DEBUG 382: medio display = {str(primer_subcampo)}")
                else:
                    print("🔍 DEBUG 382: No hay subcampos_a (medios) - first() returned None")
            except Exception as e:
                print(f"🔍 DEBUG 382: Error accediendo a medios = {e}")
        else:
            print("🔍 DEBUG 382: No hay medios_interpretacion_382")
        
        # 545 - Nota biográfica/histórica (campo simple)
        print(f"🔍 DEBUG 545: Verificando datos_biograficos_545...")
        nota_545 = getattr(self, 'datos_biograficos_545', None)
        campos_heredables['545'] = {
            'datos_biograficos_545': None,
            'uri_545': None
        }
        
        # Debug: verificar si hay datos en la base de datos
        print(f"🔍 DEBUG 545: hasattr(self, 'datos_biograficos_545') = {hasattr(self, 'datos_biograficos_545')}")
        
        if nota_545:
            try:
                campos_heredables['545']['datos_biograficos_545'] = nota_545.texto_biografico
                campos_heredables['545']['uri_545'] = nota_545.uri
                print(f"🔍 DEBUG 545: nota biográfica encontrada = {nota_545.texto_biografico[:100]}... (ID: {nota_545.pk})")
                print(f"🔍 DEBUG 545: URI encontrada = {nota_545.uri} (ID: {nota_545.pk})")
            except Exception as e:
                print(f"🔍 DEBUG 545: Error accediendo a texto_biografico = {e}")
        else:
            print("🔍 DEBUG 545: No hay datos_biograficos_545")
            # Intentar verificar si hay alguna instancia en la base de datos
            try:
                from .bloque_5xx import DatosBiograficos545
                existe = DatosBiograficos545.objects.filter(obra=self).exists()
                print(f"🔍 DEBUG 545: ¿Existe DatosBiograficos545 para esta obra? = {existe}")
                if existe:
                    db_545 = DatosBiograficos545.objects.get(obra=self)
                    print(f"🔍 DEBUG 545: Datos en BD = {db_545.texto_biografico[:100] if db_545.texto_biografico else 'None'}...")
                    print(f"🔍 DEBUG 545: URI en BD = {db_545.uri}")
            except Exception as e:
                print(f"🔍 DEBUG 545: Error verificando BD = {e}")
        
        # 852 - Localización (SOLO los campos reales del formset)
        ubicacion_852 = self.ubicaciones_852.first()
        campos_heredables['852'] = {
            'codigo_o_nombre': None,
            'signatura_original': None,
            'estanteria': None
        }
        
        if ubicacion_852:
            print(f"🔍 DEBUG 852: ubicación encontrada = {ubicacion_852}")
            
            # 852 $a - Institución/Persona
            campos_heredables['852']['codigo_o_nombre'] = ubicacion_852.codigo_o_nombre
            print(f"🔍 DEBUG 852: código_o_nombre = {ubicacion_852.codigo_o_nombre}")
            
            # 852 $h - Signatura original
            campos_heredables['852']['signatura_original'] = ubicacion_852.signatura_original
            print(f"🔍 DEBUG 852: signatura_original = {ubicacion_852.signatura_original}")
            
            # 852 $c - Estantería (si existe)
            if ubicacion_852.estanterias.exists():
                estanteria = ubicacion_852.estanterias.first()
                campos_heredables['852']['estanteria'] = estanteria.estanteria
                print(f"🔍 DEBUG 852: estantería encontrada = {estanteria.estanteria}")
            else:
                print("🔍 DEBUG 852: No hay estanterías")
        else:
            print("🔍 DEBUG 852: No hay ubicaciones_852")
        
        # 856 - Acceso electrónico (SOLO los campos reales del formset)
        enlaces_856 = self.disponibles_856.all()
        campos_heredables['856'] = {
            'url_disponible_856': None,
            'texto_disponible_856': None
        }
        
        if enlaces_856.exists():
            primer_enlace = enlaces_856.first()
            print(f"🔍 DEBUG 856: primer_enlace encontrado = {primer_enlace}")
            
            # 856 $u - URL (primera que encuentre)
            urls = primer_enlace.urls_856.all()
            if urls.exists():
                primera_url = urls.first()
                campos_heredables['856']['url_disponible_856'] = primera_url.url
                print(f"🔍 DEBUG 856: URL encontrada = {primera_url.url}")
            else:
                print("🔍 DEBUG 856: No hay URLs")
            
            # 856 $y - Texto del enlace (primero que encuentre)
            textos = primer_enlace.textos_enlace_856.all()
            if textos.exists():
                primer_texto = textos.first()
                campos_heredables['856']['texto_disponible_856'] = primer_texto.texto_enlace
                print(f"🔍 DEBUG 856: Texto encontrado = {primer_texto.texto_enlace}")
            else:
                print("🔍 DEBUG 856: No hay textos de enlace")
        else:
            print("🔍 DEBUG 856: No hay disponibles_856")
        
        print(f"🔍 DEBUG FINAL: campos_heredables = {campos_heredables}")
        return campos_heredables
