"""
Formularios para bloque 8XX - Entradas de serie
"""
from django import forms
from catalogacion.models import Serie830
from .widgets import TextAreaAutosize


class Serie830Form(forms.ModelForm):
    """Formulario para campo 830 - Entrada de serie"""
    
    class Meta:
        model = Serie830
        fields = ['titulo_serie', 'volumen']
        widgets = {
            'titulo_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '830 $a - Título uniforme de la serie',
            }),
            'volumen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '830 $v - Designación de volumen',
            }),
        }
        labels = {
            'titulo_serie': '830 $a - Título de la serie',
            'volumen': '830 $v - Volumen',
        }
