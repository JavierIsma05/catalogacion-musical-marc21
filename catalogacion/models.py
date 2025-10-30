from django.db import models
from datetime import datetime

class ObraGeneral(models.Model):
    # --------------------------------------
    # 🟩 CABECERA O LÍDER (000)
    # --------------------------------------
    estado_registro = models.CharField(
        max_length=1,
        default='n',
        editable=False,
        help_text="05 – Estado del registro. Valor predeterminado 'n' (nuevo). No genera vista de usuario."
    )

    tipo_registro = models.CharField(
        max_length=1,
        choices=[
            ('c', 'Música impresa'),
            ('d', 'Música manuscrita'),
        ],
        default='d',
        help_text="06 – Tipo de registro. Define si es música impresa o manuscrita."
    )

    nivel_bibliografico = models.CharField(
        max_length=1,
        choices=[
            ('a', 'Parte componente'),
            ('c', 'Colección'),
            ('m', 'Obra independiente'),
        ],
        default='m',
        help_text="07 – Nivel bibliográfico. Indica si es parte, colección o obra independiente."
    )

    # --------------------------------------
    # 🟨 CAMPOS FIJOS MARC21
    # --------------------------------------
    # 001 – Número de control
    num_control = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        help_text="Código numérico único del registro (equivalente a una cédula MARC21)."
    )

    # 005 – Fecha y hora de la última transacción
    fecha_hora_ultima_transaccion = models.CharField(
        max_length=14,
        editable=False,
        help_text="Fecha codificada en formato ddmmaaaahhmmss (día, mes, año, hora, minutos, segundos)."
    )

    # 008 – Códigos de información de longitud fija
    codigo_informacion = models.CharField(
        max_length=40,
        editable=False,
        help_text="Campo de 40 posiciones. Solo 00–05 se usan (ddmmaa), el resto se completa con '|'."
    )

    # --------------------------------------
    # Campo auxiliar para mostrar información
    # --------------------------------------
    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descripción opcional visible para el usuario."
    )

    def save(self, *args, **kwargs):
        """
        Generación automática de los códigos MARC21.
        """
        # 🔹 Generar número de control (001)
        if not self.num_control:
            last = ObraGeneral.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.num_control = str(next_id).zfill(6)

        # 🔹 Generar fecha y hora de transacción (005)
        self.fecha_hora_ultima_transaccion = datetime.now().strftime("%d%m%Y%H%M%S")

        # 🔹 Generar código de información (008)
        fecha_creacion = datetime.now().strftime("%d%m%y")
        self.codigo_informacion = fecha_creacion + ("|" * (40 - 6))

        super().save(*args, **kwargs)

    def __str__(self):
        tipo = self.get_tipo_registro_display()
        nivel = self.get_nivel_bibliografico_display()
        return f"{self.num_control} - {tipo} ({nivel})"
