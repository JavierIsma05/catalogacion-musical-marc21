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
    AutoridadEntidad,
)
from .widgets import TextAreaAutosize, Select2Widget


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
                'placeholder': 'Ej: Ms-123'
            }),
        }
        labels = {
            'institucion_persona': '852 $a - Institución o persona',
            'signatura_original': '852 $h - Signatura original',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institucion_persona'].queryset = AutoridadEntidad.objects.all().order_by('nombre')
        self.fields['institucion_persona'].required = False
        self.fields['signatura_original'].required = False


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
    Formulario para campo 856 - Disponible
    Los subcampos $u (URL) y $y (texto enlace) se manejan con JavaScript
    """
    
    class Meta:
        model = Disponible856
        fields = []  # Sin campos directos, los subcampos se manejan con JavaScript
    
    def __str__(self):
        return "856 - Recurso disponible"


# Los formularios URL856Form y TextoEnlace856Form no son necesarios
# porque los subcampos se manejan dinámicamente con JavaScript
