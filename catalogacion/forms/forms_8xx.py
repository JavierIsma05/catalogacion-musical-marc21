"""
Formularios para bloque 8XX - Ubicación y disponibilidad
"""
from django import forms
from catalogacion.models import (
    Ubicacion852,
    Estanteria852,
    Disponible856,
    URL856,
    TextoEnlace856,
)
from .widgets import TextAreaAutosize


class Ubicacion852Form(forms.ModelForm):
    """
    Formulario para campo 852 - Ubicación (contenedor)
    Los subcampos $a y $h están en ObraGeneral
    """
    
    class Meta:
        model = Ubicacion852
        fields = []  # No tiene campos propios, solo subcampos relacionados
        
    def __str__(self):
        return "852 - Ubicación"


class Estanteria852Form(forms.ModelForm):
    """Formulario para campo 852 $c - Estantería"""
    
    class Meta:
        model = Estanteria852
        fields = ['estanteria']
        widgets = {
            'estanteria': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'estanteria': '852 $c - Estantería',
        }


class Disponible856Form(forms.ModelForm):
    """
    Formulario para campo 856 - Disponible (contenedor)
    """
    
    class Meta:
        model = Disponible856
        fields = []  # No tiene campos propios, solo subcampos relacionados
        
    def __str__(self):
        return "856 - Recurso disponible"


class URL856Form(forms.ModelForm):
    """Formulario para campo 856 $u - URL"""
    
    class Meta:
        model = URL856
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'url': '856 $u - URL',
        }


class TextoEnlace856Form(forms.ModelForm):
    """Formulario para campo 856 $y - Texto del enlace"""
    
    class Meta:
        model = TextoEnlace856
        fields = ['texto_enlace']
        widgets = {
            'texto_enlace': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'texto_enlace': '856 $y - Texto del enlace',
        }
