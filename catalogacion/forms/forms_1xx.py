"""
Formularios para bloque 1XX - Puntos de acceso principales
"""
from django import forms
from catalogacion.models import FuncionCompositor


class FuncionCompositorForm(forms.ModelForm):
    """Formulario para campo 100 $e - Función del compositor"""
    
    class Meta:
        model = FuncionCompositor
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'funcion': '100 $e - Función del compositor',
        }
