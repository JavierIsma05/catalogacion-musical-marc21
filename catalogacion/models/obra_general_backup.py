"""
Modelo Principal MARC21 - ObraBase y Modelos Concretos
======================================

Implementa herencia de tablas abstractas según las 6 plantillas MARC21:
1. ColeccionManuscrita
2. ObraIndividualEnColeccionManuscrita
3. ObraIndividualManuscrita
4. ColeccionImpresa
5. ObraIndividualEnColeccionImpresa
6. ObraIndividualImpresa

Modelo base abstracto ObraBase contiene campos comunes.
Clase ObraGeneral se mantiene para compatibilidad con código legacy.
"""

from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime



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
# MODELO BASE ABSTRACTO - CAMPOS COMUNES
# ================================================

class ObraBase(models.Model):
    """
    Modelo principal que representa un registro bibliográfico MARC 21
    para música manuscrita o impresa
    """
    
    # ------------------------------------------------
    #? 🟩 CABECERA O LÍDER
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
    #? 🟨 CAMPOS FIJOS MARC21
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
    #? 🟦 BLOQUE 0XX – Campos de longitud variable
    # ------------------------------------------------

    # 020 ## ISBN (NR)
    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="020 $a – ISBN (NR - No Repetible)"
    )
    
    # 024 ## ISMN (NR)
    ismn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="024 $a – ISMN (NR - No Repetible)"
    )
    
    # 028 ## Número de editor (NR)
    # Primer indicador: Tipo de número de editor
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
        help_text="028 Primer indicador – Tipo de número de editor"
    )
    
    # Segundo indicador: Control de nota/punto de acceso adicional
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
        help_text="028 Segundo indicador – Control de nota/punto de acceso adicional"
    )
    
    # Subcampo $a - Número de editor
    numero_editor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="028 $a – Número de editor, plancha o placa (NR - No Repetible)"
    )
    
    # Subcampo $b - Nombre del editor
    nombre_editor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="028 $b – Nombre del editor (NR - No Repetible)"
    )
    
    #* Campo 031 implementado como modelo separado: IncipitMusical
    
    # 040 ## Fuente de catalogación
    centro_catalogador = models.CharField(
        max_length=10, 
        default='UNL',
        help_text="040 $a – Centro catalogador (predeterminado: UNL)"
    )
    
    #* Campo 041 implementado como modelo repetible: CodigoLengua
    #* Campo 044 implementado como modelo repetible: CodigoPaisEntidad
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
        'AutoridadPersona',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_como_compositor',
        help_text="100 $a y $d – Compositor principal (cruzar con 600, 700)"
    )
    
    #* Subcampo $e (R) - Campo repetible en modelo separado: FuncionCompositor
    
    # 100 $j - Autoria (NR)
    autoria = models.CharField(
        max_length=50,
        choices=[
            ('atribuida', 'Atribuida'),
            ('certificada', 'Certificada'),
            ('erronea', 'Erronea'),
        ],
        default='certificada',
        blank=True,
        null=True,
        help_text="100 $j – Autoria del compositor (NR - No Repetible)"
    )

    #* 130 0# Título uniforme como punto de acceso principal (NR)
    titulo_uniforme = models.ForeignKey(
        'AutoridadTituloUniforme',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_130',
        help_text="130 $a – Título uniforme normalizado (cruzar con campo 240)"
    )
    
    # 130 $k - Forma (NR)
    forma_130 = models.ForeignKey(
        'AutoridadFormaMusical',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_forma_130',
        help_text="130 $k – Forma musical (NR - No Repetible)"
    )
    
    # 130 $m - Medio de interpretación (NR)
    medio_interpretacion_130 = models.CharField(
        max_length=200,
        choices=[("piano", "piano")],
        default="piano",
        help_text="130 $m – Medio de interpretación (NR - No Repetible)"
    )
    
    # 130 $n - Número de parte/sección (NR)
    numero_parte_130 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="130 $n – Número de parte/sección (NR - No Repetible)"
    )
    
    # 130 $o - Arreglo (NR)
    arreglo_130 = models.CharField(
        max_length=10,
        choices=[("arreglo", "arreglo")],
        default="arreglo",
        help_text="130 $o – Arreglo (NR - No Repetible)"
    )
    
    # 130 $p - Nombre de parte/sección (NR)
    nombre_parte_130 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="130 $p – Nombre de parte/sección (NR - No Repetible)"
    )

    # 130 $r - Tonalidad (NR)
    tonalidad_130 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="130 $r – Tonalidad (NR - No repetible)"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 2XX – Títulos y mención de responsabilidad
    # ------------------------------------------------
    
    #* 240 10 $a Título uniforme con compositor (NR)
    titulo_240 = models.ForeignKey(
        'AutoridadTituloUniforme',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_240',
        help_text="240 $a – Título uniforme normalizado (cruzar con campo 130)"
    )
    
    # 240 $k - Forma (NR)
    forma_240 = models.ForeignKey(
        'AutoridadFormaMusical',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_forma_240',
        help_text="240 $k – Forma musical (NR - No Repetible)"
    )
    
    # 240 $m - Medio de interpretación (NR)   
    medio_interpretacion_240 = models.CharField(
        max_length=200,
        choices=[("piano", "piano")],
        default="piano",
        help_text="240 $m – Medio de interpretación (NR - No Repetible)"
    )
    
    # 240 $n - Número de parte/sección (NR)
    numero_parte_240 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="240 $n – Número de parte/sección (NR - No Repetible)"
    )
    
    # 240 $p - Nombre de parte/sección (NR)
    nombre_parte_240 = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="240 $p – Nombre de parte/sección (NR - No Repetible)"
    )
    
    # 240 $o - Arreglo (NR)
    arreglo_240 = models.CharField(
        max_length=10,
        choices=[("arreglo", "arreglo")],
        default="arreglo",
        help_text="240 $o – Arreglo (NR - No Repetible)"
    )
    
    # 240 $r - Tonalidad (NR)
    tonalidad_240 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TONALIDADES,
        help_text="240 $r – Tonalidad (NR - No repetible)"
    )
    
    #* Campo 245 → TituloYResponsabilidad
    
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
    
    #* Campo 246 → TituloAlternativo
    #* Campo 250 → Edicion
    #* Campo 264 → ProduccionPublicacion

    # ------------------------------------------------
    #? 🟦 BLOQUE 3XX – Descripción física
    # ------------------------------------------------

    # 300 $a - Extensión (NR)
    extension = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $a – Extensión (NR - No Repetible)"
    )
    
    # 300 $b - Otras características físicas (NR)
    otras_caracteristicas = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $b – Otras características físicas (NR - No Repetible)"
    )
    
    # 300 $c - Dimensión (NR)
    dimension = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="300 $c – Dimensión (NR - No Repetible)"
    )
    
    # 300 $e - Material acompañante (NR)
    material_acompanante = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="300 $e – Material acompañante (NR - No Repetible)"
    )
    
    #* 340 $d - Técnica (NR)
    
    TECNICAS = [
        ('autógrafo', 'Autógrafo'),
        ('posible autógrafo', 'Posible autógrafo'),
        ('manuscrito', 'Manuscrito'),
        ('manuscrito de copista no identificado', 'Manuscrito de copista no identificado'),
        ('impreso', 'Impreso'),
        ('fotocopia de manuscrito', 'Fotocopia de manuscrito'),
        ('fotocopia de impreso', 'Fotocopia de impreso'),
    ]

    # 340 $d - Técnica (NR) 
    ms_imp = models.CharField(
        max_length=200,
        choices=TECNICAS,
        blank=True,
        null=True,
        help_text="340 $d – Técnica (NR - No Repetible)"
    )
    
    #* 348 $a - Formato de la música notada (NR)
    FORMATOS = [
        ('parte', 'parte'),
        ('partitura', 'partitura'),
        ('partitura de coro', 'partitura de coro'),
        ('partitura piano vocal', 'partitura piano vocal'),
    ]

    formato = models.CharField(
        max_length=100,
        choices=FORMATOS,
        blank=True,
        null=True,
        help_text="348 $a – Formato de la música notada (NR - No Repetible)"
    )

    
    #* 382 $b - Solista (NR)
    solista = models.CharField(
        max_length=100,
        choices=[("piano", "piano")],
        default="piano",
        help_text="240 $m – Medio de interpretación (NR - No Repetible)"
    )
    
    
    #* 383 $a - Número de obra (NR)
    numero_obra = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="383 $a – Número serial de obra musical (NR - No Repetible)"
    )
    
    # 383 $b - Número de opus (NR)
    opus = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="383 $b – Número de opus (NR - No Repetible)"
    )
    
    #* 384 $a - Tonalidad (NR)
    tonalidad_384 = models.CharField(
        max_length=20,
        choices=TONALIDADES,
        blank=True,
        null=True,
        help_text="384 $a – Tonalidad (NR - No Repetible)"
    )
    
    # ------------------------------------------------
    #? 🟦 BLOQUE 4XX – Series
    # ------------------------------------------------
    
    #* Campo 490 → MencionSerie490, TituloSerie490, VolumenSerie490
    
    # ------------------------------------------------
    #? 🟦 BLOQUES 5XX
    # ------------------------------------------------
    sumario_520 = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        help_text="520 ## $a Sumario (NR)"
    )
    # ------------------------------------------------
    #? 🟦 BLOQUES 6XX
    # ------------------------------------------------
    
    # 650 $a - Materia principal (NR)
    materia_principal_650 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="650 $a – Materia (Tema principal) (NR)"
    )

    # 655 $a - Materia de género/forma (NR)
    materia_genero_655 = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="655 $a – Materia (Género/Forma) (NR)"
    )
    # ------------------------------------------------
    #? 🟦 BLOQUE 7XX – Puntos de acceso adicionales y relaciones (NR)
    # ------------------------------------------------

    # 700 $a – Nombre personal principal (NR)
    nombre_relacionado_700a = models.ForeignKey(
        'AutoridadPersona',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_relacionadas_700a',
        help_text="700 $a – Nombre personal relacionado (NR)"
    )

    # 700 $d – Coordenadas biográficas (NR)
    coordenadas_biograficas_700d = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="700 $d – Coordenadas biográficas (NR)"
    )

    # 700 $t – Título de obra relacionada (NR)
    titulo_relacionado_700t = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="700 $t – Título de la obra relacionada (NR)"
    )

    # 710 $a – Entidad o jurisdicción relacionada (NR)
    entidad_relacionada_710a = models.ForeignKey(
        'AutoridadEntidad',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_relacionadas_710a',
        help_text="710 $a – Entidad o jurisdicción relacionada (NR)"
    )

    # 773 $a – Compositor de la colección (NR)
    compositor_coleccion_773a = models.ForeignKey(
        'AutoridadPersona',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_coleccion_773a',
        help_text="773 $a – Compositor de la colección (NR)"
    )

    # 773 $t – Título de colección (NR)
    titulo_coleccion_773t = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="773 $t – Título de la colección (NR)"
    )
    # 774 $a – Enlace a la unidad constituyente (NR)
    enlace_unidad_774 = models.URLField(
        blank=True,
        null=True,
        help_text="774 $a – Enlace a la unidad constituyente (NR)"
    )
    # 774 $t – Título de la unidad constituyente (NR)
    titulo_unidad_774t = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="774 $t – Título de la unidad constituyente (NR)"
    )
    # 787 $a – Encabezamiento principal (NR)
    encabezamiento_principal_787a = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="787 $a – Encabezamiento principal (NR)"
    )

    # 787 $t – Título de la obra relacionada (NR)
    titulo_obra_relacionada_787t = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="787 $t – Título de la obra relacionada (NR)"
    )
    # ------------------------------------------------
    #? 🟦 BLOQUE 8XX – Ubicación y disponibilidad
    # ------------------------------------------------

    # 852 $a – Institución o persona (NR)
    institucion_persona_852a = models.ForeignKey(
        'AutoridadEntidad',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='obras_ubicacion_852a',
        help_text="852 $a – Institución o persona (NR). Enlace a autoridad institucional."
    )


    # 852 $h – Signatura original (NR)
    signatura_original_852h = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="852 $h – Signatura original (NR)"
    )

  
    # ------------------------------------------------
    #? Metadatos del sistema
    fecha_creacion_sistema = models.DateTimeField(auto_now_add=True)
    fecha_modificacion_sistema = models.DateTimeField(auto_now=True)
    
    #? Métodos
    # ------------------------------------------------

    def generar_relaciones_7xx(self):
        """
        Genera resumen de relaciones adicionales (700–710)
        para visualización rápida o exportación MARC.
        """
        nombres = [str(n.persona) for n in self.nombres_relacionados_700.all()]
        entidades = [str(e.entidad) for e in self.entidades_relacionadas_710.all()]
        return ", ".join(nombres + entidades) or "Sin relaciones registradas"
    
    def get_enlaces_8xx(self):
        """
        Devuelve enlaces y ubicaciones disponibles (852, 856)
        para mostrar o exportar.
        """
        ubicaciones = [str(u) for u in self.ubicaciones_852.all()]
        enlaces = [str(e) for e in self.disponibles_856.all()]
        return ubicaciones + enlaces


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
        from .bloque_3xx import MedioFisico, Tecnica340
        
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
        # Generar número de control si no existe
        if not self.num_control:
            try:
                ultima_obra = ObraGeneral.objects.order_by('-id').first()
                siguiente_id = 1 if not ultima_obra else ultima_obra.id + 1
            except:
                siguiente_id = 1
            
            tipo_abrev = 'M' if self.tipo_registro == 'd' else 'I'
            self.num_control = f"{tipo_abrev}{str(siguiente_id).zfill(6)}"
        
        # Generar código de información (campo 008)
        if not self.codigo_informacion:
            fecha_creacion = datetime.now().strftime("%y%m%d")  
            self.codigo_informacion = fecha_creacion + (" " * (40 - len(fecha_creacion)))
        
        # Establecer estado del registro
        if not self.estado_registro:
            self.estado_registro = 'n'  # n = nuevo registro
        
        # Generar clasificación 092
        self.generar_clasificacion_092()
        
        # Guardar primero el objeto
        super().save(*args, **kwargs)
        
        # Generar medio físico automático (340) después del save
        self.generar_medio_fisico_automatico()
        
        # Actualizar campos de clasificación
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
        
        # Validar título principal obligatorio
        if not self.titulo_principal or not self.titulo_principal.strip():
            errores['titulo_principal'] = (
                "El título principal (campo 245 $a) es obligatorio."
            )
        
        # Validar tipo de registro
        if self.tipo_registro not in ['c', 'd']:
            errores['tipo_registro'] = (
                "El tipo de registro debe ser 'c' (música impresa) o 'd' (música manuscrita)."
            )
        
        # Validar nivel bibliográfico
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
