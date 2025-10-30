from django.db import models

# Create your models here.
class ObraGeneral(models.Model):
    # Cabeceras MARC21 Musical
    num_control = models.IntegerField(max_length=6,unique=True, blank=False, null=False)
    fecha_hora_ultima_transaccion =  models.DateTimeField(auto_now=True)
    codigo_informacion = models.CharField(max_length=39, blank=True, null=True)
    # CAMPOS 0XX
    # CAMPOS 1XX
    # CAMPOS 2XX
    # CAMPOS 3XX
    # CAMPOS 4XX
    # CAMPOS 5XX
    # CAMPOS 6XX
    # CAMPOS 7XX
    # CAMPOS 8XX


    def __str__(self):
        return f"Obra MARC - {self.titulo_encabezamiento or 'Sin título'}"
