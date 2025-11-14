"""
Puntos de acceso principales (asientos principales):
- Campo 100: Compositor (subcampos $e)
"""

from django.db import models

# ================================================
#? 📌 CAMPO 100 - SUBCAMPOS REPETIBLES (R)
# ================================================

class FuncionCompositor(models.Model):
    """
    Campo 100 - Subcampo $e (R)
    Termino indicativo de funcion del compositor
    Permite múltiples funciones para un compositor en una obra
    """
    
    FUNCIONES = [
        ('arreglista', 'Arreglista'),
        ('coeditor', 'Coeditor'),
        ('compilador', 'Compilador'),
        ('compositor', 'Compositor'),
        ('copista', 'Copista'),
        ('dedicatario', 'Dedicatario'),
        ('editor', 'Editor'),
        ('prologuista', 'Prologuista'),
    ]
    
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='funciones_compositor',
        help_text="Obra a la que pertenece esta funcion"
    )
    
    # Subcampo $e - Funcion (R)
    funcion = models.CharField(
        max_length=20,
        choices=FUNCIONES,
        default='compositor',
        help_text="100 $e – Funcion del compositor (predeterminado: compositor)"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Funcion Compositor (100 $e)"
        verbose_name_plural = "Funciones Compositor (100 $e - R)"
        ordering = ['obra', 'id']
    
    def __str__(self):
        return self.get_funcion_display()
