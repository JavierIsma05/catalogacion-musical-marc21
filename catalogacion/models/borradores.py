"""
Modelo para gestión de borradores de obras MARC21
Permite guardar el progreso de catalogación y recuperarlo posteriormente
"""
from django.db import models
from django.utils import timezone
import json


class BorradorObra(models.Model):
    """
    Modelo para guardar borradores de obras MARC21 en progreso.
    No requiere usuario ya que el sistema es personal (sin autenticación).
    """
    
    tipo_obra = models.CharField(
        max_length=50,
        help_text="Tipo de obra MARC21: manuscrito, impreso, coleccion, etc."
    )
    
    datos_formulario = models.JSONField(
        help_text="Datos del formulario serializados en JSON"
    )
    
    pestana_actual = models.IntegerField(
        default=0,
        help_text="Índice de la pestaña actual (0-8)"
    )
    
    titulo_temporal = models.CharField(
        max_length=500,
        blank=True,
        help_text="Título extraído del campo 245$a para mostrar en la lista"
    )
    
    num_control_temporal = models.CharField(
        max_length=50,
        blank=True,
        help_text="Número de control temporal si existe"
    )
    
    tipo_registro = models.CharField(
        max_length=1,
        blank=True,
        help_text="c=impreso, d=manuscrito"
    )
    
    nivel_bibliografico = models.CharField(
        max_length=1,
        blank=True,
        help_text="a=parte, c=colección, m=monografía"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('convertido', 'Convertido a Obra'),
            ('descartado', 'Descartado'),
        ],
        default='activo',
        help_text="Estado del borrador: activo (en progreso), convertido (publicado como obra), descartado (eliminado por usuario)"
    )
    
    obra_creada = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrador_origen',
        help_text="Obra final creada a partir de este borrador"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'catalogacion_borrador_obra'
        verbose_name = 'Borrador de Obra MARC21'
        verbose_name_plural = 'Borradores de Obras MARC21'
        ordering = ['-fecha_modificacion']
        indexes = [
            models.Index(fields=['-fecha_modificacion']),
            models.Index(fields=['tipo_obra']),
            models.Index(fields=['tipo_registro']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        titulo = self.titulo_temporal or "Sin título"
        fecha = self.fecha_modificacion.strftime('%d/%m/%Y %H:%M')
        return f"{titulo} ({fecha})"
    
    def extraer_metadatos(self):
        """Extrae título, tipo de registro y nivel bibliográfico del formulario"""
        try:
            datos = self.datos_formulario
            if isinstance(datos, str):
                datos = json.loads(datos)
            
            # Extraer título del campo 245$a (titulo_principal)
            self.titulo_temporal = datos.get('titulo_principal', '')[:500] or "Sin título"
            
            # Extraer tipo de registro y nivel bibliográfico
            self.tipo_registro = datos.get('tipo_registro', '')
            self.nivel_bibliografico = datos.get('nivel_bibliografico', '')
            
            # Extraer número de control si existe
            self.num_control_temporal = datos.get('num_control', '')
            
        except Exception as e:
            self.titulo_temporal = "Sin título"
            print(f"Error extrayendo metadatos: {e}")
    
    def save(self, *args, **kwargs):
        """Override save para extraer metadatos automáticamente"""
        self.extraer_metadatos()
        super().save(*args, **kwargs)
    
    @property
    def dias_desde_modificacion(self):
        """Retorna días desde última modificación"""
        diferencia = timezone.now() - self.fecha_modificacion
        return diferencia.days
    
    def get_descripcion_tipo(self):
        """Retorna descripción legible del tipo de obra"""
        tipos = {
            'manuscrito_independiente': 'Manuscrito Independiente',
            'manuscrito_coleccion': 'Manuscrito Colección',
            'impreso_independiente': 'Impreso Independiente',
            'impreso_coleccion': 'Impreso Colección',
        }
        return tipos.get(self.tipo_obra, self.tipo_obra)
