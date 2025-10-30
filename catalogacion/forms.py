from django import forms
from .models import (
    ObraGeneral, 
    AutoridadPersona, 
    AutoridadTituloUniforme, 
    AutoridadFormaMusical,
    AutoridadMateria
)


class ObraForm(forms.ModelForm):
    """
    Formulario principal para catalogación de obras musicales MARC21
    Incluye funcionalidad para crear autoridades al vuelo
    """
    
    # ------------------------------------------------
    # 🆕 CAMPOS ADICIONALES PARA CREAR NUEVAS AUTORIDADES
    # ------------------------------------------------
    
    # Para crear nuevo compositor si no existe
    nuevo_compositor_apellidos_nombres = forms.CharField(
        max_length=200,
        required=False,
        label="Nuevo compositor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos, Nombres (si no está en la lista)'
        }),
        help_text="Solo si el compositor NO está en la lista desplegable de arriba"
    )
    
    nuevo_compositor_fechas = forms.CharField(
        max_length=50,
        required=False,
        label="Fechas del nuevo compositor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1876-1935'
        }),
        help_text="Coordenadas biográficas del nuevo compositor"
    )
    
    # Para crear nuevo título uniforme si no existe
    nuevo_titulo_uniforme = forms.CharField(
        max_length=300,
        required=False,
        label="Nuevo título uniforme (130)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si no está en la lista, escríbalo aquí'
        }),
        help_text="Solo si el título NO está en la lista desplegable"
    )
    
    # Para crear nuevo título 240 si no existe
    nuevo_titulo_240 = forms.CharField(
        max_length=300,
        required=False,
        label="Nuevo título uniforme (240)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si no está en la lista, escríbalo aquí'
        }),
        help_text="Solo si el título NO está en la lista desplegable"
    )
    
    # Para crear nueva forma musical si no existe
    nueva_forma_130 = forms.CharField(
        max_length=100,
        required=False,
        label="Nueva forma musical (130 $k)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pasillo, Vals, Sonata'
        }),
        help_text="Solo si la forma NO está en la lista"
    )
    
    nueva_forma_240 = forms.CharField(
        max_length=100,
        required=False,
        label="Nueva forma musical (240 $k)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pasillo, Vals, Sonata'
        }),
        help_text="Solo si la forma NO está en la lista"
    )
    
    class Meta:
        model = ObraGeneral
        fields = [
            # CABECERA
            'tipo_registro', 'nivel_bibliografico',
            
            # Bloque 0XX
            'isbn', 'ismn', 'numero_editor', 'indicador_028',
            'incipit_num_obra', 'incipit_num_movimiento', 'incipit_num_pasaje',
            'incipit_titulo', 'incipit_voz_instrumento', 'incipit_notacion', 'incipit_url',
            'centro_catalogador', 'codigo_lengua', 'codigo_pais',
            'clasif_institucion', 'clasif_proyecto', 'clasif_pais', 'clasif_ms_imp',
            
            # Bloque 1XX
            'compositor', 'compositor_funcion', 'compositor_autoria',
            'titulo_uniforme', 'titulo_uniforme_forma',
            'titulo_uniforme_medio_interpretacion', 'titulo_uniforme_num_parte',
            'titulo_uniforme_arreglo', 'titulo_uniforme_nombre_parte',
            'titulo_uniforme_tonalidad',
            
            # Bloque 2XX
            'titulo_240', 'titulo_240_forma',
            'titulo_240_medio_interpretacion', 'titulo_240_num_parte',
            'titulo_240_arreglo', 'titulo_240_nombre_parte', 'titulo_240_tonalidad',
            'titulo_principal', 'resto_titulo', 'mencion_responsabilidad',
            'numero_parte_245', 'nombre_parte_245',
            'titulo_variante', 'resto_titulo_variante',
            'presentacion_musical',
            'lugar_publicacion', 'nombre_editor', 'fecha_publicacion',
            'extension', 'otros_detalles_fisicos', 'dimensiones', 'material_acompanante'
        ]
        
        widgets = {
            # CABECERA
            'tipo_registro': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo_registro'
            }),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            
            # Bloque 0XX
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 978-3-16-148410-0'
            }),
            'ismn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: M-2306-7118-7'
            }),
            'numero_editor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de plancha o código'
            }),
            'indicador_028': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '20'
            }),
            'incipit_num_obra': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_num_movimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_num_pasaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del íncipit'
            }),
            'incipit_voz_instrumento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: soprano, violín'
            }),
            'incipit_notacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notación musical codificada'
            }),
            'incipit_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'centro_catalogador': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'codigo_lengua': forms.Select(attrs={'class': 'form-select'}),
            'codigo_pais': forms.Select(attrs={'class': 'form-select'}),
            'clasif_institucion': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_proyecto': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_pais': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_ms_imp': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_clasif_ms_imp'
            }),
            
            # Bloque 1XX - CAMPOS CON AUTORIDADES
            'compositor': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un compositor existente'
            }),
            'compositor_funcion': forms.Select(attrs={'class': 'form-select'}),
            'compositor_autoria': forms.Select(attrs={'class': 'form-select'}),
            
            'titulo_uniforme': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un título existente'
            }),
            'titulo_uniforme_forma': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione una forma musical'
            }),
            'titulo_uniforme_medio_interpretacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'piano (predeterminado)'
            }),
            'titulo_uniforme_num_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: no. 1'
            }),
            'titulo_uniforme_arreglo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'arreglo'
            }),
            'titulo_uniforme_nombre_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la parte'
            }),
            'titulo_uniforme_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            
            # Bloque 2XX - CAMPOS CON AUTORIDADES
            'titulo_240': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un título existente'
            }),
            'titulo_240_forma': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione una forma musical'
            }),
            'titulo_240_medio_interpretacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'piano (predeterminado)'
            }),
            'titulo_240_num_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: no. 1'
            }),
            'titulo_240_arreglo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'arreglo'
            }),
            'titulo_240_nombre_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la parte'
            }),
            'titulo_240_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            
            'titulo_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título principal de la obra'
            }),
            'resto_titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subtítulo o complemento'
            }),
            'mencion_responsabilidad': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Autor, compositor, etc.'
            }),
            'numero_parte_245': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de parte'
            }),
            'nombre_parte_245': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de parte'
            }),
            'titulo_variante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título alternativo'
            }),
            'resto_titulo_variante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resto del título variante'
            }),
            'presentacion_musical': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: partitura, partes'
            }),
            'lugar_publicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Quito, Madrid'
            }),
            'nombre_editor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la editorial'
            }),
            'fecha_publicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2023'
            }),
            'extension': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 partitura (24 p.)'
            }),
            'otros_detalles_fisicos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ilustraciones'
            }),
            'dimensiones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 30 cm'
            }),
            'material_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 CD-ROM'
            }),
        }
        
        help_texts = {
            'isbn': '020 $a – ISBN tal como aparece en la fuente',
            'ismn': '024 $a – ISMN para obras impresas desde 1993 aprox.',
            'numero_editor': '028 $a – Número de plancha, placa o código del editor',
            'compositor': '100 $a y $d – Compositor principal (cruzar con 600, 700)',
            'titulo_uniforme': '130 $a – Título uniforme normalizado (cruzar con 240)',
            'titulo_uniforme_forma': '130 $k – Forma musical (cruzar con 240 $k y 655)',
            'titulo_240': '240 $a – Título uniforme cuando hay compositor (cruzar con 130)',
            'titulo_240_forma': '240 $k – Forma musical (cruzar con 130 $k y 655)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ------------------------------------------------
        # Configurar querysets de campos con autoridades
        # ------------------------------------------------
        
        # Campo 100: Compositor (cruzar con 600, 700)
        self.fields['compositor'].queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')
        self.fields['compositor'].required = False
        self.fields['compositor'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 130: Título uniforme (cruzar con 240)
        self.fields['titulo_uniforme'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        self.fields['titulo_uniforme'].required = False
        self.fields['titulo_uniforme'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 130 $k: Forma (cruzar con 240 $k y 655)
        self.fields['titulo_uniforme_forma'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        self.fields['titulo_uniforme_forma'].required = False
        self.fields['titulo_uniforme_forma'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 240: Título uniforme (MISMA tabla que 130)
        self.fields['titulo_240'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        self.fields['titulo_240'].required = False
        self.fields['titulo_240'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 240 $k: Forma (MISMA tabla que 130 $k)
        self.fields['titulo_240_forma'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        self.fields['titulo_240_forma'].required = False
        self.fields['titulo_240_forma'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
    
    def clean(self):
        """Validaciones personalizadas y creación de autoridades al vuelo"""
        cleaned_data = super().clean()
        
        # ------------------------------------------------
        # 1. COMPOSITOR: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        compositor_existente = cleaned_data.get('compositor')
        nuevo_compositor_nombre = cleaned_data.get('nuevo_compositor_apellidos_nombres')
        nuevo_compositor_fechas = cleaned_data.get('nuevo_compositor_fechas')
        
        if nuevo_compositor_nombre:
            # Crear nueva autoridad de persona
            autoridad_compositor, created = AutoridadPersona.objects.get_or_create(
                apellidos_nombres=nuevo_compositor_nombre,
                defaults={'fechas': nuevo_compositor_fechas or ''}
            )
            cleaned_data['compositor'] = autoridad_compositor
        
        # ------------------------------------------------
        # 2. TÍTULO UNIFORME 130: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        titulo_130_existente = cleaned_data.get('titulo_uniforme')
        nuevo_titulo_130 = cleaned_data.get('nuevo_titulo_uniforme')
        
        if nuevo_titulo_130:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=nuevo_titulo_130
            )
            cleaned_data['titulo_uniforme'] = autoridad_titulo
        
        # ------------------------------------------------
        # 3. FORMA 130: Si escribió una nueva, crearla
        # ------------------------------------------------
        forma_130_existente = cleaned_data.get('titulo_uniforme_forma')
        nueva_forma_130 = cleaned_data.get('nueva_forma_130')
        
        if nueva_forma_130:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=nueva_forma_130
            )
            cleaned_data['titulo_uniforme_forma'] = autoridad_forma
        
        # ------------------------------------------------
        # 4. TÍTULO 240: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        titulo_240_existente = cleaned_data.get('titulo_240')
        nuevo_titulo_240 = cleaned_data.get('nuevo_titulo_240')
        
        if nuevo_titulo_240:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=nuevo_titulo_240
            )
            cleaned_data['titulo_240'] = autoridad_titulo
        
        # ------------------------------------------------
        # 5. FORMA 240: Si escribió una nueva, crearla
        # ------------------------------------------------
        forma_240_existente = cleaned_data.get('titulo_240_forma')
        nueva_forma_240 = cleaned_data.get('nueva_forma_240')
        
        if nueva_forma_240:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=nueva_forma_240
            )
            cleaned_data['titulo_240_forma'] = autoridad_forma
        
        # ------------------------------------------------
        # 6. VALIDACIÓN SEGÚN DOCUMENTO: 100 vs 130/240
        # ------------------------------------------------
        compositor_final = cleaned_data.get('compositor')
        titulo_130_final = cleaned_data.get('titulo_uniforme')
        titulo_240_final = cleaned_data.get('titulo_240')
        
        # Regla: Si hay compositor (100), NO debe haber 130
        if compositor_final and titulo_130_final:
            raise forms.ValidationError(
                "Si hay compositor (campo 100), debe usar campo 240, no campo 130"
            )
        
        # Regla: Si NO hay compositor, NO debe haber 240
        if not compositor_final and titulo_240_final:
            raise forms.ValidationError(
                "Si no hay compositor, debe usar campo 130, no campo 240"
            )
        
        # Debe haber al menos uno: compositor O título uniforme 130
        if not compositor_final and not titulo_130_final:
            raise forms.ValidationError(
                "Debe haber un punto de acceso principal: compositor (100) o título uniforme (130)"
            )
        
        return cleaned_data
from django import forms
from .models import (
    ObraGeneral, 
    AutoridadPersona, 
    AutoridadTituloUniforme, 
    AutoridadFormaMusical,
    AutoridadMateria
)


class ObraForm(forms.ModelForm):
    """
    Formulario principal para catalogación de obras musicales MARC21
    Incluye funcionalidad para crear autoridades al vuelo
    """
    
    # ------------------------------------------------
    # 🆕 CAMPOS ADICIONALES PARA CREAR NUEVAS AUTORIDADES
    # ------------------------------------------------
    
    # Para crear nuevo compositor si no existe
    nuevo_compositor_apellidos_nombres = forms.CharField(
        max_length=200,
        required=False,
        label="Nuevo compositor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos, Nombres (si no está en la lista)'
        }),
        help_text="Solo si el compositor NO está en la lista desplegable de arriba"
    )
    
    nuevo_compositor_fechas = forms.CharField(
        max_length=50,
        required=False,
        label="Fechas del nuevo compositor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1876-1935'
        }),
        help_text="Coordenadas biográficas del nuevo compositor"
    )
    
    # Para crear nuevo título uniforme si no existe
    nuevo_titulo_uniforme = forms.CharField(
        max_length=300,
        required=False,
        label="Nuevo título uniforme (130)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si no está en la lista, escríbalo aquí'
        }),
        help_text="Solo si el título NO está en la lista desplegable"
    )
    
    # Para crear nuevo título 240 si no existe
    nuevo_titulo_240 = forms.CharField(
        max_length=300,
        required=False,
        label="Nuevo título uniforme (240)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si no está en la lista, escríbalo aquí'
        }),
        help_text="Solo si el título NO está en la lista desplegable"
    )
    
    # Para crear nueva forma musical si no existe
    nueva_forma_130 = forms.CharField(
        max_length=100,
        required=False,
        label="Nueva forma musical (130 $k)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pasillo, Vals, Sonata'
        }),
        help_text="Solo si la forma NO está en la lista"
    )
    
    nueva_forma_240 = forms.CharField(
        max_length=100,
        required=False,
        label="Nueva forma musical (240 $k)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pasillo, Vals, Sonata'
        }),
        help_text="Solo si la forma NO está en la lista"
    )
    
    class Meta:
        model = ObraGeneral
        fields = [
            # CABECERA
            'tipo_registro', 'nivel_bibliografico',
            
            # Bloque 0XX
            'isbn', 'ismn', 'numero_editor', 'indicador_028',
            'incipit_num_obra', 'incipit_num_movimiento', 'incipit_num_pasaje',
            'incipit_titulo', 'incipit_voz_instrumento', 'incipit_notacion', 'incipit_url',
            'centro_catalogador', 'codigo_lengua', 'codigo_pais',
            'clasif_institucion', 'clasif_proyecto', 'clasif_pais', 'clasif_ms_imp',
            
            # Bloque 1XX
            'compositor', 'compositor_funcion', 'compositor_autoria',
            'titulo_uniforme', 'titulo_uniforme_forma',
            'titulo_uniforme_medio_interpretacion', 'titulo_uniforme_num_parte',
            'titulo_uniforme_arreglo', 'titulo_uniforme_nombre_parte',
            'titulo_uniforme_tonalidad',
            
            # Bloque 2XX
            'titulo_240', 'titulo_240_forma',
            'titulo_240_medio_interpretacion', 'titulo_240_num_parte',
            'titulo_240_arreglo', 'titulo_240_nombre_parte', 'titulo_240_tonalidad',
            'titulo_principal', 'resto_titulo', 'mencion_responsabilidad',
            'numero_parte_245', 'nombre_parte_245',
            'titulo_variante', 'resto_titulo_variante',
            'presentacion_musical',
            'lugar_publicacion', 'nombre_editor', 'fecha_publicacion',
            'extension', 'otros_detalles_fisicos', 'dimensiones', 'material_acompanante'
        ]
        
        widgets = {
            # CABECERA
            'tipo_registro': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_tipo_registro'
            }),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            
            # Bloque 0XX
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 978-3-16-148410-0'
            }),
            'ismn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: M-2306-7118-7'
            }),
            'numero_editor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de plancha o código'
            }),
            'indicador_028': forms.TextInput(attrs={
                'class': 'form-control',
                'value': '20'
            }),
            'incipit_num_obra': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_num_movimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_num_pasaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'incipit_titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del íncipit'
            }),
            'incipit_voz_instrumento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: soprano, violín'
            }),
            'incipit_notacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notación musical codificada'
            }),
            'incipit_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'centro_catalogador': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'codigo_lengua': forms.Select(attrs={'class': 'form-select'}),
            'codigo_pais': forms.Select(attrs={'class': 'form-select'}),
            'clasif_institucion': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_proyecto': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_pais': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'clasif_ms_imp': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_clasif_ms_imp'
            }),
            
            # Bloque 1XX - CAMPOS CON AUTORIDADES
            'compositor': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un compositor existente'
            }),
            'compositor_funcion': forms.Select(attrs={'class': 'form-select'}),
            'compositor_autoria': forms.Select(attrs={'class': 'form-select'}),
            
            'titulo_uniforme': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un título existente'
            }),
            'titulo_uniforme_forma': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione una forma musical'
            }),
            'titulo_uniforme_medio_interpretacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'piano (predeterminado)'
            }),
            'titulo_uniforme_num_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: no. 1'
            }),
            'titulo_uniforme_arreglo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'arreglo'
            }),
            'titulo_uniforme_nombre_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la parte'
            }),
            'titulo_uniforme_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            
            # Bloque 2XX - CAMPOS CON AUTORIDADES
            'titulo_240': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione un título existente'
            }),
            'titulo_240_forma': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Seleccione una forma musical'
            }),
            'titulo_240_medio_interpretacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'piano (predeterminado)'
            }),
            'titulo_240_num_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: no. 1'
            }),
            'titulo_240_arreglo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'arreglo'
            }),
            'titulo_240_nombre_parte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la parte'
            }),
            'titulo_240_tonalidad': forms.Select(attrs={'class': 'form-select'}),
            
            'titulo_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título principal de la obra'
            }),
            'resto_titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subtítulo o complemento'
            }),
            'mencion_responsabilidad': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Autor, compositor, etc.'
            }),
            'numero_parte_245': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de parte'
            }),
            'nombre_parte_245': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de parte'
            }),
            'titulo_variante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título alternativo'
            }),
            'resto_titulo_variante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resto del título variante'
            }),
            'presentacion_musical': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: partitura, partes'
            }),
            'lugar_publicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Quito, Madrid'
            }),
            'nombre_editor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la editorial'
            }),
            'fecha_publicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2023'
            }),
            'extension': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 partitura (24 p.)'
            }),
            'otros_detalles_fisicos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ilustraciones'
            }),
            'dimensiones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 30 cm'
            }),
            'material_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 CD-ROM'
            }),
        }
        
        help_texts = {
            'isbn': '020 $a – ISBN tal como aparece en la fuente',
            'ismn': '024 $a – ISMN para obras impresas desde 1993 aprox.',
            'numero_editor': '028 $a – Número de plancha, placa o código del editor',
            'compositor': '100 $a y $d – Compositor principal (cruzar con 600, 700)',
            'titulo_uniforme': '130 $a – Título uniforme normalizado (cruzar con 240)',
            'titulo_uniforme_forma': '130 $k – Forma musical (cruzar con 240 $k y 655)',
            'titulo_240': '240 $a – Título uniforme cuando hay compositor (cruzar con 130)',
            'titulo_240_forma': '240 $k – Forma musical (cruzar con 130 $k y 655)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ------------------------------------------------
        # Configurar querysets de campos con autoridades
        # ------------------------------------------------
        
        # Campo 100: Compositor (cruzar con 600, 700)
        self.fields['compositor'].queryset = AutoridadPersona.objects.all().order_by('apellidos_nombres')
        self.fields['compositor'].required = False
        self.fields['compositor'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 130: Título uniforme (cruzar con 240)
        self.fields['titulo_uniforme'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        self.fields['titulo_uniforme'].required = False
        self.fields['titulo_uniforme'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 130 $k: Forma (cruzar con 240 $k y 655)
        self.fields['titulo_uniforme_forma'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        self.fields['titulo_uniforme_forma'].required = False
        self.fields['titulo_uniforme_forma'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 240: Título uniforme (MISMA tabla que 130)
        self.fields['titulo_240'].queryset = AutoridadTituloUniforme.objects.all().order_by('titulo')
        self.fields['titulo_240'].required = False
        self.fields['titulo_240'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
        
        # Campo 240 $k: Forma (MISMA tabla que 130 $k)
        self.fields['titulo_240_forma'].queryset = AutoridadFormaMusical.objects.all().order_by('forma')
        self.fields['titulo_240_forma'].required = False
        self.fields['titulo_240_forma'].empty_label = "-- Seleccione o cree uno nuevo abajo --"
    
    def clean(self):
        """Validaciones personalizadas y creación de autoridades al vuelo"""
        cleaned_data = super().clean()
        
        # ------------------------------------------------
        # 1. COMPOSITOR: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        compositor_existente = cleaned_data.get('compositor')
        nuevo_compositor_nombre = cleaned_data.get('nuevo_compositor_apellidos_nombres')
        nuevo_compositor_fechas = cleaned_data.get('nuevo_compositor_fechas')
        
        if nuevo_compositor_nombre:
            # Crear nueva autoridad de persona
            autoridad_compositor, created = AutoridadPersona.objects.get_or_create(
                apellidos_nombres=nuevo_compositor_nombre,
                defaults={'fechas': nuevo_compositor_fechas or ''}
            )
            cleaned_data['compositor'] = autoridad_compositor
        
        # ------------------------------------------------
        # 2. TÍTULO UNIFORME 130: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        titulo_130_existente = cleaned_data.get('titulo_uniforme')
        nuevo_titulo_130 = cleaned_data.get('nuevo_titulo_uniforme')
        
        if nuevo_titulo_130:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=nuevo_titulo_130
            )
            cleaned_data['titulo_uniforme'] = autoridad_titulo
        
        # ------------------------------------------------
        # 3. FORMA 130: Si escribió una nueva, crearla
        # ------------------------------------------------
        forma_130_existente = cleaned_data.get('titulo_uniforme_forma')
        nueva_forma_130 = cleaned_data.get('nueva_forma_130')
        
        if nueva_forma_130:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=nueva_forma_130
            )
            cleaned_data['titulo_uniforme_forma'] = autoridad_forma
        
        # ------------------------------------------------
        # 4. TÍTULO 240: Si escribió uno nuevo, crearlo
        # ------------------------------------------------
        titulo_240_existente = cleaned_data.get('titulo_240')
        nuevo_titulo_240 = cleaned_data.get('nuevo_titulo_240')
        
        if nuevo_titulo_240:
            autoridad_titulo, created = AutoridadTituloUniforme.objects.get_or_create(
                titulo=nuevo_titulo_240
            )
            cleaned_data['titulo_240'] = autoridad_titulo
        
        # ------------------------------------------------
        # 5. FORMA 240: Si escribió una nueva, crearla
        # ------------------------------------------------
        forma_240_existente = cleaned_data.get('titulo_240_forma')
        nueva_forma_240 = cleaned_data.get('nueva_forma_240')
        
        if nueva_forma_240:
            autoridad_forma, created = AutoridadFormaMusical.objects.get_or_create(
                forma=nueva_forma_240
            )
            cleaned_data['titulo_240_forma'] = autoridad_forma
        
        # ------------------------------------------------
        # 6. VALIDACIÓN SEGÚN DOCUMENTO: 100 vs 130/240
        # ------------------------------------------------
        compositor_final = cleaned_data.get('compositor')
        titulo_130_final = cleaned_data.get('titulo_uniforme')
        titulo_240_final = cleaned_data.get('titulo_240')
        
        # Regla: Si hay compositor (100), NO debe haber 130
        if compositor_final and titulo_130_final:
            raise forms.ValidationError(
                "Si hay compositor (campo 100), debe usar campo 240, no campo 130"
            )
        
        # Regla: Si NO hay compositor, NO debe haber 240
        if not compositor_final and titulo_240_final:
            raise forms.ValidationError(
                "Si no hay compositor, debe usar campo 130, no campo 240"
            )
        
        # Debe haber al menos uno: compositor O título uniforme 130
        if not compositor_final and not titulo_130_final:
            raise forms.ValidationError(
                "Debe haber un punto de acceso principal: compositor (100) o título uniforme (130)"
            )
        
        return cleaned_data
