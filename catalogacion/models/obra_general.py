"""
Modelo principal de Obra General MARC21
Versión refactorizada con un solo modelo concreto
Incluye soft-delete, validadores especializados y auditoría
"""
from django.db import models
from django.core.exceptions import ValidationError

from .autoridades import (
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadEntidad,
)
from .constantes import TONALIDADES, TECNICAS, FORMATOS, MEDIOS_INTERPRETACION, TIPO_OBRA_MAP
from .managers import ObraGeneralManager
from .utils import (
    actualizar_fecha_hora_transaccion,
    generar_numero_control,
    generar_codigo_informacion,
    generar_signatura_completa,
)
from .auxiliares import SoftDeleteMixin
from .validadores import obtener_validador


class NumeroControlSecuencia(models.Model):
    """
    Modelo auxiliar para generar números de control de forma atómica.
    Previene race conditions en entornos concurrentes.
    """
    tipo_registro = models.CharField(
        max_length=1,
        choices=[('c', 'Impreso'), ('d', 'Manuscrito')],
        unique=True,
        help_text="Tipo de registro para esta secuencia"
    )
    ultimo_numero = models.PositiveIntegerField(
        default=0,
        help_text="Último número asignado"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Secuencia de Número de Control"
        verbose_name_plural = "Secuencias de Números de Control"

    def __str__(self):
        tipo_nombre = "Manuscrito" if self.tipo_registro == 'd' else "Impreso"
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
        default='n',
        editable=False,
        help_text="Posición 05: Estado del registro (n=nuevo)"
    )
    
    tipo_registro = models.CharField(
        max_length=1,
        choices=[('c', 'Música impresa'), ('d', 'Música manuscrita')],
        default='d',
        help_text="Posición 06: Tipo de registro"
    )
    
    nivel_bibliografico = models.CharField(
        max_length=1,
        choices=[
            ('a', 'Parte componente'),
            ('c', 'Colección'),
            ('m', 'Obra independiente')
        ],
        default='m',
        help_text="Posición 07: Nivel bibliográfico"
    )

    num_control = models.CharField(
        max_length=7,
        unique=True,
        editable=False,
        db_index=True,
        help_text="001 - Número de control (formato: M000001 o I000001)"
    )
    
    fecha_hora_ultima_transaccion = models.CharField(
        max_length=14,
        editable=False,
        help_text="005 - Fecha y hora de última modificación"
    )
    
    codigo_informacion = models.CharField(
        max_length=40,
        editable=False,
        help_text="008 - Información codificada"
    )

    # ===========================================
    # CAMPOS DE IDENTIFICACIÓN (020/024/028)
    # ===========================================
    
    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="020 $a — ISBN (solo obras impresas)"
    )
    
    ismn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="024 $a — ISMN (solo obras impresas)"
    )
    
    tipo_numero_028 = models.CharField(
        max_length=1,
        choices=[
            ('0', 'Número de publicación'),
            ('1', 'Número de matriz'),
            ('2', 'Número de plancha'),
            ('3', 'Otro número de música'),
            ('4', 'Número de videograbación'),
            ('5', 'Otro número de editor'),
        ],
        default='2',
        blank=True,
        null=True,
        help_text="028 Primer indicador — Tipo de número de editor (predeterminado: Número de plancha)"
    )
    
    control_nota_028 = models.CharField(
        max_length=1,
        choices=[
            ('0', 'No hay nota ni punto de acceso adicional'),
            ('1', 'Nota, hay punto de acceso adicional'),
            ('2', 'Nota, no hay punto de acceso adicional'),
            ('3', 'No hay nota, hay punto de acceso adicional'),
        ],
        default='0',
        blank=True,
        null=True,
        help_text="028 Segundo indicador — Control de nota (predeterminado: No hay nota ni punto de acceso adicional)"
    )
    
    numero_editor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="028 $a — Número de editor, plancha o placa"
    )
    

    # ===========================================
    # CAMPO 040 - CENTRO CATALOGADOR
    # ===========================================
    
    centro_catalogador = models.CharField(
        max_length=10,
        default='UNL',
        help_text="040 $a — Centro catalogador"
    )

    # ===========================================
    # CAMPOS 100/130/240 - PUNTO DE ACCESO PRINCIPAL
    # ===========================================
    
    compositor = models.ForeignKey(
        AutoridadPersona,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_como_compositor',
        db_index=True,
        help_text="100 $a y $d — Compositor principal"
    )
    
    termino_asociado = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="100 $c — Término asociado al nombre"
    )
    
    autoria = models.CharField(
        max_length=50,
        choices=[
            ('atribuida', 'Atribuida'),
            ('certificada', 'Certificada'),
            ('erronea', 'Errónea'),
        ],
        default='certificada',
        blank=True,
        null=True,
        help_text="100 $j — Autoría del compositor"
    )

    # Campo 130 - Título uniforme principal 
    titulo_uniforme = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_130',
        db_index=True,
        help_text="130 $a — Título uniforme normalizado (solo sin compositor)"
    )
    
    forma_130 = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_forma_130',
        help_text="130 $k — Forma musical"
    )
    
    medio_interpretacion_130 = models.CharField(
        max_length=200,
        choices=MEDIOS_INTERPRETACION,
        default='piano',
        blank=True,
        null=True,
        help_text="130 $m — Medio de interpretación (predeterminado: piano)"
    )
    
    numero_parte_130 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="130 $n — Número de parte/sección"
    )
    
    arreglo_130 = models.CharField(
        max_length=10,
        choices=[("arreglo", "Arreglo")],
        default='arreglo',
        blank=True,
        null=True,
        help_text="130 $o — Arreglo (predeterminado: Arreglo)"
    )
    
    nombre_parte_130 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="130 $p — Nombre de parte/sección"
    )
    
    tonalidad_130 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="130 $r — Tonalidad"
    )

    # Campo 240 - Título uniforme secundario (cuando SÍ hay compositor)
    titulo_240 = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_240',
        help_text="240 $a — Título uniforme (solo con compositor)"
    )
    
    forma_240 = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_forma_240',
        help_text="240 $k — Forma musical"
    )
    
    medio_interpretacion_240 = models.CharField(
        max_length=200,
        choices=MEDIOS_INTERPRETACION,
        default='piano',
        blank=True,
        null=True,
        help_text="240 $m — Medio de interpretación (predeterminado: piano)"
    )
    
    numero_parte_240 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="240 $n — Número de parte/sección"
    )
    
    nombre_parte_240 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="240 $p — Nombre de parte/sección"
    )
    
    arreglo_240 = models.CharField(
        max_length=10,
        choices=[("arreglo", "Arreglo")],
        default='arreglo',
        blank=True,
        null=True,
        help_text="240 $o — Arreglo (predeterminado: Arreglo)"
    )
    
    tonalidad_240 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="240 $r — Tonalidad"
    )

    # ===========================================
    # CAMPO 245 - TÍTULO PRINCIPAL
    # ===========================================
    
    titulo_principal = models.CharField(
        max_length=500,
        db_index=True,
        help_text="245 $a — Título principal"
    )
    
    subtitulo = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="245 $b — Subtítulo"
    )
    
    mencion_responsabilidad = models.TextField(
        blank=True,
        null=True,
        help_text="245 $c — Nombres en fuente"
    )

    # ===========================================
    # CAMPO 300 - DESCRIPCIÓN FÍSICA
    # ===========================================
    
    extension = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $a — Extensión"
    )
    
    otras_caracteristicas = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $b — Otras características físicas"
    )
    
    dimension = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="300 $c — Dimensión"
    )
    
    material_acompanante = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $e — Material acompañante"
    )

    # ===========================================
    # CAMPOS 340/348 - CARACTERÍSTICAS TÉCNICAS
    # ===========================================
    
    ms_imp = models.CharField(
        max_length=200,
        choices=TECNICAS,
        blank=True,
        null=True,
        help_text="340 $d — Técnica"
    )
    
    formato = models.CharField(
        max_length=100,
        choices=FORMATOS,
        blank=True,
        null=True,
        help_text="348 $a — Formato de la música notada"
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
        help_text="383 $a — Número serial de obra musical"
    )
    
    opus = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="383 $b — Número de opus"
    )
    
    tonalidad_384 = models.CharField(
        max_length=20,
        choices=TONALIDADES,
        blank=True,
        null=True,
        help_text="384 $a — Tonalidad"
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
        ordering = ['-num_control']
        indexes = [
            models.Index(fields=['num_control']),
            models.Index(fields=['tipo_registro']),
            models.Index(fields=['nivel_bibliografico']),
            models.Index(fields=['tipo_registro', 'nivel_bibliografico']),
            models.Index(fields=['-fecha_creacion_sistema']),
            models.Index(fields=['titulo_principal']),
        ]

    # ===========================================
    # PROPIEDADES COMPUTADAS
    # ===========================================
    
    @property
    def tipo_obra(self):
        """Retorna el tipo de obra basado en tipo_registro y nivel_bibliografico"""
        key = (self.tipo_registro, self.nivel_bibliografico)
        tipo_info = TIPO_OBRA_MAP.get(key)
        return tipo_info[0] if tipo_info else 'DESCONOCIDO'
    
    @property
    def tipo_obra_descripcion(self):
        """Retorna la descripción completa del tipo de obra"""
        key = (self.tipo_registro, self.nivel_bibliografico)
        tipo_info = TIPO_OBRA_MAP.get(key)
        return tipo_info[1] if tipo_info else 'Tipo desconocido'
    
    @property
    def es_manuscrita(self):
        """Retorna True si la obra es manuscrita"""
        return self.tipo_registro == 'd'
    
    @property
    def es_impresa(self):
        """Retorna True si la obra es impresa"""
        return self.tipo_registro == 'c'
    
    @property
    def es_coleccion(self):
        """Retorna True si es una colección"""
        return self.nivel_bibliografico == 'c'
    
    @property
    def es_obra_independiente(self):
        """Retorna True si es obra independiente"""
        return self.nivel_bibliografico == 'm'
    
    @property
    def es_parte_de_coleccion(self):
        """Retorna True si forma parte de una colección"""
        return self.nivel_bibliografico == 'a'
    
    @property
    def signatura_completa(self):
        """Retorna la signatura completa (campo 092)"""
        return generar_signatura_completa(self)
    
    @property
    def campo_092_marc(self):
        """Retorna el campo 092 en formato MARC"""
        from .utils import obtener_pais_principal
        pais = obtener_pais_principal(self)
        ms_imp = 'Ms' if self.tipo_registro == 'd' else 'Imp'
        
        return (
            f"092 ## "
            f"$a{self.centro_catalogador} "
            f"$bBLMP "
            f"$c{pais} "
            f"$d{ms_imp} "
            f"$0{self.num_control}"
        )

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
            self.estado_registro = 'n'
        
        # Generar fecha/hora de última transacción (005)
        self.fecha_hora_ultima_transaccion = actualizar_fecha_hora_transaccion()
            
    def generar_leader(self):
        """
        Genera la cabecera MARC21 completa (24 caracteres)
        Formato: |||||[estado][tipo][nivel]||||||||||||4500
        """
        leader = '|' * 5  # Posiciones 00-04 (longitud del registro, calculado después)
        leader += self.estado_registro or 'n'  # Posición 05
        leader += self.tipo_registro or '|'    # Posición 06
        leader += self.nivel_bibliografico or '|'  # Posición 07
        leader += '|' * 12  # Posiciones 08-19 (datos técnicos)
        leader += '4500'    # Posiciones 20-23 (constante MARC21)
        
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
            if self.tipo_registro not in ('c', 'd'):
                errores['tipo_registro'] = "Tipo de registro inválido (use 'c' o 'd')."
            
            # Validación de nivel_bibliografico
            if self.nivel_bibliografico not in ('a', 'c', 'm'):
                errores['nivel_bibliografico'] = "Nivel bibliográfico inválido."
            
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
        return reverse('catalogacion:detalle_obra', kwargs={'pk': self.pk})
    
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
    
    def exportar_marc21_control(self):
        """
        Exporta la cabecera y campos de control en formato MARC21
        """
        return {
            'Leader': self.generar_leader(),
            '001': self.num_control,
            '005': self.campo_005_marc(),
            '008': self.campo_008_marc(),
        }