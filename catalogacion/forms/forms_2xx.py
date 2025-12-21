"""
Formularios para bloque 2XX - Títulos y publicación
"""
from django import forms
from catalogacion.models import (
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    Lugar264,
    NombreEntidad264,
    Fecha264,
)


class TituloAlternativoForm(forms.ModelForm):
    """Formulario para campo 246 - Título alternativo"""
    
    class Meta:
        model = TituloAlternativo
        fields = ['titulo', 'resto_titulo', 'texto_visualizacion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'resto_titulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'texto_visualizacion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'titulo': '246 $a - Título alternativo',
            'resto_titulo': '246 $b - Resto del título',
            'texto_visualizacion': '246 $i - Texto de visualización',
        }


class EdicionForm(forms.ModelForm):
    """Formulario para campo 250 - Edición"""
    
    class Meta:
        model = Edicion
        fields = ['edicion']
        widgets = {
            'edicion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class ProduccionPublicacionForm(forms.ModelForm):
    """Formulario para campo 264 - Producción/Publicación"""
    
    class Meta:
        model = ProduccionPublicacion
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select no-select2',
                'data-no-select2': '1',
            }),
        }
        labels = {
            'funcion': '264 - Función de la entidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asegurar que este select sea siempre nativo (sin Select2)
        self.fields['funcion'].widget.attrs.update({
            'class': 'form-select no-select2',
            'data-no-select2': '1',
        })

        # Establecer valor inicial para manuscritos (Producción = 0)
        if not self.instance.pk and not self.initial.get('funcion'):
            self.initial['funcion'] = '0'


class Lugar264Form(forms.ModelForm):
    """Formulario para campo 264 $a - Lugar"""
    
    class Meta:
        model = Lugar264
        fields = ['lugar']
        widgets = {
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class NombreEntidad264Form(forms.ModelForm):
    """Formulario para campo 264 $b - Nombre de entidad"""
    
    class Meta:
        model = NombreEntidad264
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class Fecha264Form(forms.ModelForm):
    """Formulario para campo 264 $c - Fecha"""
    
    class Meta:
        model = Fecha264
        fields = ['fecha']
        widgets = {
            'fecha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '264 $c - Fecha de publicación',
            }),
        }
