from django.db import models
from datetime import datetime
from .models_repetibles import TituloAlternativo, Edicion, ProduccionPublicacion, DescripcionFisica

# Exportar todos los modelos para que estén disponibles con "from .models import ..."
__all__ = [
    # Autoridades
    'AutoridadPersona',
    'AutoridadTituloUniforme',
    'AutoridadFormaMusical',
    'AutoridadMateria',
    # Modelos repetibles (importados desde models_repetibles.py)
    'TituloAlternativo',
    'Edicion',
    'ProduccionPublicacion',
    'DescripcionFisica',
    # Modelo principal
    'ObraGeneral',
]

# ================================================
# 📚 TABLAS DE AUTORIDADES (Vocabularios Controlados)
# ================================================

class AutoridadPersona(models.Model):
    """
    Base de datos de autoridades para nombres de personas.
    Se usa en: Campo 100 (compositor), Campo 600 (materia-persona), 
    Campo 700 (colaborador), Campo 773/774/787 (enlaces)
    """
    apellidos_nombres = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Formato: Apellidos, Nombres (normalizado)"
    )
    fechas = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Coordenadas biográficas: año nacimiento - año muerte"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Persona"
        verbose_name_plural = "Autoridades - Personas"
        ordering = ['apellidos_nombres']
    
    def __str__(self):
        if self.fechas:
            return f"{self.apellidos_nombres} {self.fechas}"
        return self.apellidos_nombres


class AutoridadTituloUniforme(models.Model):
    """
    Base de datos de autoridades para títulos uniformes.
    Se usa en: Campo 130 (título principal), Campo 240 (título con compositor)
    """
    titulo = models.CharField(
        max_length=300, 
        unique=True,
        help_text="Título uniforme normalizado"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Título Uniforme"
        verbose_name_plural = "Autoridades - Títulos Uniformes"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo


class AutoridadFormaMusical(models.Model):
    """
    Base de datos de autoridades para formas musicales.
    Se usa en: Campo 130 $k, Campo 240 $k, Campo 655 (género/forma)
    """
    forma = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Forma o género musical (ej: Pasillo, Sinfonía, Vals)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Forma Musical"
        verbose_name_plural = "Autoridades - Formas Musicales"
        ordering = ['forma']
    
    def __str__(self):
        return self.forma


class AutoridadMateria(models.Model):
    """
    Base de datos de autoridades para términos de materia.
    Se usa en: Campo 650 (materia general)
    """
    termino = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Término de materia normalizado"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Autoridad - Materia"
        verbose_name_plural = "Autoridades - Materias"
        ordering = ['termino']
    
    def __str__(self):
        return self.termino


# ================================================
# 🎵 CONSTANTES Y OPCIONES
# ================================================

TONALIDADES = [
    ('Do mayor', 'Do mayor'),
    ('Do menor', 'Do menor'),
    ('Do# mayor', 'Do# mayor'),
    ('Do# menor', 'Do# menor'),
    ('Reb mayor', 'Reb mayor'),
    ('Reb menor', 'Reb menor'),
    ('Re mayor', 'Re mayor'),
    ('Re menor', 'Re menor'),
    ('Mib mayor', 'Mib mayor'),
    ('Mib menor', 'Mib menor'),
    ('Mi mayor', 'Mi mayor'),
    ('Mi menor', 'Mi menor'),
    ('Fa mayor', 'Fa mayor'),
    ('Fa menor', 'Fa menor'),
    ('Fa# mayor', 'Fa# mayor'),
    ('Fa# menor', 'Fa# menor'),
    ('Sol mayor', 'Sol mayor'),
    ('Sol menor', 'Sol menor'),
    ('Sol# mayor', 'Sol# mayor'),
    ('Sol# menor', 'Sol# menor'),
    ('Lab mayor', 'Lab mayor'),
    ('Lab menor', 'Lab menor'),
    ('La mayor', 'La mayor'),
    ('La menor', 'La menor'),
    ('Sib mayor', 'Sib mayor'),
    ('Sib menor', 'Sib menor'),
    ('Si mayor', 'Si mayor'),
    ('Si menor', 'Si menor'),
]

FUNCIONES_PERSONA = [
    ('arreglista', 'Arreglista'),
    ('compositor', 'Compositor'),
    # ('coeditor', 'Coeditor'),
    # ('compilador', 'Compilador'),
    # ('copista', 'Copista'),
    # ('dedicatario', 'Dedicatario'),
    # ('editor', 'Editor'),
    # ('letrista', 'Letrista'),
    # ('prologuista', 'Prologuista'),
]

CALIFICADORES_AUTORIA = [
    ('atribuida', 'Atribuida'),
    ('certificada', 'Certificada'),
    # ('dudosa', 'Dudosa'),
    # ('erronea', 'Errónea'),
]

# ================================================
# 📄 MODELO PRINCIPAL - OBRA GENERAL
# ================================================

class ObraGeneral(models.Model):
    """
    Modelo principal que representa un registro bibliográfico MARC 21
    para música manuscrita o impresa
    """
    
    # ------------------------------------------------
    # 🟩 CABECERA O LÍDER
    # ------------------------------------------------
    estado_registro = models.CharField(
        max_length=1, 
        default='n', 
        editable=False,
        help_text="Posición 05: Estado del registro (n=nuevo)"
    )
    
    tipo_registro = models.CharField(
        max_length=1,
        choices=[
            ('c', 'Música impresa'), 
            ('d', 'Música manuscrita')
        ],
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
    
    # ------------------------------------------------
    # 🟨 CAMPOS FIJOS MARC21
    # ------------------------------------------------
    num_control = models.CharField(
        max_length=6, 
        unique=True, 
        editable=False,
        help_text="001 - Número de control (6 dígitos)"
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
    
    # ------------------------------------------------
    # ?🟦 BLOQUE 0XX – Campos de longitud variable
    # ------------------------------------------------

    #* Campo 020 implementado como modelo separado: ISBN
    #* Campo 024 implementado como modelo separado: ISMN    
    #* Campo 028 implementado como modelo separado: NumeroEditor
    #* Campo 031 implementado como modelo separado: IncipitMusical
    
    # 040 ## Fuente de catalogación
    centro_catalogador = models.CharField(
        max_length=10, 
        default='UNL',
        help_text="040 $a – Centro catalogador (predeterminado: UNL)"
    )
    
    # 041 0# Código de lengua
    codigo_lengua = models.CharField(
        max_length=3, 
        default='spa',
        choices=[
            ('spa', 'Español'),
            ('eng', 'Inglés'),
            ('fra', 'Francés'),
            ('ger', 'Alemán'),
            ('ita', 'Italiano'),
            ('lat', 'Latín'),
            ('por', 'Portugués'),
            ('que', 'Quechua'),
        ],
        help_text="041 $a – Código de lengua MARC21 (predeterminado: spa)"
    )
    
    # 044 ## Código del país
    codigo_pais = models.CharField(
        max_length=3, 
        default='ec',
        choices=[
            ('ec', 'Ecuador'),
            ('us', 'Estados Unidos'),
            ('es', 'España'),
            ('fr', 'Francia'),
            ('it', 'Italia'),
            ('de', 'Alemania'),
            ('ar', 'Argentina'),
            ('co', 'Colombia'),
            ('pe', 'Perú'),
        ],
        help_text="044 $a – Código del país (predeterminado: ec)"
    )
    
    # 092 ## Clasificación local
    clasif_institucion = models.CharField(
        max_length=50, 
        default='UNL', 
        help_text="092 $a – Institución (UNL)"
    )
    clasif_proyecto = models.CharField(
        max_length=50, 
        default='BLMP', 
        help_text="092 $b – Proyecto (BLMP)"
    )
    clasif_pais = models.CharField(
        max_length=50, 
        default='EC', 
        help_text="092 $c – País (EC)"
    )
    clasif_ms_imp = models.CharField(
        max_length=3,
        choices=[('Ms', 'Manuscrito'), ('Imp', 'Impreso')],
        default='Ms',
        help_text="092 $d – Tipo de material (Ms/Imp)"
    )
    clasif_num_control = models.CharField(
        max_length=6, 
        editable=False, 
        help_text="092 $0 – Duplica 001"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 1XX – Asientos principales
    # ------------------------------------------------
    
    # 100 1# Compositor (NR - No Repetible)
    # ⚠️ USA la tabla de autoridades
    compositor = models.ForeignKey(
        AutoridadPersona,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_como_compositor',
        help_text="100 $a y $d – Compositor principal (cruzar con 600, 700)"
    )
    
    # TODO: Repetible
    compositor_funcion = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        choices=FUNCIONES_PERSONA,
        default='compositor',
        help_text="100 $e – Función (predeterminado: compositor)"
    )
    
    # TODO: Repetible
    compositor_autoria = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        choices=CALIFICADORES_AUTORIA,
        default='certificada',
        help_text="100 $j – Calificador de atribución"
    )
    
    # 130 0# Título uniforme como punto de acceso principal (NR)
    titulo_uniforme = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_130',
        help_text="130 $a – Título uniforme (cruzar con 240)"
    )
    
    # TODO: Repetible
    titulo_uniforme_forma = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_130_forma',
        help_text="130 $k – Forma (cruzar con 240 $k y 655)"
    )
    
    # TODO: Repetible
    titulo_uniforme_medio_interpretacion = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        default='piano',
        help_text="130 $m – Medio de interpretación"
    )
    
    titulo_uniforme_num_parte = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="130 $n – Número de parte/sección"
    )
    
    titulo_uniforme_arreglo = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        default='arreglo',
        help_text="130 $o – Arreglo"
    )
    
    # TODO: Repetible
    titulo_uniforme_nombre_parte = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="130 $p – Nombre de parte/sección"
    )
    
    titulo_uniforme_tonalidad = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        choices=TONALIDADES,
        help_text="130 $r – Tonalidad"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 2XX – Títulos y mención de responsabilidad
    # ------------------------------------------------
    
    # ⚠️ Usa LA MISMA tabla de autoridades que 130
    titulo_240 = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_240',
        help_text="240 $a – Título uniforme (cruzar con 130)"
    )
    
    # TODO: Repetible
    titulo_240_forma = models.ForeignKey(
        AutoridadFormaMusical,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_240_forma',
        help_text="240 $k – Forma (cruzar con 130 $k y 655)"
    )
    
    # TODO: Repetible
    titulo_240_medio_interpretacion = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="240 $m – Medio de interpretación"
    )
    
    # TODO: Repetible
    titulo_240_num_parte = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="240 $n – Número de parte/sección"
    )
    
    titulo_240_arreglo = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="240 $o – Arreglo"
    )
    
    # TODO: Repetible
    titulo_240_nombre_parte = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="240 $p – Nombre de parte/sección"
    )
    
    titulo_240_tonalidad = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        choices=TONALIDADES,
        help_text="240 $r – Tonalidad"
    )
    
    # 245 10 Mención de título (NR)
    titulo_principal = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="245 $a – Título principal"
    )
    
    subtitulo = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="245 $b – Subtítulo"
    )
    
    mencion_responsabilidad = models.TextField(
        blank=True, 
        null=True,
        help_text="245 $c – Mención de responsabilidad"
    )
    
    #* Campo 246 implementado como modelo separado: TituloAlternativo

    #* Campo 250 implementado como modelo separado: Edicion
    
    #* Campo 264 implementado como modelo separado: ProduccionPublicacion
    # ------------------------------------------------


    #? 🟦 BLOQUE 3XX – Descripción física

    #* Campo 300 implementado como modelo separado: DescripcionFisica

    
    # ------------------------------------------------
    # Metadatos del sistema
    # ------------------------------------------------
    fecha_creacion_sistema = models.DateTimeField(auto_now_add=True)
    fecha_modificacion_sistema = models.DateTimeField(auto_now=True)
    
    # ------------------------------------------------
    # Métodos
    # ------------------------------------------------
    
    def save(self, *args, **kwargs):
        """Autogenerar campos automáticos"""
        if not self.num_control:
            last = ObraGeneral.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.num_control = str(next_id).zfill(6)
        
        # Actualizar fecha/hora de transacción
        self.fecha_hora_ultima_transaccion = datetime.now().strftime("%d%m%Y%H%M%S")
        
        # Generar código de información (008)
        if not self.codigo_informacion:
            fecha_creacion = datetime.now().strftime("%d%m%y")
            self.codigo_informacion = fecha_creacion + ("|" * (40 - 6))
        
        # Sincronizar clasificación con número de control
        self.clasif_num_control = self.num_control
        
        # Sincronizar 092 $d con tipo de registro
        if self.tipo_registro == 'd':
            self.clasif_ms_imp = 'Ms'
        elif self.tipo_registro == 'c':
            self.clasif_ms_imp = 'Imp'
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validaciones"""
        from django.core.exceptions import ValidationError
        
        # Regla: Si hay compositor (100), NO debe haber 130
        if self.compositor and self.titulo_uniforme:
            raise ValidationError(
                "Si hay compositor (campo 100), debe usar campo 240, no 130"
            )
        
        # Regla: Si NO hay compositor, NO debe haber 240
        if not self.compositor and self.titulo_240:
            raise ValidationError(
                "Si no hay compositor, debe usar campo 130, no 240"
            )
        
        # Debe haber al menos uno: 100 o 130
        if not self.compositor and not self.titulo_uniforme:
            raise ValidationError(
                "Debe haber un punto de acceso principal: compositor (100) o título uniforme (130)"
            )
    
    def __str__(self):
        return f"Obra {self.num_control} ({self.get_tipo_registro_display()})"
    
    class Meta:
        verbose_name = "Obra Musical"
        verbose_name_plural = "Obras Musicales"
        ordering = ['-num_control']
