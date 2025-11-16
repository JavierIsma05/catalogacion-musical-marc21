"""
Formularios para bloque 7XX - Puntos de acceso adicionales y enlaces
"""
from django import forms
from catalogacion.models import (
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    Relacion700,
    Autoria700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    EnlaceUnidadConstituyente774,
    OtrasRelaciones787,
    AutoridadPersona,
    AutoridadEntidad,
)
from models.auxiliares import EncabezamientoEnlace
from .widgets import Select2Widget, TextAreaAutosize


class NombreRelacionado700Form(forms.ModelForm):
    """Formulario para campo 700 - Nombre relacionado (contenedor)"""
    
    class Meta:
        model = NombreRelacionado700
        fields = ['persona']
        widgets = {
            'persona': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
                'data-placeholder': 'Buscar persona (700 $a)',
            }),
        }
        labels = {
            'persona': '700 $a - Nombre relacionado',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['persona'].queryset = AutoridadPersona.objects.filter(
            activo=True
        ).order_by('apellidos_nombres')


class TerminoAsociado700Form(forms.ModelForm):
    """Formulario para campo 700 $t - Título asociado"""
    
    class Meta:
        model = TerminoAsociado700
        fields = ['titulo_asociado']
        widgets = {
            'titulo_asociado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '700 $t - Título de la obra',
            }),
        }


class Funcion700Form(forms.ModelForm):
    """Formulario para campo 700 $e - Función"""
    
    class Meta:
        model = Funcion700
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'funcion': '700 $e - Término de función',
        }


class Relacion700Form(forms.ModelForm):
    """Formulario para campo 700 $i - Información de relación"""
    
    class Meta:
        model = Relacion700
        fields = ['informacion_relacion']
        widgets = {
            'informacion_relacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '700 $i - Información de relación',
            }),
        }


class Autoria700Form(forms.ModelForm):
    """Formulario para campo 700 $j - Autoría"""
    
    class Meta:
        model = Autoria700
        fields = ['autoria']
        widgets = {
            'autoria': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'autoria': '700 $j - Término de autoría',
        }


class EntidadRelacionada710Form(forms.ModelForm):
    """Formulario para campo 710 - Entidad corporativa"""
    
    class Meta:
        model = EntidadRelacionada710
        fields = ['entidad', 'funcion']
        widgets = {
            'entidad': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/entidad/',
                'data-placeholder': 'Buscar entidad (710 $a)',
            }),
            'funcion': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'entidad': '710 $a - Nombre de entidad',
            'funcion': '710 $e - Función de la entidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entidad'].queryset = AutoridadEntidad.objects.filter(
            activo=True
        ).order_by('nombre')


class EnlaceDocumentoFuente773Form(forms.ModelForm):
    """Formulario para campo 773 - Documento fuente (colección padre)"""
    
    class Meta:
        model = EnlaceDocumentoFuente773
        fields = ['titulo_fuente', 'numero_obra']
        widgets = {
            'titulo_fuente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '773 $t - Título de la colección',
            }),
            'numero_obra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '773 $g - Número de obra dentro de la colección',
            }),
        }
        labels = {
            'titulo_fuente': '773 $t - Título de documento fuente',
            'numero_obra': '773 $g - Número de obra',
        }
    
    # Campo adicional para el encabezamiento polimórfico
    encabezamiento_tipo = forms.ChoiceField(
        choices=[
            ('persona', 'Persona (Compositor)'),
            ('titulo', 'Título Uniforme'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo de encabezamiento',
        required=False,
    )
    
    encabezamiento_persona = forms.ModelChoiceField(
        queryset=AutoridadPersona.objects.filter(activo=True),
        required=False,
        widget=Select2Widget(attrs={
            'data-url': '/catalogacion/autocompletar/persona/',
            'data-placeholder': '773 $a - Compositor de la colección',
        }),
        label='773 $a - Compositor',
    )
    
    encabezamiento_titulo = forms.ModelChoiceField(
        queryset=AutoridadPersona.objects.none(),  # Se configura en __init__
        required=False,
        widget=Select2Widget(attrs={
            'data-url': '/catalogacion/autocompletar/titulo-uniforme/',
            'data-placeholder': '773 $s - Título uniforme de la colección',
        }),
        label='773 $s - Título uniforme',
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from catalogacion.models import AutoridadTituloUniforme
        
        self.fields['encabezamiento_titulo'].queryset = AutoridadTituloUniforme.objects.filter(
            activo=True
        ).order_by('titulo')
        
        # Si existe una instancia, cargar el encabezamiento actual
        if self.instance.pk and hasattr(self.instance, 'encabezamiento'):
            encabezamiento = self.instance.encabezamiento
            if encabezamiento:
                if encabezamiento.content_type.model == 'autoridadpersona':
                    self.fields['encabezamiento_tipo'].initial = 'persona'
                    self.fields['encabezamiento_persona'].initial = encabezamiento.content_object
                elif encabezamiento.content_type.model == 'autoridadtitulouniforme':
                    self.fields['encabezamiento_tipo'].initial = 'titulo'
                    self.fields['encabezamiento_titulo'].initial = encabezamiento.content_object
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('encabezamiento_tipo')
        
        if tipo == 'persona' and not cleaned_data.get('encabezamiento_persona'):
            raise forms.ValidationError({
                'encabezamiento_persona': 'Debe seleccionar un compositor.'
            })
        elif tipo == 'titulo' and not cleaned_data.get('encabezamiento_titulo'):
            raise forms.ValidationError({
                'encabezamiento_titulo': 'Debe seleccionar un título uniforme.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Crear/actualizar el encabezamiento polimórfico
        tipo = self.cleaned_data.get('encabezamiento_tipo')
        
        if tipo == 'persona':
            persona = self.cleaned_data.get('encabezamiento_persona')
            if persona:
                encabezamiento, created = EncabezamientoEnlace.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(persona),
                    object_id=persona.pk
                )
                instance.encabezamiento = encabezamiento
        elif tipo == 'titulo':
            titulo = self.cleaned_data.get('encabezamiento_titulo')
            if titulo:
                from django.contrib.contenttypes.models import ContentType
                encabezamiento, created = EncabezamientoEnlace.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(titulo),
                    object_id=titulo.pk
                )
                instance.encabezamiento = encabezamiento
        
        if commit:
            instance.save()
        
        return instance


class EnlaceUnidadConstituyente774Form(forms.ModelForm):
    """Formulario para campo 774 - Unidad constituyente (obra contenida)"""
    
    class Meta:
        model = EnlaceUnidadConstituyente774
        fields = ['titulo_unidad', 'numero_obra']
        widgets = {
            'titulo_unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '774 $t - Título de la obra contenida',
            }),
            'numero_obra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '774 $g - Número de obra',
            }),
        }
        labels = {
            'titulo_unidad': '774 $t - Título de unidad constituyente',
            'numero_obra': '774 $g - Número de obra',
        }


class OtrasRelaciones787Form(forms.ModelForm):
    """Formulario para campo 787 - Otras relaciones"""
    
    class Meta:
        model = OtrasRelaciones787
        fields = ['informacion_relacion', 'titulo_relacionado']
        widgets = {
            'informacion_relacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '787 $i - Información de relación',
            }),
            'titulo_relacionado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '787 $t - Título relacionado',
            }),
        }
        labels = {
            'informacion_relacion': '787 $i - Tipo de relación',
            'titulo_relacionado': '787 $t - Título',
        }
