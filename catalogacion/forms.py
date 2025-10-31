from django import forms
from django.forms.widgets import Select
from .models import (
    ObraGeneral, 
    AutoridadPersona, 
    AutoridadTituloUniforme, 
    AutoridadFormaMusical,
    TituloAlternativo,  # ✅ Campo 246
    Edicion,  # ✅ Campo 250
    ProduccionPublicacion,  # ✅ Campo 264
    DescripcionFisica  # ✅ Campo 300
)

# ================================================
# 📋 FORMSETS PARA CAMPOS REPETIBLES
# ================================================

TituloAlternativoFormSet = forms.inlineformset_factory(
    ObraGeneral,
    TituloAlternativo,
    fields=['titulo', 'resto_titulo'],
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True,
    widgets={
        'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título alternativo'}),
        'resto_titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resto del título variante'}),
    }
)

EdicionFormSet = forms.inlineformset_factory(
    ObraGeneral,
    Edicion,
    fields=['edicion'],
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True,
    widgets={
        'edicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2a ed., Primera edición'}),
    }
)

ProduccionPublicacionFormSet = forms.inlineformset_factory(
    ObraGeneral,
    ProduccionPublicacion,
    fields=['funcion', 'lugar', 'nombre_entidad', 'fecha', 'orden'],
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True,
    widgets={
        'funcion': forms.Select(attrs={'class': 'form-select'}),
        'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Quito, Madrid'}),
        'nombre_entidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del productor/editor'}),
        'fecha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2023, ©2020'}),
        'orden': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
    }
)

DescripcionFisicaFormSet = forms.inlineformset_factory(
    ObraGeneral,
    DescripcionFisica,
    fields=['extension', 'otras_caracteristicas_fisicas'],
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True,
    widgets={
        'extension': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1 partitura (24 p.)'}),
        'otras_caracteristicas_fisicas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ilustraciones'}),
    }
)

# Widget personalizado para Select2 con tagging
class Select2TaggingWidget(Select):
    """Widget Select que permite tanto seleccionar como crear nuevos valores"""
    
    def __init__(self, attrs=None, choices=()):
        default_attrs = {'class': 'form-control select2-tagging'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, choices)


class ObraForm(forms.ModelForm):
    """
    Formulario principal para catalogación de obras musicales MARC 21
    """
    
    # ================================================
    # 🎯 CAMPOS CON SELECT2
    # ================================================
    
    compositor_select = forms.CharField(
        max_length=200,
        required=False,
        label='Compositor (100 $a)',
        help_text='Apellidos, Nombres. Escriba o seleccione de la lista.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_compositor_select',
            'data-model': 'compositor',
            'placeholder': 'Escriba o seleccione un compositor'
        })
    )
    
    compositor_fechas = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1876-1935',
            'id': 'id_compositor_fechas'
        }),
        label='Fechas del compositor (100 $d)',
        help_text='Año nacimiento - año muerte'
    )
    
    titulo_uniforme_130 = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_titulo_uniforme_130',
            'data-model': 'titulo_uniforme',
            'placeholder': 'Escriba o seleccione un título uniforme'
        }),
        label='Título uniforme (130 $a)',
        help_text='Escriba o seleccione de la lista (cruzar con 240)'
    )
    
    titulo_uniforme_130_forma = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_titulo_uniforme_130_forma',
            'data-model': 'forma_musical',
            'placeholder': 'Ej: Pasillo, Sinfonía, Vals'
        }),
        label='Forma musical (130 $k)',
        help_text='Escriba o seleccione (cruzar con 240 $k y 655)'
    )
    
    titulo_240_select = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_titulo_240_select',
            'data-model': 'titulo_uniforme',
            'placeholder': 'Escriba o seleccione un título uniforme'
        }),
        label='Título uniforme (240 $a)',
        help_text='Escriba o seleccione de la lista (cruzar con 130)'
    )
    
    titulo_240_forma_select = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_titulo_240_forma_select',
            'data-model': 'forma_musical',
            'placeholder': 'Ej: Pasillo, Sinfonía, Vals'
        }),
        label='Forma musical (240 $k)',
        help_text='Escriba o seleccione (cruzar con 130 $k y 655)'
    )
    
    class Meta:
        model = ObraGeneral
        fields = [
            'tipo_registro', 
            'nivel_bibliografico',
            'isbn', 
            'ismn', 
            'numero_editor', 
            'indicador_028',
            'incipit_num_obra', 
            'incipit_num_movimiento', 
            'incipit_num_pasaje',
            'incipit_titulo', 
            'incipit_voz_instrumento', 
            'incipit_notacion', 
            'incipit_url',
            'centro_catalogador', 
            'codigo_lengua', 
            'codigo_pais',
            'clasif_institucion', 
            'clasif_proyecto', 
            'clasif_pais', 
            'clasif_ms_imp',
            'compositor_funcion', 
            'compositor_autoria',
            'titulo_uniforme_medio_interpretacion', 
            'titulo_uniforme_num_parte',
            'titulo_uniforme_arreglo', 
            'titulo_uniforme_nombre_parte',
            'titulo_uniforme_tonalidad',
            'titulo_240_medio_interpretacion', 
            'titulo_240_num_parte',
            'titulo_240_arreglo', 
            'titulo_240_nombre_parte', 
            'titulo_240_tonalidad',
            'titulo_principal', 
            'subtitulo', 
            'mencion_responsabilidad',
        ]
        
        widgets = {
            'tipo_registro': forms.Select(attrs={'class': 'form-select'}),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'ismn': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_editor': forms.TextInput(attrs={'class': 'form-control'}),
            'indicador_028': forms.TextInput(attrs={'class': 'form-control', 'value': '20'}),
            'incipit_num_obra': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'incipit_num_movimiento': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'incipit_num_pasaje': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'incipit_titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'incipit_voz_instrumento': forms.TextInput(attrs={'class': 'form-control'}),
            'incipit_notacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'incipit_url': forms.URLInput(attrs={'class': 'form-control'}),
            'centro_catalogador': forms.TextInput(attrs={'class': 'form-control', 'value': 'UNL'}),
            'codigo_lengua': forms.Select(attrs={'class': 'form-select'}),
            'codigo_pais': forms.Select(attrs={'class': 'form-select'}),
            'clasif_institucion': forms.TextInput(attrs={'class': 'form-control', 'value': 'UNL'}),
            'clasif_proyecto': forms.TextInput(attrs={'class': 'form-control', 'value': 'BLMP'}),
            'clasif_pais': forms.TextInput(attrs={'class': 'form-control', 'value': 'EC'}),
            'clasif_ms_imp': forms.Select(attrs={'class': 'form-select'}),
            'compositor_funcion': forms.Select(attrs={'class': 'form-select'}),
            'compositor_autoria': forms.Select(attrs={'class': 'form-select'}),
            'titulo_uniforme_medio_interpretacion': forms.TextInput(attrs={'class': 'form-control', 'value': 'piano'}),
            'titulo_uniforme_num_parte': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_uniforme_arreglo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_uniforme_nombre_parte': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_uniforme_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            'titulo_240_medio_interpretacion': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_240_num_parte': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_240_arreglo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_240_nombre_parte': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_240_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            'titulo_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mencion_responsabilidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es edición, cargar los valores
        if self.instance and self.instance.pk:
            if self.instance.compositor:
                self.fields['compositor_select'].initial = self.instance.compositor.apellidos_nombres
                self.fields['compositor_fechas'].initial = self.instance.compositor.fechas
            
            if self.instance.titulo_uniforme:
                self.fields['titulo_uniforme_130'].initial = self.instance.titulo_uniforme.titulo
            
            if self.instance.titulo_uniforme_forma:
                self.fields['titulo_uniforme_130_forma'].initial = self.instance.titulo_uniforme_forma.forma
            
            if self.instance.titulo_240:
                self.fields['titulo_240_select'].initial = self.instance.titulo_240.titulo
            
            if self.instance.titulo_240_forma:
                self.fields['titulo_240_forma_select'].initial = self.instance.titulo_240_forma.forma
    
    def clean(self):
        cleaned_data = super().clean()
        
        compositor = cleaned_data.get('compositor_select')
        titulo_130 = cleaned_data.get('titulo_uniforme_130')
        titulo_240 = cleaned_data.get('titulo_240_select')
        
        if not compositor and not titulo_130:
            raise forms.ValidationError(
                "Debe tener un punto de acceso principal: compositor (100) o título uniforme (130)"
            )
        
        if compositor and titulo_130:
            raise forms.ValidationError(
                "Si hay compositor (campo 100), debe usar campo 240, no 130"
            )
        
        if not compositor and titulo_240:
            raise forms.ValidationError(
                "Si no hay compositor, debe usar campo 130, no 240"
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Crear o buscar compositor
        compositor_nombre = self.cleaned_data.get('compositor_select')
        if compositor_nombre:
            compositor_fechas = self.cleaned_data.get('compositor_fechas', '')
            autoridad_persona, created = AutoridadPersona.objects.get_or_create(
                apellidos_nombres=compositor_nombre.strip(),
                defaults={'fechas': compositor_fechas}
            )
            if not created and compositor_fechas and autoridad_persona.fechas != compositor_fechas:
                autoridad_persona.fechas = compositor_fechas
                autoridad_persona.save()
            instance.compositor = autoridad_persona
        else:
            instance.compositor = None
        
        # Crear o buscar título uniforme 130
        titulo_130 = self.cleaned_data.get('titulo_uniforme_130')
        if titulo_130:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=titulo_130.strip()
            )
            instance.titulo_uniforme = autoridad_titulo
        else:
            instance.titulo_uniforme = None
        
        # Crear o buscar forma musical 130
        forma_130 = self.cleaned_data.get('titulo_uniforme_130_forma')
        if forma_130:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=forma_130.strip()
            )
            instance.titulo_uniforme_forma = autoridad_forma
        else:
            instance.titulo_uniforme_forma = None
        
        # Crear o buscar título 240
        titulo_240 = self.cleaned_data.get('titulo_240_select')
        if titulo_240:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=titulo_240.strip()
            )
            instance.titulo_240 = autoridad_titulo
        else:
            instance.titulo_240 = None
        
        # Crear o buscar forma musical 240
        forma_240 = self.cleaned_data.get('titulo_240_forma_select')
        if forma_240:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=forma_240.strip()
            )
            instance.titulo_240_forma = autoridad_forma
        else:
            instance.titulo_240_forma = None
        
        if commit:
            instance.save()
        
        return instance
