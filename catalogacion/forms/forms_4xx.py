"""
Formularios para bloque 4XX - Series
"""
from django import forms
from catalogacion.models import (
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
)


class MencionSerie490Form(forms.ModelForm):
    """Formulario para campo 490 - Mención de serie"""
    
    class Meta:
        model = MencionSerie490
        fields = ['relacion']
        widgets = {
            'relacion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'relacion': '490 - Relación con entrada secundaria',
        }
        help_texts = {
            'relacion': '0 = No relacionado / 1 = Relacionado con 800-830',
        }


class TituloSerie490Form(forms.ModelForm):
    """Formulario para campo 490 $a - Título de serie"""
    
    class Meta:
        model = TituloSerie490
        fields = ['titulo_serie']
        widgets = {
            'titulo_serie': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class VolumenSerie490Form(forms.ModelForm):
    """Formulario para campo 490 $v - Volumen"""
    
    class Meta:
        model = VolumenSerie490
        fields = ['volumen']
        widgets = {
            'volumen': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
