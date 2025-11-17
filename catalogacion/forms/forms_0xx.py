"""
Formularios para bloque 0XX - Campos de control e identificación
"""
from django import forms
from catalogacion.models import (
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
)
from .widgets import TextAreaAutosize


class IncipitMusicalForm(forms.ModelForm):
    """Formulario para campo 031 - Íncipit musical"""
    
    class Meta:
        model = IncipitMusical
        fields = [
            'numero_obra',
            'numero_movimiento',
            'numero_pasaje',
            'titulo_encabezamiento',
            'voz_instrumento',
            'notacion_musical',
        ]
        widgets = {
            'numero_obra': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '031 $a - Número de obra',
            }),
            'numero_movimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '031 $b - Número de movimiento',
            }),
            'numero_pasaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '031 $c - Número de pasaje',
            }),
            'titulo_encabezamiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $d - Título/tempo',
            }),
            'voz_instrumento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $m - Voz/instrumento',
            }),
            'notacion_musical': TextAreaAutosize(attrs={
                'placeholder': '031 $p - Notación musical codificada',
                'rows': 4,
            }),
        }


class IncipitURLForm(forms.ModelForm):
    """Formulario para campo 031 $u - URL de íncipit"""
    
    class Meta:
        model = IncipitURL
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $u - URL del íncipit',
            }),
        }


class CodigoLenguaForm(forms.ModelForm):
    """Formulario para campo 041 - Código de lengua"""
    
    class Meta:
        model = CodigoLengua
        fields = [
            'indicacion_traduccion',
            'fuente_codigo',
        ]
        widgets = {
            'indicacion_traduccion': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fuente_codigo': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class IdiomaObraForm(forms.ModelForm):
    """Formulario para campo 041 $a - Idioma"""
    
    class Meta:
        model = IdiomaObra
        fields = ['codigo_idioma']
        widgets = {
            'codigo_idioma': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'codigo_idioma': '041 $a - Código de idioma',
        }


class CodigoPaisEntidadForm(forms.ModelForm):
    """Formulario para campo 044 $a - País de entidad"""
    
    class Meta:
        model = CodigoPaisEntidad
        fields = ['codigo_pais']
        widgets = {
            'codigo_pais': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'codigo_pais': '044 $a - Código de país',
        }
