from django.db import models
from datetime import datetime
from .models_repetibles import *

# Exportar todos los modelos para que estén disponibles con "from .models import ..."
__all__ = [
    # Autoridades
    'AutoridadPersona',
    'AutoridadTituloUniforme',
    'AutoridadFormaMusical',
    'AutoridadMateria',
    # Modelos repetibles 
    'TituloAlternativo',
    'Edicion',
    'ProduccionPublicacion',
    'ISBN',
    'ISMN',
    'NumeroEditor',
    'IncipitMusical',
    'CodigoLengua',
    'CodigoPaisEntidad',
    'FuncionCompositor',
    'AtribucionCompositor',
    'Forma130',
    'MedioInterpretacion130',
    'NumeroParteSección130',
    'NombreParteSección130',
    'Forma240',
    'MedioInterpretacion240',
    'NumeroParteSección240',
    'NombreParteSección240',
    'TituloAlternativo',
    'Edicion',
    'ProduccionPublicacion',
    'DescripcionFisica',
    'Extension300',
    'Dimension300',
    'MedioFisico',
    'Tecnica340',
    'CaracteristicaMusicaNotada',
    'Formato348',
    'MedioInterpretacion382',
    'MedioInterpretacion382_a',
    'Solista382',
    'NumeroInterpretes382',
    'DesignacionNumericaObra',
    'NumeroObra383',
    'Opus383',
    
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
# CONSTANTES 
# ================================================

TONALIDADES = [
    # Mayores
    ('Do mayor', 'Do mayor'),
    ('Do# mayor', 'Do# mayor'),
    ('Reb mayor', 'Re♭ mayor'),
    ('Re mayor', 'Re mayor'),
    ('Mib mayor', 'Mi♭ mayor'),
    ('Mi mayor', 'Mi mayor'),
    ('Fa mayor', 'Fa mayor'),
    ('Fa# mayor', 'Fa# mayor'),
    ('Sol mayor', 'Sol mayor'),
    ('Sol# mayor', 'Sol# mayor'),
    ('Lab mayor', 'La♭ mayor'),
    ('La mayor', 'La mayor'),
    ('Sib mayor', 'Si♭ mayor'),
    ('Si mayor', 'Si mayor'),
    
    # Menores
    ('Do menor', 'Do menor'),
    ('Do# menor', 'Do# menor'),
    ('Reb menor', 'Re♭ menor'),
    ('Re menor', 'Re menor'),
    ('Mib menor', 'Mi♭ menor'),
    ('Mi menor', 'Mi menor'),
    ('Fa menor', 'Fa menor'),
    ('Fa# menor', 'Fa# menor'),
    ('Sol menor', 'Sol menor'),
    ('Sol# menor', 'Sol# menor'),
    ('Lab menor', 'La♭ menor'),
    ('La menor', 'La menor'),
    ('Sib menor', 'Si♭ menor'),
    ('Si menor', 'Si menor'),
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
    
    #* Campo 041 implementado como modelo repetible: CodigoLengua en models_repetibles.py 
    #* Campo 044 implementado como modelo repetible: CodigoPaisEntidad en models_repetibles.py
    
    #* 092 ## Clasificación local
    # 092 $a - Institución (NR)
    clasif_institucion = models.CharField(
        max_length=10,
        default='UNL',
        editable=False,
        help_text="092 $a – Institución (duplica campo 040 $a)"
    )
    
    # 092 $b - Proyecto (NR)
    clasif_proyecto = models.CharField(
        max_length=50,
        default='BLMP',
        editable=False,
        help_text="092 $b – Proyecto"
    )
    
    # 092 $c - País (NR)
    # Se genera automáticamente del campo 044 $a
    clasif_pais = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        editable=False,
        help_text="092 $c – País (duplica campo 044 $a)"
    )
    
    # 092 $d - Ms/Imp (NR)
    # Se genera automáticamente de la posición 06 de cabecera (tipo_registro)
    clasif_ms_imp = models.CharField(
        max_length=3,
        choices=[
            ('Ms', 'Manuscrito'),
            ('Imp', 'Impreso'),
        ],
        blank=True,
        null=True,
        editable=False,
        help_text="092 $d – Ms (Manuscrito) o Imp (Impreso) - Cruza con posición 06 de cabecera"
    )
    
    # 092 $0 - Número de control (NR)
    # Se genera automáticamente del campo 001
    clasif_num_control = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        editable=False,
        help_text="092 $0 – Número de control (duplica campo 001)"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 1XX – Asientos principales
    # ------------------------------------------------
    
    #* 100 1# Compositor (NR - No Repetible)
    compositor = models.ForeignKey(
        AutoridadPersona,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_como_compositor',
        help_text="100 $a y $d – Compositor principal (cruzar con 600, 700)"
    )
    
    #* Subcampo $e (R) - Funciones del compositor implementado como modelo repetible: FuncionCompositor
    #* Subcampo $j (R) - Atribución del compositor implementado como modelo repetible: AtribucionCompositor
    
    #* 130 0# Título uniforme como punto de acceso principal (NR)
    titulo_uniforme = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_130',
        help_text="130 $a – Título uniforme normalizado (cruzar con campo 240)"
    )
    
    
    #* - 130 $k → Forma130 como modelo repetible en models_repetibles.py
    #* - 130 $m → MedioInterpretacion130 como modelo repetible en models_repetibles.py
    #* - 130 $n → NumeroParteSección130 como modelo repetible en models_repetibles.py
    #* - 130 $p → NombreParteSección130 como modelo repetible en models_repetibles.py

    titulo_uniforme_arreglo = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        default='arreglo',
        help_text="130 $o – Arreglo"
    )
    
    titulo_uniforme_tonalidad = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="130 $r – Tonalidad (NR - No repetible)"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 2XX – Títulos y mención de responsabilidad
    # ------------------------------------------------
    
    #* 240 10 Título uniforme con compositor (NR)
    titulo_240 = models.ForeignKey(
        AutoridadTituloUniforme,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_240',
        help_text="240 $a – Título uniforme normalizado (cruzar con campo 130)"
    )
    
    #* - 240 $k → Forma240 como modelo repetible en models_repetibles.py
    #* - 240 $m → MedioInterpretacion240 como modelo repetible en models_repetibles.py
    #* - 240 $n → NumeroParteSección240 como modelo repetible en models_repetibles.py
    #* - 240 $p → NombreParteSección240 como modelo repetible en models_repetibles.py
    
    titulo_240_arreglo = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default='arreglo',
        help_text="240 $o – Arreglo (NR - No repetible, predeterminado: arreglo)"
    )
    
    titulo_240_tonalidad = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="240 $r – Tonalidad (NR - No repetible)"
    )
    
    #* 245 10 Mención de título (NR)
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

    #? 🟦 BLOQUE 3XX 

    #* Campo 300 implementado como modelo separado: DescripcionFisica
    #* Campo 340 implementado como modelo separado: MedioFisico y Tecnica340
    #* Campo 348 implementado como modelo repetible: CaracteristicaMusicaNotada
    #* Campo 382 implementado como modelo repetible: MedioInterpretacion382
    #* Campo 383 implementado como modelo repetible: DesignacionNumericaObra, NumeroObra383, Opus383
    
    tonalidad_384 = models.CharField(
        max_length=20,
        choices=TONALIDADES,
        blank=True,
        null=True,
        help_text="384 $a – Tonalidad (NR)"
    )
    
    
    #? 🟦 BLOQUE 4XX 
    
    #? 🟦 BLOQUE 5XX 
    
    #? 🟦 BLOQUE 6XX 
    
    #? 🟦 BLOQUE 7XX
     
    #? 🟦 BLOQUE 8XX 
  
    # ------------------------------------------------
    #? Metadatos del sistema
    # ------------------------------------------------
    fecha_creacion_sistema = models.DateTimeField(auto_now_add=True)
    fecha_modificacion_sistema = models.DateTimeField(auto_now=True)
    
    # ------------------------------------------------
    # Métodos
    # ------------------------------------------------

    def generar_clasificacion_092(self):
        """
        Genera automáticamente el campo 092 completo (Clasificación local)
        Toma información de otros campos según especificaciones MARC21
        """
        self.clasif_institucion = self.centro_catalogador or 'UNL'
        self.clasif_proyecto = 'BLMP'
        
        try:
            primer_pais = self.codigos_pais_entidad.order_by('orden').first()
            if primer_pais:
                self.clasif_pais = primer_pais.codigo_pais.upper()
            else:
                self.clasif_pais = getattr(self, 'codigo_pais_simple', 'EC').upper()
        except:
            self.clasif_pais = 'EC'
        
        if self.tipo_registro == 'd':  # Música manuscrita
            self.clasif_ms_imp = 'Ms'
        elif self.tipo_registro == 'c':  # Música impresa
            self.clasif_ms_imp = 'Imp'
        else:
            self.clasif_ms_imp = 'Imp'  # Por defecto: Impreso
        
        self.clasif_num_control = self.num_control

    def get_signatura_completa(self):
        """
        Retorna la signatura completa en formato legible
        Formato: UNL-BLMP-EC-Ms-000001
        """
        if not all([self.clasif_institucion, self.clasif_proyecto, 
                    self.clasif_pais, self.clasif_ms_imp, self.clasif_num_control]):
            return "Pendiente de generar"
        
        return (
            f"{self.clasif_institucion}-"
            f"{self.clasif_proyecto}-"
            f"{self.clasif_pais}-"
            f"{self.clasif_ms_imp}-"
            f"{self.clasif_num_control}"
        )

    def get_campo_092_marc(self):
        """
        Retorna el campo 092 completo en formato MARC21
        """
        return (
            f"092 ## "
            f"$a{self.clasif_institucion} "
            f"$b{self.clasif_proyecto} "
            f"$c{self.clasif_pais} "
            f"$d{self.clasif_ms_imp} "
            f"$0{self.clasif_num_control}"
        )
        
    def generar_medio_fisico_automatico(self):
        """
        Autogenera MedioFisico con Tecnica340 basado en tipo_registro
        """
        # Solo generar si no existen medios físicos aún
        if self.medios_fisicos.exists():
            return
        
        medio = MedioFisico.objects.create(obra=self)
        
        # Agregar técnica automática según tipo_registro
        if self.tipo_registro == 'd':  # Manuscrito
            tecnica_automatica = 'manuscrito'
        elif self.tipo_registro == 'c':  # Impreso
            tecnica_automatica = 'impreso'
        else:
            return
        
        # Crear técnica dentro del MedioFisico
        Tecnica340.objects.create(
            medio_fisico=medio,
            tecnica=tecnica_automatica
        )


    def save(self, *args, **kwargs):
        """
        Override del método save para autogenerar campos automáticos
        según especificaciones MARC21
        """

        if not self.num_control:
            try:
                ultima_obra = ObraGeneral.objects.order_by('-id').first()
                siguiente_id = 1 if not ultima_obra else ultima_obra.id + 1
            except:
                siguiente_id = 1
            
            tipo_abrev = 'M' if self.tipo_registro == 'd' else 'I'
            self.num_control = f"{tipo_abrev}{str(siguiente_id).zfill(6)}"
        

        if not self.codigo_informacion:
            fecha_creacion = datetime.now().strftime("%y%m%d")  
            self.codigo_informacion = fecha_creacion + (" " * (40 - len(fecha_creacion)))
        

        if not self.estado_registro:
            self.estado_registro = 'n'  # n = nuevo registro
        
        # Generar clasificación 092
        self.generar_clasificacion_092()
        
        # Generar medio físico automático (340)
        self.generar_medio_fisico_automatico()

        super().save(*args, **kwargs)
        

        ObraGeneral.objects.filter(pk=self.pk).update(
            clasif_institucion=self.clasif_institucion,
            clasif_proyecto=self.clasif_proyecto,
            clasif_pais=self.clasif_pais,
            clasif_ms_imp=self.clasif_ms_imp,
            clasif_num_control=self.clasif_num_control
        )

    def clean(self):
        """
        Validaciones de negocio según reglas MARC21
        Se ejecuta antes de save() cuando se usa full_clean()
        """
        from django.core.exceptions import ValidationError
        
        errores = {}
        
        
        # Regla: Si hay compositor (100), NO debe haber 130
        if self.compositor and self.titulo_uniforme:
            errores['compositor'] = (
                "Si hay compositor (campo 100), debe usar campo 240 para el título uniforme, "
                "no campo 130. El campo 130 es solo para obras anónimas."
            )
            errores['titulo_uniforme'] = (
                "No puede usar campo 130 cuando hay compositor. Use campo 240 en su lugar."
            )
        
        # Regla: Si NO hay compositor, NO debe haber 240
        if not self.compositor and self.titulo_240:
            errores['titulo_240'] = (
                "El campo 240 solo se usa cuando hay compositor (campo 100). "
                "Si no hay compositor, use campo 130 para el título uniforme."
            )
        
        # Regla: Debe haber al menos uno: 100 o 130
        if not self.compositor and not self.titulo_uniforme:
            errores['compositor'] = (
                "Debe haber un punto de acceso principal. Complete el campo 100 (compositor) "
                "o el campo 130 (título uniforme para obras anónimas)."
            )
            errores['titulo_uniforme'] = (
                "Debe haber un punto de acceso principal. Complete el campo 130 (título uniforme) "
                "o el campo 100 (compositor)."
            )

        
        if not self.titulo_principal or not self.titulo_principal.strip():
            errores['titulo_principal'] = (
                "El título principal (campo 245 $a) es obligatorio."
            )
        
        
        if self.tipo_registro not in ['c', 'd']:
            errores['tipo_registro'] = (
                "El tipo de registro debe ser 'c' (música impresa) o 'd' (música manuscrita)."
            )
        
        
        if self.nivel_bibliografico not in ['a', 'c', 'm']:
            errores['nivel_bibliografico'] = (
                "El nivel bibliográfico debe ser 'a' (parte componente), "
                "'c' (colección) o 'm' (obra independiente)."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        """Representación en string del objeto"""
        if self.compositor:
            return f"{self.num_control or 'Sin N°'}: {self.titulo_principal} - {self.compositor}"
        elif self.titulo_uniforme:
            return f"{self.num_control or 'Sin N°'}: {self.titulo_uniforme}"
        return f"{self.num_control or 'Sin N°'}: {self.titulo_principal}"

    class Meta:
        verbose_name = "Obra Musical MARC21"
        verbose_name_plural = "Obras Musicales MARC21"
        ordering = ['-num_control']
        indexes = [
            models.Index(fields=['num_control']),
            models.Index(fields=['tipo_registro']),
            models.Index(fields=['nivel_bibliografico']),
            models.Index(fields=['-fecha_creacion_sistema']),
        ]
