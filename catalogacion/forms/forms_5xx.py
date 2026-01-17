"""
Formularios para bloque 5XX - Notas
"""
from django import forms
from catalogacion.models import (
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
)
from .widgets import TextAreaAutosize


class NotaGeneral500Form(forms.ModelForm):
    """Formulario para campo 500 - Nota general"""
    
    class Meta:
        model = NotaGeneral500
        fields = ['nota_general']
        widgets = {
            'nota_general': TextAreaAutosize(attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: Datos tomados de portada y encabezado de música…',
            }),
        }
        labels = {
            'nota_general': '500 $a - Nota general',
        }


class Contenido505Form(forms.ModelForm):
    """Formulario para campo 505 - Contenido"""
    
    class Meta:
        model = Contenido505
        fields = ['contenido']
        widgets = {
            'contenido': TextAreaAutosize(attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: Emma Mercedes / Alfonso Dolberg. Violetas y rosas. Para llamarte mía / Segundo Cueva Celi…',
                'rows': 5,
            }),
        }
        labels = {
            'contenido': '505 $a - Nota de contenido',
        }


class Sumario520Form(forms.ModelForm):
    """Formulario para campo 520 - Sumario"""
    
    class Meta:
        model = Sumario520
        fields = ['sumario']
        widgets = {
            'sumario': TextAreaAutosize(attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: Allegro, Andante, Vivace…',
                'rows': 4,
            }),
        }
        labels = {
            'sumario': '520 $a - Sumario',
        }

class DatosBiograficos545Form(forms.ModelForm):
    class Meta:
        model = DatosBiograficos545
        fields = ['texto_biografico', 'uri']
        widgets = {
            'texto_biografico': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej.: Teresa Carreño (Caracas, 22/12/1853 – Nueva York, 12/06/1917)…'}
            ),
            'uri': forms.URLInput(
                attrs={'class': 'form-control','placeholder': 'Ej.: https://es.wikipedia.org/wiki/Teresa_Carre%C3%B1o'}
            ),
        }
        labels = {
            'texto_biografico': '545 $a – Datos biográficos',
            'uri': '545 $u – URL',
        }

