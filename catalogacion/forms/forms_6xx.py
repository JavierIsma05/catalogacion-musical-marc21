"""
Formularios para bloque 6XX - Materias
"""
from django import forms
from catalogacion.models import (
    Materia650,
    MateriaGenero655,
    AutoridadMateria,
)
from .widgets import Select2Widget


class Materia650Form(forms.ModelForm):
    """Formulario para campo 650 - Materia"""
    
    class Meta:
        model = Materia650
        fields = ['materia']
        widgets = {
            'materia': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/materia/',
            }),
        }
        labels = {
            'materia': '650 $a - Encabezamiento de materia',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materia'].queryset = AutoridadMateria.objects.all().order_by('termino')


class MateriaGenero655Form(forms.ModelForm):
    """Formulario para campo 655 - Género/Forma"""
    
    class Meta:
        model = MateriaGenero655
        fields = ['materia']
        widgets = {
            'materia': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'materia': '655 $a - Término de género/forma',
        }
