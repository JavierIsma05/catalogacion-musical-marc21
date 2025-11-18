"""
Formulario principal para ObraGeneral
Incluye campos del modelo principal (no repetibles)
"""
from django import forms
from catalogacion.models import (
    ObraGeneral,
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadEntidad,
)
from .widgets import Select2Widget, TextAreaAutosize


class ObraGeneralForm(forms.ModelForm):
    """
    Formulario base para ObraGeneral
    Maneja campos no repetibles del modelo principal
    """
    
    # Campos adicionales para autocomplete editable de compositor
    compositor_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione un compositor...',
            'autocomplete': 'off',
        }),
        label='100 $a - Compositor (Apellidos, Nombres)'
    )
    
    compositor_coordenadas = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1900-1980',
        }),
        label='100 $d - Coordenadas biográficas'
    )
    
    # Campos adicionales para autocomplete editable de título uniforme 130
    titulo_uniforme_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione un título uniforme...',
            'autocomplete': 'off',
        }),
        label='130 $a - Título Uniforme'
    )
    
    forma_130_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione una forma musical...',
            'autocomplete': 'off',
        }),
        label='130 $k - Forma Musical'
    )
    
    # Campos adicionales para autocomplete editable de título uniforme 240
    titulo_240_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione un título uniforme...',
            'autocomplete': 'off',
        }),
        label='240 $a - Título Uniforme'
    )
    
    forma_240_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione una forma musical...',
            'autocomplete': 'off',
        }),
        label='240 $k - Forma Musical'
    )
    
    class Meta:
        model = ObraGeneral
        fields = [
            # Leader y control
            'tipo_registro',
            'nivel_bibliografico',
            'centro_catalogador',
            
            # Identificadores (020/024/028)
            'isbn',
            'ismn',
            'tipo_numero_028',
            'control_nota_028',
            'numero_editor',
            
            # Punto de acceso principal (100/130/240)
            'compositor',
            'termino_asociado',
            'autoria',
            'titulo_uniforme',
            'forma_130',
            'medio_interpretacion_130',
            'numero_parte_130',
            'arreglo_130',
            'nombre_parte_130',
            'tonalidad_130',
            'titulo_240',
            'forma_240',
            'medio_interpretacion_240',
            'numero_parte_240',
            'nombre_parte_240',
            'arreglo_240',
            'tonalidad_240',
            
            # Título principal (245)
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
            
            # Descripción física (300)
            'extension',
            'otras_caracteristicas',
            'dimension',
            'material_acompanante',
            
            # Características técnicas (340/348)
            'ms_imp',
            'formato',
            
            # Medio y designación (383/384)
            # NOTA: 382 ($a medios y $b solista) ahora usa MedioInterpretacion382Form
            'numero_obra',
            'opus',
            'tonalidad_384',
        ]
        
        widgets = {
            # Selects con autoridades
            'tipo_registro': forms.HiddenInput(),
            'nivel_bibliografico': forms.HiddenInput(),
            
            'compositor': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'titulo_uniforme': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/titulo-uniforme/',
            }),
            'titulo_240': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/titulo-uniforme/',
            }),
            'forma_130': Select2Widget(attrs={}),
            'forma_240': Select2Widget(attrs={}),
            
            # Selects normales
            'tipo_registro': forms.Select(attrs={'class': 'form-select'}),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            'autoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_numero_028': forms.Select(attrs={'class': 'form-select'}),
            'control_nota_028': forms.Select(attrs={'class': 'form-select'}),
            'medio_interpretacion_130': forms.Select(attrs={'class': 'form-select'}),
            'medio_interpretacion_240': forms.Select(attrs={'class': 'form-select'}),
            'tonalidad_130': forms.Select(attrs={'class': 'form-select'}),
            'tonalidad_240': forms.Select(attrs={'class': 'form-select'}),
            'tonalidad_384': forms.Select(attrs={'class': 'form-select'}),
            'arreglo_130': forms.Select(attrs={'class': 'form-select'}),
            'arreglo_240': forms.Select(attrs={'class': 'form-select'}),
            'ms_imp': forms.Select(attrs={'class': 'form-select'}),
            'formato': forms.Select(attrs={'class': 'form-select'}),
            
            # Inputs de texto
            'centro_catalogador': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'termino_asociado': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ismn': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_editor': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_parte_130': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nombre_parte_130': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_parte_240': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nombre_parte_240': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'titulo_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'extension': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'otras_caracteristicas': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'dimension': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'material_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'numero_obra': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'opus': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
            # TextAreas
            'mencion_responsabilidad': TextAreaAutosize(attrs={}),
        }
        
        labels = {
            'tipo_registro': 'Tipo de registro',
            'nivel_bibliografico': 'Nivel bibliográfico',
            'centro_catalogador': '040 $a - Centro catalogador',
            'isbn': '020 $a - ISBN',
            'ismn': '024 $a - ISMN',
            'tipo_numero_028': '028 - Tipo de número',
            'control_nota_028': '028 - Control de nota',
            'numero_editor': '028 $a - Número de editor',
            'compositor': '100 $a - Compositor',
            'termino_asociado': '100 $c - Término asociado',
            'autoria': '100 $j - Autoría',
            'titulo_uniforme': '130 $a - Título uniforme',
            'forma_130': '130 $k - Forma musical',
            'medio_interpretacion_130': '130 $m - Medio de interpretación',
            'numero_parte_130': '130 $n - Número de parte',
            'nombre_parte_130': '130 $p - Nombre de parte',
            'arreglo_130': '130 $o - Arreglo',
            'tonalidad_130': '130 $r - Tonalidad',
            'titulo_240': '240 $a - Título uniforme',
            'forma_240': '240 $k - Forma musical',
            'medio_interpretacion_240': '240 $m - Medio de interpretación',
            'numero_parte_240': '240 $n - Número de parte',
            'nombre_parte_240': '240 $p - Nombre de parte',
            'arreglo_240': '240 $o - Arreglo',
            'tonalidad_240': '240 $r - Tonalidad',
            'titulo_principal': '245 $a - Título principal *',
            'subtitulo': '245 $b - Subtítulo',
            'mencion_responsabilidad': '245 $c - Nombres en fuente',
            'extension': '300 $a - Extensión',
            'otras_caracteristicas': '300 $b - Otras características físicas',
            'dimension': '300 $c - Dimensiones',
            'material_acompanante': '300 $e - Material acompañante',
            'ms_imp': '340 $d - Técnica',
            'formato': '348 $a - Formato',
            'numero_obra': '383 $a - Número serial de obra',
            'opus': '383 $b - Número de opus',
            'tonalidad_384': '384 $a - Tonalidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar querysets para autoridades
        self.fields['compositor'].queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')
        
        self.fields['titulo_uniforme'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        
        self.fields['titulo_240'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        
        self.fields['forma_130'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        
        self.fields['forma_240'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        
        # Hacer título principal obligatorio
        self.fields['titulo_principal'].required = True
    
    def clean(self):
        """Validación personalizada y creación automática de autoridades"""
        cleaned_data = super().clean()
        
        # Manejar compositor autocomplete editable
        compositor_texto = cleaned_data.get('compositor_texto', '').strip()
        compositor_coordenadas = cleaned_data.get('compositor_coordenadas', '').strip()
        
        if compositor_texto:
            try:
                persona = AutoridadPersona.objects.get(apellidos_nombres__iexact=compositor_texto)
                if compositor_coordenadas and persona.coordenadas_biograficas != compositor_coordenadas:
                    persona.coordenadas_biograficas = compositor_coordenadas
                    persona.save()
                cleaned_data['compositor'] = persona
            except AutoridadPersona.DoesNotExist:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=compositor_texto,
                    coordenadas_biograficas=compositor_coordenadas
                )
                cleaned_data['compositor'] = persona
            except AutoridadPersona.MultipleObjectsReturned:
                persona = AutoridadPersona.objects.filter(
                    apellidos_nombres__iexact=compositor_texto
                ).first()
                cleaned_data['compositor'] = persona
        
        # Manejar título uniforme 130 autocomplete editable
        titulo_uniforme_texto = cleaned_data.get('titulo_uniforme_texto', '').strip()
        if titulo_uniforme_texto:
            titulo, _ = AutoridadTituloUniforme.objects.get_or_create(
                titulo__iexact=titulo_uniforme_texto,
                defaults={'titulo': titulo_uniforme_texto}
            )
            cleaned_data['titulo_uniforme'] = titulo
        
        # Manejar forma musical 130 autocomplete editable
        forma_130_texto = cleaned_data.get('forma_130_texto', '').strip()
        if forma_130_texto:
            forma, _ = AutoridadFormaMusical.objects.get_or_create(
                forma__iexact=forma_130_texto,
                defaults={'forma': forma_130_texto}
            )
            cleaned_data['forma_130'] = forma
        
        # Manejar título uniforme 240 autocomplete editable
        titulo_240_texto = cleaned_data.get('titulo_240_texto', '').strip()
        if titulo_240_texto:
            titulo, _ = AutoridadTituloUniforme.objects.get_or_create(
                titulo__iexact=titulo_240_texto,
                defaults={'titulo': titulo_240_texto}
            )
            cleaned_data['titulo_240'] = titulo
        
        # Manejar forma musical 240 autocomplete editable
        forma_240_texto = cleaned_data.get('forma_240_texto', '').strip()
        if forma_240_texto:
            forma, _ = AutoridadFormaMusical.objects.get_or_create(
                forma__iexact=forma_240_texto,
                defaults={'forma': forma_240_texto}
            )
            cleaned_data['forma_240'] = forma
        
        # Validar punto de acceso principal (100 vs 130)
        compositor = cleaned_data.get('compositor')
        titulo_uniforme = cleaned_data.get('titulo_uniforme')
        
        if compositor and titulo_uniforme:
            raise forms.ValidationError(
                "No puede tener compositor (100) y título uniforme (130) simultáneamente. "
                "Si hay compositor, use el campo 240 para título uniforme."
            )
        
        # Validar campos condicionalessegun tipo de obra
        tipo_registro = cleaned_data.get('tipo_registro')
        
        # Manuscritos no pueden tener ISBN/ISMN
        if tipo_registro == 'd':
            if cleaned_data.get('isbn'):
                raise forms.ValidationError({
                    'isbn': "Los manuscritos no pueden tener ISBN (campo 020)."
                })
            if cleaned_data.get('ismn'):
                raise forms.ValidationError({
                    'ismn': "Los manuscritos no pueden tener ISMN (campo 024)."
                })
        
        return cleaned_data
