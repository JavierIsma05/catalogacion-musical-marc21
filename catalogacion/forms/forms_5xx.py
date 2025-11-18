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
            'nota_general': TextAreaAutosize(attrs={}),
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
                'rows': 4,
            }),
        }
        labels = {
            'sumario': '520 $a - Sumario',
        }


class DatosBiograficos545Form(forms.ModelForm):
    """Formulario para campo 545 - Datos biográficos (manejado con JavaScript)"""
    
    class Meta:
        model = DatosBiograficos545
        fields = []  # Campos vacíos, subcampos manejados por JavaScript
