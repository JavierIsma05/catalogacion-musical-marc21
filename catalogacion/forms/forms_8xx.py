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
from .widgets import Select2Widget


# ============================================================
# 852 – Ubicación
# ============================================================

class Ubicacion852Form(forms.ModelForm):
    class Meta:
        model = Ubicacion852
        fields = ['codigo_o_nombre', 'signatura_original']
        widgets = {
            'codigo_o_nombre': forms.TextInput(attrs={
                'class': 'form-control autoridad852-autocomplete',
                'placeholder': 'Buscar institución/persona o escribir código…',
                'autocomplete': 'off',
            }),
            'signatura_original': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Archivo Histórico – Caja 3, Carpeta 7'
            }),
        }
        labels = {
            'codigo_o_nombre': '852 $a — Institución / persona / código',
            'signatura_original': '852 $h — Signatura original',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_o_nombre'].required = False
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
    dummy = forms.CharField(required=False, widget=forms.HiddenInput(), initial="1")

    class Meta:
        model = Disponible856
        fields = ["dummy"]



class URL856Form(forms.ModelForm):
    """
    856 $u – URL
    (si algún día quieres manejar las URLs con formsets Django
    en vez de 100% JavaScript)
    """
    class Meta:
        model = URL856
        fields = ["url"]
        widgets = {
            "url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://ejemplo.com/recurso",
            })
        }
        labels = {
            "url": "856 $u — URL",
        }


class TextoEnlace856Form(forms.ModelForm):
    """
    856 $y – Texto del enlace
    """
    class Meta:
        model = TextoEnlace856
        fields = ["texto_enlace"]
        widgets = {
            "texto_enlace": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Texto descriptivo del enlace",
            })
        }
        labels = {
            "texto_enlace": "856 $y — Texto del enlace",
        }
