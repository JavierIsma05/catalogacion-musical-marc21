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
    Incluye URL ($u) y texto del enlace ($y) en un solo formulario
    """
    
    url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://ejemplo.com/recurso'
        }),
        label='856 $u - URL'
    )
    
    texto_enlace = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Texto descriptivo del enlace'
        }),
        label='856 $y - Texto del enlace'
    )
    
    class Meta:
        model = Disponible856
        fields = []  # Los campos reales están definidos arriba
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si existe instancia, cargar los datos de URL y texto
        if self.instance and self.instance.pk:
            primera_url = self.instance.urls_856.first()
            primer_texto = self.instance.textos_enlace_856.first()
            
            if primera_url:
                self.fields['url'].initial = primera_url.url
            if primer_texto:
                self.fields['texto_enlace'].initial = primer_texto.texto_enlace
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        if commit:
            # Guardar URL si se proporcionó
            url_value = self.cleaned_data.get('url')
            if url_value:
                # Eliminar URLs antiguas y crear nueva
                instance.urls_856.all().delete()
                URL856.objects.create(disponible=instance, url=url_value)
            
            # Guardar texto de enlace si se proporcionó
            texto_value = self.cleaned_data.get('texto_enlace')
            if texto_value:
                # Eliminar textos antiguos y crear nuevo
                instance.textos_enlace_856.all().delete()
                TextoEnlace856.objects.create(disponible=instance, texto_enlace=texto_value)
        
        return instance
    
    def __str__(self):
        return "856 - Recurso disponible"


class URL856Form(forms.ModelForm):
    """Formulario para campo 856 $u - URL"""
    
    class Meta:
        model = URL856
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'url': '856 $u - URL',
        }


class TextoEnlace856Form(forms.ModelForm):
    """Formulario para campo 856 $y - Texto del enlace"""
    
    class Meta:
        model = TextoEnlace856
        fields = ['texto_enlace']
        widgets = {
            'texto_enlace': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'texto_enlace': '856 $y - Texto del enlace',
        }
