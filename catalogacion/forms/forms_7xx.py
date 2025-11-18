"""
Formularios para bloque 7XX - Puntos de acceso adicionales y enlaces
"""
from django import forms
from django.contrib.contenttypes.models import ContentType
from catalogacion.models import (
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    NumeroObraRelacionada773,
    EnlaceUnidadConstituyente774,
    NumeroObraRelacionada774,
    OtrasRelaciones787,
    NumeroObraRelacionada787,
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadEntidad,
    EncabezamientoEnlace,
)
from .widgets import Select2Widget, TextAreaAutosize


class NombreRelacionado700Form(forms.ModelForm):
    """Formulario para campo 700 - Nombre relacionado (contenedor)"""
    
    class Meta:
        model = NombreRelacionado700
        fields = ['persona', 'coordenadas_biograficas', 'relacion', 'autoria', 'titulo_obra']
        widgets = {
            'persona': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'coordenadas_biograficas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1900-1980'
            }),
            'relacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'intérprete de, arreglista de, etc.'
            }),
            'autoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'titulo_obra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la obra relacionada'
            }),
        }
        labels = {
            'persona': '700 $a - Nombre relacionado',
            'coordenadas_biograficas': '700 $d - Coordenadas biográficas',
            'relacion': '700 $i - Relación',
            'autoria': '700 $j - Autoría',
            'titulo_obra': '700 $t - Título de obra',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['persona'].queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')


class TerminoAsociado700Form(forms.ModelForm):
    """Formulario para campo 700 $c - Término asociado"""
    
    class Meta:
        model = TerminoAsociado700
        fields = ['termino']
        widgets = {
            'termino': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class Funcion700Form(forms.ModelForm):
    """Formulario para campo 700 $e - Función"""
    
    class Meta:
        model = Funcion700
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'funcion': '700 $e - Término de función',
        }


# NOTA: Los formularios Relacion700Form y Autoria700Form fueron eliminados
# porque $i (relación) y $j (autoría) ahora son campos no repetibles
# dentro de NombreRelacionado700Form


class EntidadRelacionada710Form(forms.ModelForm):
    """Formulario para campo 710 - Entidad corporativa"""
    
    class Meta:
        model = EntidadRelacionada710
        fields = ['entidad', 'funcion']
        widgets = {
            'entidad': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/entidad/',
            }),
            'funcion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'entidad': '710 $a - Nombre de entidad',
            'funcion': '710 $e - Función de la entidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entidad'].queryset = AutoridadEntidad.objects.all().order_by('nombre')


class EnlaceDocumentoFuente773Form(forms.ModelForm):
    """Formulario para campo 773 - Documento fuente"""
    
    class Meta:
        model = EnlaceDocumentoFuente773
        fields = ['compositor_773', 'titulo']
        widgets = {
            'compositor_773': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la colección o documento fuente'
            }),
        }
        labels = {
            'compositor_773': '773 $a - Compositor',
            'titulo': '773 $t - Título',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['compositor_773'].required = True


class NumeroObraRelacionada773Form(forms.ModelForm):
    """Formulario para 773 $w - Número de obra en la colección"""
    
    class Meta:
        model = NumeroObraRelacionada773
        fields = ['numero']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 001234567'
            }),
        }
        labels = {
            'numero': '773 $w - Número de obra',
        }


class EnlaceUnidadConstituyente774Form(forms.ModelForm):
    """Formulario para campo 774 - Unidad constituyente (obra contenida)"""
    
    class Meta:
        model = EnlaceUnidadConstituyente774
        fields = ['compositor_774', 'titulo']
        widgets = {
            'compositor_774': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la obra constituyente'
            }),
        }
        labels = {
            'compositor_774': '774 $a - Compositor',
            'titulo': '774 $t - Título de unidad constituyente',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['compositor_774'].required = True


class NumeroObraRelacionada774Form(forms.ModelForm):
    """Formulario para 774 $w - Número de obra relacionada"""
    
    class Meta:
        model = NumeroObraRelacionada774
        fields = ['numero']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 001234567'
            }),
        }
        labels = {
            'numero': '774 $w - Número de obra',
        }


class OtrasRelaciones787Form(forms.ModelForm):
    """Formulario para campo 787 - Otras relaciones"""
    
    class Meta:
        model = OtrasRelaciones787
        fields = ['compositor_787', 'titulo']
        widgets = {
            'compositor_787': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la obra relacionada'
            }),
        }
        labels = {
            'compositor_787': '787 $a - Compositor',
            'titulo': '787 $t - Título',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['compositor_787'].required = True


class NumeroObraRelacionada787Form(forms.ModelForm):
    """Formulario para 787 $w - Número de obra relacionada"""
    
    class Meta:
        model = NumeroObraRelacionada787
        fields = ['numero']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 001234567'
            }),
        }
        labels = {
            'numero': '787 $w - Número de obra',
        }
