"""
Modelos auxiliares para ObraGeneral
Incluye validadores, soft-delete, y campos polimórficos
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


# ============================================
# SOFT DELETE MIXIN
# ============================================

class SoftDeleteMixin(models.Model):
    """
    Mixin para implementar soft-delete en los modelos.
    Los registros no se eliminan físicamente, solo se marcan como inactivos.
    """
    activo = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indica si el registro está activo o eliminado lógicamente"
    )
    fecha_eliminacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se eliminó lógicamente el registro"
    )
    eliminado_por = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Usuario que eliminó el registro"
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(self, usuario=None):
        """Elimina lógicamente el registro"""
        from django.utils import timezone
        self.activo = False
        self.fecha_eliminacion = timezone.now()
        if usuario:
            self.eliminado_por = usuario
        self.save()
    
    def restore(self):
        """Restaura un registro eliminado lógicamente"""
        self.activo = True
        self.fecha_eliminacion = None
        self.eliminado_por = None
        self.save()

    @property
    def dias_desde_eliminacion(self):
        """Retorna dias desde la eliminacion logica"""
        if not self.fecha_eliminacion:
            return 0
        from django.utils import timezone
        diferencia = timezone.now() - self.fecha_eliminacion
        return diferencia.days


# ============================================
# AUDITORÍA DE CAMBIOS
# ============================================

class HistorialCambio(models.Model):
    """
    Tabla de auditoría para rastrear cambios en los registros MARC.
    Registra quién, cuándo y qué cambió.
    """
    # Relación polimórfica con cualquier modelo
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Información del cambio
    accion = models.CharField(
        max_length=20,
        choices=[
            ('create', 'Creación'),
            ('update', 'Modificación'),
            ('delete', 'Eliminación'),
            ('restore', 'Restauración'),
        ],
        help_text="Tipo de acción realizada"
    )
    
    usuario = models.CharField(
        max_length=150,
        help_text="Usuario que realizó el cambio"
    )
    
    fecha_cambio = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Fecha y hora del cambio"
    )
    
    # Datos del cambio
    campos_modificados = models.JSONField(
        null=True,
        blank=True,
        help_text="Diccionario con los campos modificados {campo: {anterior: valor, nuevo: valor}}"
    )
    
    valores_completos = models.JSONField(
        null=True,
        blank=True,
        help_text="Snapshot completo del objeto después del cambio"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Dirección IP desde donde se hizo el cambio"
    )
    
    notas = models.TextField(
        blank=True,
        help_text="Notas adicionales sobre el cambio"
    )
    
    class Meta:
        verbose_name = "Historial de Cambio"
        verbose_name_plural = "Historial de Cambios"
        ordering = ['-fecha_cambio']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['-fecha_cambio']),
            models.Index(fields=['usuario']),
        ]
    
    def __str__(self):
        return f"{self.get_accion_display()} - {self.content_type} #{self.object_id} por {self.usuario}"


# ============================================
# ENCABEZAMIENTO POLIMÓRFICO PARA 773/774/787
# ============================================

class EncabezamientoEnlace(models.Model):
    """
    Modelo polimórfico para encabezamientos principales en enlaces jerárquicos.
    Permite que 773/774/787 apunten a Persona, Título Uniforme o Entidad.
    """
    # Relación polimórfica
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to={
            'model__in': ('autoridadpersona', 'autoridadtitulouniforme', 'autoridadentidad')
        },
        help_text="Tipo de autoridad (Persona, Título Uniforme o Entidad)"
    )
    object_id = models.PositiveIntegerField(
        help_text="ID de la autoridad"
    )
    encabezamiento = GenericForeignKey('content_type', 'object_id')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Encabezamiento de Enlace"
        verbose_name_plural = "Encabezamientos de Enlaces"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return str(self.encabezamiento) if self.encabezamiento else "Sin encabezamiento"
    
    def clean(self):
        """Validar que el content_type sea válido"""
        if self.content_type:
            modelo = self.content_type.model
            if modelo not in ['autoridadpersona', 'autoridadtitulouniforme', 'autoridadentidad']:
                raise ValidationError(
                    f"El tipo de contenido '{modelo}' no es válido. "
                    "Debe ser AutoridadPersona, AutoridadTituloUniforme o AutoridadEntidad."
                )


# ============================================
# CÓDIGO DE LENGUA (CAMPO 041)
# ============================================

class ObraLengua(models.Model):
    """
    Relación many-to-many ordenada entre ObraGeneral y CodigoLengua.
    Permite múltiples idiomas por obra con orden específico.
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='lenguas_obra'
    )
    
    lengua = models.ForeignKey(
        'CodigoLengua',
        on_delete=models.PROTECT,
        help_text="041 $a — Código de lengua del texto/sonido"
    )
    
    orden = models.PositiveSmallIntegerField(
        default=0,
        help_text="Orden de aparición del idioma"
    )
    
    tipo_lengua = models.CharField(
        max_length=1,
        choices=[
            ('a', 'Lengua del texto'),
            ('d', 'Lengua del resumen'),
            ('h', 'Lengua del original'),
        ],
        default='a',
        help_text="041 subcampo — Tipo de lengua"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Lengua de la Obra (041)"
        verbose_name_plural = "Lenguas de la Obra (041)"
        ordering = ['obra', 'orden']
        unique_together = [['obra', 'lengua', 'tipo_lengua']]
    
    def __str__(self):
        return f"{self.obra.num_control} - {self.lengua} ({self.get_tipo_lengua_display()})"
