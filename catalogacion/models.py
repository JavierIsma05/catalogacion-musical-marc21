from django.db import models

# Create your models here.
class ObraMarc(models.Model):
    # 🔸 Datos de cabecera
    estado_registro = models.CharField(max_length=50, choices=[
        ('n', 'Nuevo'),
        ('c', 'Corregido'),
        ('d', 'Eliminado'),
    ])
    tipo_registro = models.CharField(max_length=50, choices=[
        ('c', 'Música notada impresa'),
        ('d', 'Música notada manuscrita'),
    ])
    nivel_bibliografico = models.CharField(max_length=50, choices=[
        ('b', 'Parte componente seriada'),
        ('m', 'Monografía'),
    ])
    nivel_codificacion = models.CharField(max_length=50, choices=[
        ('7', 'Nivel mínimo'),
        ('n', 'Completo'),
    ])
    forma_catalogacion = models.CharField(max_length=50, choices=[
        ('a', 'AACR 2'),
        ('i', 'ISBD'),
    ])

    # 🔹 Campos 0XX
    tipo_fecha_publicacion = models.CharField(max_length=100, blank=True, null=True)
    primera_fecha = models.CharField(max_length=20, blank=True, null=True)
    segunda_fecha = models.CharField(max_length=20, blank=True, null=True)
    lugar_publicacion = models.CharField(max_length=150, blank=True, null=True)
    forma_composicion = models.CharField(max_length=100, blank=True, null=True)
    tipo_recurso = models.CharField(max_length=100, blank=True, null=True)
    lengua = models.CharField(max_length=10, blank=True, null=True)
    material_anejo = models.CharField(max_length=100, blank=True, null=True)

    numero_copyright = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    isbn_disponibilidad = models.CharField(max_length=100, blank=True, null=True)
    isbn_invalido = models.CharField(max_length=50, blank=True, null=True)
    ismn = models.CharField(max_length=50, blank=True, null=True)
    ismn_incorrecto = models.CharField(max_length=50, blank=True, null=True)

    # 🔹 Campos 3XX (028 y 031)
    numero_plancha = models.CharField(max_length=100, blank=True, null=True)
    fuente_plancha = models.CharField(max_length=100, blank=True, null=True)

    numero_obra = models.CharField(max_length=100, blank=True, null=True)
    numero_movimiento = models.CharField(max_length=100, blank=True, null=True)
    numero_pasaje = models.CharField(max_length=100, blank=True, null=True)
    titulo_encabezamiento = models.CharField(max_length=150, blank=True, null=True)
    clave = models.CharField(max_length=20, blank=True, null=True)
    instrumento = models.CharField(max_length=100, blank=True, null=True)
    armadura = models.CharField(max_length=50, blank=True, null=True)
    notacion_token = models.TextField(blank=True, null=True)
    nota_general = models.TextField(blank=True, null=True)
    tonalidad = models.CharField(max_length=20, blank=True, null=True)
    nota_validez = models.CharField(max_length=100, blank=True, null=True)

    # 🔹 Campos 9XX (092 + archivos)
    clasificacion_a = models.CharField(max_length=100, blank=True, null=True)
    clasificacion_b = models.CharField(max_length=100, blank=True, null=True)
    clasificacion_c = models.CharField(max_length=100, blank=True, null=True)

    portada = models.FileField(upload_to='portadas/', blank=True, null=True)
    documento = models.FileField(upload_to='documentos/', blank=True, null=True)
    publicado = models.BooleanField(default=False)

    # 🔸 Fecha automática
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Obra MARC - {self.titulo_encabezamiento or 'Sin título'}"
