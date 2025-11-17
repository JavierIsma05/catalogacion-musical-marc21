"""
Formularios para bloque 7XX - Puntos de acceso adicionales y enlaces
"""
from django import forms
from django.contrib.contenttypes.models import ContentType
from catalogacion.models import (
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    Relacion700,
    Autoria700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    NumeroObraRelacionada773,
    EnlaceUnidadConstituyente774,
    NumeroObraRelacionada774,
    OtrasRelaciones787,
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
        fields = ['persona']
        widgets = {
            'persona': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
        }
        labels = {
            'persona': '700 $a - Nombre relacionado',
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


class Relacion700Form(forms.ModelForm):
    """Formulario para campo 700 $i - Información de relación"""
    
    class Meta:
        model = Relacion700
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class Autoria700Form(forms.ModelForm):
    """Formulario para campo 700 $j - Autoría"""
    
    class Meta:
        model = Autoria700
        fields = ['autoria']
        widgets = {
            'autoria': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'autoria': '700 $j - Término de autoría',
        }


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
        fields = ['encabezamiento_principal', 'titulo']
        widgets = {
            'encabezamiento_principal': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la colección o documento fuente'
            }),
        }
        labels = {
            'encabezamiento_principal': '773 $a - Encabezamiento principal',
            'titulo': '773 $t - Título',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['encabezamiento_principal'].required = True


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
        fields = ['encabezamiento_principal', 'titulo']
        widgets = {
            'encabezamiento_principal': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la obra constituyente'
            }),
        }
        labels = {
            'encabezamiento_principal': '774 $a - Encabezamiento principal',
            'titulo': '774 $t - Título de unidad constituyente',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['encabezamiento_principal'].required = True


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
        fields = ['titulo', 'numero_obra_relacionada']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_obra_relacionada': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'titulo': '787 $t - Título',
            'numero_obra_relacionada': '787 $w - Número de obra relacionada',
        }
