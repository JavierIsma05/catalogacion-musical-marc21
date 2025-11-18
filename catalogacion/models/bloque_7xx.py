from django.db import models
from .autoridades import AutoridadPersona, AutoridadEntidad
from .auxiliares import EncabezamientoEnlace

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
# 🧑 700 1# Punto de acceso adicional – Nombre de persona (R)
# =====================================================

class NombreRelacionado700(models.Model):
    """
    700 1# – Punto de acceso adicional (Nombre de persona)
    $a (NR), $c (R), $d (NR), $e (R), $i (NR), $j (NR), $t (NR)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='nombres_relacionados_700',
    )

    persona = models.ForeignKey(
        AutoridadPersona,
        on_delete=models.PROTECT,
        help_text="700 $a – Apellidos, Nombres (controlado, NR)",
    )

    coordenadas_biograficas = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="700 $d – Coordenadas biográficas (NR)",
    )

    relacion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="700 $i – Información sobre la relación (NR)"
    )

    autoria = models.CharField(
        max_length=20,
        choices=AUTORIAS_CHOICES,
        blank=True,
        null=True,
        help_text="700 $j – Calificador de atribución (NR)"
    )

    titulo_obra = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="700 $t – Título de la obra (NR)",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "700 – Nombre relacionado"
        verbose_name_plural = "700 – Nombres relacionados (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return str(self.persona)


class TerminoAsociado700(models.Model):
    """700 $c – Término asociado al nombre (R)"""
    nombre_700 = models.ForeignKey(
        NombreRelacionado700,
        on_delete=models.CASCADE,
        related_name='terminos_asociados',
    )
    termino = models.CharField(
        max_length=100,
        help_text="700 $c – Término asociado al nombre (R)"
    )

    class Meta:
        verbose_name = "700 $c – Término asociado"
        verbose_name_plural = "700 $c – Términos asociados (R)"
        ordering = ['nombre_700', 'id']

    def __str__(self):
        return self.termino


class Funcion700(models.Model):
    """700 $e – Término indicativo de función (R)"""
    nombre_700 = models.ForeignKey(
        NombreRelacionado700,
        on_delete=models.CASCADE,
        related_name='funciones',
    )
    funcion = models.CharField(
        max_length=30,
        choices=FUNCIONES_PERSONA,
        help_text="700 $e – Función (R)"
    )

    class Meta:
        verbose_name = "700 $e – Función"
        verbose_name_plural = "700 $e – Funciones (R)"
        ordering = ['nombre_700', 'id']

    def __str__(self):
        return self.get_funcion_display()


# NOTA: Los subcampos $i (relación) y $j (autoría) ahora son campos
# no repetibles dentro de NombreRelacionado700


# =====================================================
# 🏛️ 710 2# Punto de acceso adicional – Entidad (R)
# =====================================================

class EntidadRelacionada710(models.Model):
    """
    710 2# – Punto de acceso adicional (Entidad)
    $a (NR), $e (R)
    """
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='entidades_relacionadas_710',
    )

    entidad = models.ForeignKey(
        AutoridadEntidad,
        on_delete=models.PROTECT,
        help_text="710 $a – Entidad/Jurisdicción (controlado, NR)",
    )

    funcion = models.CharField(
        max_length=50,
        choices=FUNCIONES_ENTIDAD,
        blank=True,
        null=True,
        help_text="710 $e – Función institucional (R)",
    )

    class Meta:
        verbose_name = "710 – Entidad relacionada"
        verbose_name_plural = "710 – Entidades relacionadas (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return str(self.entidad)


# =====================================================
# 📘 773, 📗 774, 🔗 787 – Relaciones entre obras
# =====================================================

class EnlaceDocumentoFuente773(models.Model):
    """773 1# – Enlace a documento fuente (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='enlaces_documento_fuente_773',
    )

    compositor_773 = models.ForeignKey(
        EncabezamientoEnlace,
        on_delete=models.PROTECT,
        help_text="773 $a – Compositor (Persona, Título o Entidad)",
    )

    titulo = models.CharField(
        max_length=250,
        help_text="773 $t – Título (NR)"
    )

    class Meta:
        verbose_name = "773 – Documento fuente"
        verbose_name_plural = "773 – Documentos fuente (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.titulo


class NumeroObraRelacionada773(models.Model):
    """773 $w – Número de la obra en la colección (R)"""
    enlace_773 = models.ForeignKey(
        EnlaceDocumentoFuente773,
        on_delete=models.CASCADE,
        related_name='numeros_obra',
    )
    
    numero = models.CharField(
        max_length=50,
        help_text="773 $w – Número de control 001 del registro de documento fuente"
    )

    class Meta:
        verbose_name = "773 $w – Número de obra"
        verbose_name_plural = "773 $w – Números de obra (R)"
        ordering = ['enlace_773', 'id']

    def __str__(self):
        return self.numero


class EnlaceUnidadConstituyente774(models.Model):
    """774 1# – Enlace a unidad constituyente (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='enlaces_unidades_774',
    )

    compositor_774 = models.ForeignKey(
        EncabezamientoEnlace,
        on_delete=models.PROTECT,
        help_text="774 $a – Compositor (Persona, Título o Entidad)",
    )

    titulo = models.CharField(
        max_length=250,
        help_text="774 $t – Título (NR)"
    )

    class Meta:
        verbose_name = "774 – Unidad constituyente"
        verbose_name_plural = "774 – Unidades constituyentes (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.titulo


class NumeroObraRelacionada774(models.Model):
    """774 $w – Número de obra relacionada (R)"""
    enlace_774 = models.ForeignKey(
        EnlaceUnidadConstituyente774,
        on_delete=models.CASCADE,
        related_name='numeros_obra',
    )
    
    numero = models.CharField(
        max_length=50,
        help_text="774 $w – Número de control de la obra constituyente"
    )

    class Meta:
        verbose_name = "774 $w – Número de obra"
        verbose_name_plural = "774 $w – Números de obra (R)"
        ordering = ['enlace_774', 'id']

    def __str__(self):
        return self.numero


class OtrasRelaciones787(models.Model):
    """787 1# – Otras relaciones (R)"""
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='otras_relaciones_787',
    )

    compositor_787 = models.ForeignKey(
        EncabezamientoEnlace,
        on_delete=models.PROTECT,
        help_text="787 $a – Encabezamiento principal (Persona, Título o Entidad)",
    )

    titulo = models.CharField(
        max_length=250,
        help_text="787 $t – Título (NR)"
    )

    class Meta:
        verbose_name = "787 – Otra relación"
        verbose_name_plural = "787 – Otras relaciones (R)"
        ordering = ['obra', 'id']

    def __str__(self):
        return self.titulo

class NumeroObraRelacionada787(models.Model):
    """787 $w – Número de obra relacionada (R)"""
    enlace_787 = models.ForeignKey(
        OtrasRelaciones787,
        on_delete=models.CASCADE,
        related_name='numeros_obra',
    )
    
    numero = models.CharField(
        max_length=50,
        help_text="787 $w – Número de control de la obra relacionada"
    )

    class Meta:
        verbose_name = "787 $w – Número de obra"
        verbose_name_plural = "787 $w – Números de obra (R)"
        ordering = ['enlace_787', 'id']

    def __str__(self):
        return self.numero