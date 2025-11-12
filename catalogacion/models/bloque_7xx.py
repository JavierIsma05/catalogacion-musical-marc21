# =====================================================
# 📘 BLOQUE 7XX – Campos repetibles (R)
# =====================================================
from django.db import models
from .autoridades import AutoridadPersona, AutoridadEntidad

# =====================================================
# ⚙️ Choices (listas controladas)
# =====================================================
FUNCIONES_PERSONA = [
    ('arreglista', 'Arreglista'),
    ('coeditor', 'Coeditor'),
    ('compilador', 'Compilador'),
    ('compositor', 'Compositor'),
    ('copista', 'Copista'),
    ('dedicatario', 'Dedicatorio'),
    ('editor', 'Editor'),
    ('prologuista', 'Prologuista'),
]

AUTORIAS_CHOICES = [
    ('atribuida', 'Atribuida'),
    ('certificada', 'Certificada'),
    ('erronea', 'Errónea'),
]

FUNCIONES_ENTIDAD = [
    ('coeditor', 'Coeditor'),
    ('dedicatario', 'Dedicatorio'),
    ('editor', 'Editor'),
    ('lugar_ejecucion', 'Lugar de ejecución'),
    ('lugar_estreno', 'Lugar de estreno'),
    ('patrocinante', 'Patrocinante'),
]


# =====================================================
# 🧑 700 – Nombre relacionado (R)
# =====================================================
class TerminoAsociado700(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='terminos_asociados_700')
    termino = models.CharField(max_length=100, help_text="700 $c – Término asociado al nombre (R)")

    def __str__(self):
        return self.termino


class Funcion700(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='funciones_700')
    funcion = models.CharField(max_length=30, choices=FUNCIONES_PERSONA, help_text="700 $e – Función (R)")

    def __str__(self):
        return self.get_funcion_display()


class Relacion700(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='relaciones_700')
    descripcion = models.CharField(max_length=200, help_text="700 $i – Relación (R)")

    def __str__(self):
        return self.descripcion


class Autoria700(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='autoridades_autoria_700')
    autoria = models.CharField(max_length=20, choices=AUTORIAS_CHOICES, default='certificada', help_text="700 $j – Autoría (R)")

    def __str__(self):
        return self.get_autoria_display()


# =====================================================
# 🏛️ 710 – Entidad relacionada (R)
# =====================================================
class FuncionEntidad710(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='funciones_entidad_710')
    funcion = models.CharField(max_length=50, choices=FUNCIONES_ENTIDAD, help_text="710 $e – Función institucional (R)")

    def __str__(self):
        return self.get_funcion_display()


# =====================================================
# 📘 773, 774, 787 – Relaciones (R)
# =====================================================
class NumeroDocumentoRelacionado773(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='numeros_relacionados_773')
    numero = models.CharField(max_length=50, help_text="773 $w – Número de obra relacionada (R)")

    def __str__(self):
        return self.numero


class NumeroObraRelacionada774(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='numeros_relacionados_774')
    numero = models.CharField(max_length=50, help_text="774 $w – Número de obra relacionada (R)")

    def __str__(self):
        return self.numero


class NumeroObraRelacionada787(models.Model):
    obra = models.ForeignKey('ObraGeneral', on_delete=models.CASCADE, related_name='numeros_relacionados_787')
    numero = models.CharField(max_length=50, help_text="787 $w – Número de obra relacionada (R)")

    def __str__(self):
        return self.numero
