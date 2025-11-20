"""
Formularios para bloque 8XX - Ubicación y disponibilidad
"""
from django import forms
from catalogacion.models import (
    Ubicacion852,
    Estanteria852,
    Disponible856,
    AutoridadEntidad,
)
from .widgets import Select2Widget


# ============================================================
# 852 – Ubicación
# ============================================================

class Ubicacion852Form(forms.ModelForm):
    """
    Formulario para campo 852 - Ubicación
    Incluye $a (institución) y $h (signatura)
    """
    class Meta:
        model = Ubicacion852
        fields = ['institucion_persona', 'signatura_original']
        widgets = {
            'institucion_persona': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/entidad/',
            }),
            'signatura_original': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Archivo Histórico – Caja 3, Carpeta 7'
            }),
        }
        labels = {
            'institucion_persona': '852 $a – Institución o persona',
            'signatura_original': '852 $h – Signatura original',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion_persona'].queryset = AutoridadEntidad.objects.all().order_by('nombre')
        self.fields['institucion_persona'].required = False
        self.fields['signatura_original'].required = False


# ============================================================
# 852 $c – Estantería (R)
# ============================================================

class Estanteria852Form(forms.ModelForm):
    class Meta:
        model = Estanteria852
        fields = ['estanteria']
        widgets = {
            'estanteria': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'estanteria': '852 $c – Estantería',
        }

class Disponible856Form(forms.ModelForm):
    """
    Formulario fantasma usado por el formset.
    No tiene campos porque $u y $y se manejan por JavaScript.
    """
    class Meta:
        model = Disponible856
        fields = []