from django.db import models
from datetime import datetime

class ObraGeneral(models.Model):
    # ------------------------------------------------
    # 🟩 CABECERA O LÍDER (ya definido previamente)
    # ------------------------------------------------
    estado_registro = models.CharField(max_length=1, default='n', editable=False)
    tipo_registro = models.CharField(
        max_length=1,
        choices=[('c', 'Música impresa'), ('d', 'Música manuscrita')],
        default='d'
    )
    nivel_bibliografico = models.CharField(
        max_length=1,
        choices=[('a', 'Parte componente'), ('c', 'Colección'), ('m', 'Obra independiente')],
        default='m'
    )

    # ------------------------------------------------
    # 🟨 CAMPOS FIJOS MARC21
    # ------------------------------------------------
    num_control = models.CharField(max_length=6, unique=True, editable=False)
    fecha_hora_ultima_transaccion = models.CharField(max_length=14, editable=False)
    codigo_informacion = models.CharField(max_length=40, editable=False)

    # ------------------------------------------------
    # 🟦 BLOQUE 0XX – Campos de longitud variable
    # ------------------------------------------------
    # 020 ## Número Internacional Normalizado para Libros (ISBN)
    isbn = models.CharField(
        max_length=20, blank=True, null=True,
        help_text="020 $a – ISBN tomado tal como aparece en la fuente. Genera vista de usuario."
    )

    # 024 2# Otros identificadores normalizados (ISMN)
    ismn = models.CharField(
        max_length=20, blank=True, null=True,
        help_text="024 $a – ISMN tomado tal como aparece en la fuente. Genera vista de usuario."
    )

    # 028 20 Número de editor
    numero_editor = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="028 $a – Número de plancha, placa o código distintivo del editor. Genera vista de usuario."
    )
    indicador_028 = models.CharField(
        max_length=2, default='20',
        help_text="028 Indicador. Predeterminado '20', con opción de cambiar."
    )

    # 031 ## Información del íncipit musical
    incipit_num_obra = models.PositiveIntegerField(default=1, help_text="031 $a – Número de la obra.")
    incipit_num_movimiento = models.PositiveIntegerField(default=1, help_text="031 $b – Número del movimiento.")
    incipit_num_pasaje = models.PositiveIntegerField(default=1, help_text="031 $c – Número de pasaje.")
    incipit_titulo = models.CharField(max_length=100, blank=True, null=True, help_text="031 $d – Título o encabezamiento del íncipit.")
    incipit_voz_instrumento = models.CharField(max_length=100, blank=True, null=True, help_text="031 $m – Voz o instrumento.")
    incipit_notacion = models.TextField(blank=True, null=True, help_text="031 $p – Íncipit musical codificado.")
    incipit_url = models.URLField(blank=True, null=True, help_text="031 $u – URL del íncipit en otra base de datos.")

    # 040 ## Fuente de la catalogación
    centro_catalogador = models.CharField(
        max_length=10, default='UNL',
        help_text="040 $a – Centro catalogador de origen (UNL)."
    )

    # 041 0# Código de lengua
    codigo_lengua = models.CharField(
        max_length=3, default='spa',
        choices=[
            ('spa', 'Español'),
            ('eng', 'Inglés'),
            ('fra', 'Francés'),
            ('ger', 'Alemán'),
            ('ita', 'Italiano'),
            ('lat', 'Latín'),
        ],
        help_text="041 $a – Código de lengua MARC21."
    )

    # 044 ## Código del país de la entidad editora
    codigo_pais = models.CharField(
        max_length=3, default='ec',
        choices=[
            ('ec', 'Ecuador'),
            ('us', 'Estados Unidos'),
            ('es', 'España'),
            ('fr', 'Francia'),
            ('it', 'Italia'),
            ('de', 'Alemania'),
        ],
        help_text="044 $a – Código MARC del país."
    )

    # 092 ## Clasificación local
    clasif_institucion = models.CharField(max_length=50, default='UNL', help_text="092 $a – Institución (duplica 040 $a).")
    clasif_proyecto = models.CharField(max_length=50, default='BLMP', help_text="092 $b – Proyecto asociado.")
    clasif_pais = models.CharField(max_length=50, default='EC', help_text="092 $c – País (duplica 044 $a).")
    clasif_ms_imp = models.CharField(
        max_length=3,
        choices=[('Ms', 'Manuscrito'), ('Imp', 'Impreso')],
        default='Ms',
        help_text="092 $d – Ms o Imp. Tipo de material."
    )
    clasif_num_control = models.CharField(max_length=6, editable=False, help_text="092 $0 – Duplica el número de control (001).")

    # ------------------------------------------------
    # 🔸 Sobrescribir save() para autogenerar datos
    # ------------------------------------------------
    def save(self, *args, **kwargs):
        if not self.num_control:
            last = ObraGeneral.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.num_control = str(next_id).zfill(6)
        self.fecha_hora_ultima_transaccion = datetime.now().strftime("%d%m%Y%H%M%S")
        fecha_creacion = datetime.now().strftime("%d%m%y")
        self.codigo_informacion = fecha_creacion + ("|" * (40 - 6))
        self.clasif_num_control = self.num_control
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Obra {self.num_control} ({self.get_tipo_registro_display()})"
    
    # ------------------------------------------------
    # 🟦 BLOQUE 1XX – Asientos principales (punto de acceso)
    # ------------------------------------------------
    
    # 100 1# Compositor (NR - No Repetible)
    compositor_apellidos_nombres = models.CharField(
        max_length=200, blank=True, null=True,
        help_text="100 $a – Apellidos, Nombres del compositor. Cruzar con campos 600 y 700."
    )
    compositor_coordenadas_biograficas = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="100 $d – Coordenadas biográficas (fecha nacimiento - fecha muerte)."
    )
    compositor_funcion = models.CharField(
        max_length=20, blank=True, null=True,
        choices=[
            ('arreglista', 'Arreglista'),
            ('coeditor', 'Coeditor'),
            ('compilador', 'Compilador'),
            ('compositor', 'Compositor'),
            ('copista', 'Copista'),
            ('dedicatario', 'Dedicatario'),
            ('editor', 'Editor'),
            ('prologuista', 'Prologuista'),
        ],
        default='compositor',
        help_text="100 $e – Función (R - Repetible)."
    )
    compositor_autoria = models.CharField(
        max_length=15, blank=True, null=True,
        choices=[
            ('atribuida', 'Atribuida'),
            ('certificada', 'Certificada'),
            ('errónea', 'Errónea'),
        ],
        default='certificada',
        help_text="100 $j – Autoría (R - Repetible)."
    )
    
    # 130 0# Título uniforme (punto de acceso principal) (NR - No Repetible)
    titulo_uniforme = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="130 $a – Título uniforme."
    )
    titulo_uniforme_subencabezamiento_forma = models.CharField(
        max_length=20, blank=True, null=True,
        choices=[
            ('adaptación', 'Adaptación'),
            ('boceto', 'Boceto'),
            ('fragmento', 'Fragmento'),
            ('selección', 'Selección'),
            ('tema con variaciones', 'Tema con variaciones'),
        ],
        help_text="130 $k – Subencabezamiento de forma (R - Repetible). Cruzar con campo 655."
    )
    titulo_uniforme_medio_interpretacion = models.CharField(
        max_length=100, blank=True, null=True,
        default='piano',
        help_text="130 $m – Medio de interpretación (R - Repetible). Ej: piano."
    )
    titulo_uniforme_num_parte_seccion = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="130 $n – Número de parte o sección de la obra (R - Repetible)."
    )
    titulo_uniforme_arreglo = models.CharField(
        max_length=10, blank=True, null=True,
        default='arreglo',
        help_text="130 $o – Arreglo (NR - No Repetible)."
    )
    titulo_uniforme_nombre_parte_seccion = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="130 $p – Nombre de parte o sección de la obra (R - Repetible)."
    )
    titulo_uniforme_tonalidad = models.CharField(
        max_length=15, blank=True, null=True,
        choices=[
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
        ],
        help_text="130 $r – Tonalidad (NR - No Repetible). 24 tonalidades mayores y menores."
    )
    
