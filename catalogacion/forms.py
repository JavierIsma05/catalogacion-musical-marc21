
from django import forms
from django.forms.widgets import SelectMultiple, CheckboxSelectMultiple
from django.core.exceptions import ValidationError

from .models import (
    # Bloque 0XX
    ISBN,
    ISMN,
    NumeroEditor,
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
    # Bloque 1XX
    FuncionCompositor,
    AtribucionCompositor,
    Forma130,
    MedioInterpretacion130,
    NumeroParteSección130,
    NombreParteSección130,
    Forma240,
    MedioInterpretacion240,
    NumeroParteSección240,
    NombreParteSección240,
    # Bloque 2XX
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    # Bloque 3XX
    DescripcionFisica,
    Extension300,
    Dimension300,
    MedioFisico,
    Tecnica340,
    CaracteristicaMusicaNotada,
    Formato348,
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    Solista382,
    NumeroInterpretes382,
    DesignacionNumericaObra,
    NumeroObra383,
    Opus383,
    # Bloque 4XX
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
    # Bloque 5XX
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
    # Bloque 6XX
    Materia650,
    SubdivisionMateria650,
    MateriaGenero655,
    SubdivisionGeneral655,
    # Principal
    ObraGeneral,
    AutoridadPersona,
    AutoridadTituloUniforme,
)

# ============================================================
# 📋 BLOQUE 0XX - CAMPOS DE CONTROL
# ============================================================

class ISBNForm(forms.ModelForm):
    """Formulario para ISBN (020 $a) - Repetible"""
    class Meta:
        model = ISBN
        fields = ['isbn']
        widgets = {
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '020 $a - ISBN (ej: 978-3-16-148410-0)',
                'pattern': '[0-9\-]{10,}',
                'title': 'Ingrese un ISBN válido'
            })
        }


# ISMNFormSet - FormSet para ISMN (024 $a) - Repetible
ISMNFormSet = forms.inlineformset_factory(
    ObraGeneral,
    ISMN,
    fields=['ismn'],
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True,
    widgets={
        'ismn': forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': '024 $a - ISMN'
        })
    }
)


class NumeroEditorForm(forms.ModelForm):
    """Formulario para Número de Editor (028) - Repetible"""
    class Meta:
        model = NumeroEditor
        fields = ['numero', 'tipo_numero', 'control_nota']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '028 $a - Número de editor'
            }),
            'tipo_numero': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'control_nota': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }


class IncipitMusicalForm(forms.ModelForm):
    """Formulario para Íncipit Musical (031) - Repetible"""
    class Meta:
        model = IncipitMusical
        fields = [
            'numero_obra', 'numero_movimiento', 'numero_pasaje',
            'titulo_encabezamiento', 'voz_instrumento', 'notacion_musical'
        ]
        widgets = {
            'numero_obra': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '031 $a - Número de obra'
            }),
            'numero_movimiento': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '031 $b - Número de movimiento'
            }),
            'numero_pasaje': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '031 $c - Número de pasaje'
            }),
            'titulo_encabezamiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $d - Título/encabezamiento (ej: Aria, Allegro)'
            }),
            'voz_instrumento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $m - Voz/instrumento'
            }),
            'notacion_musical': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '031 $p - Notación musical codificada'
            })
        }


class IncipitURLForm(forms.ModelForm):
    """Formulario para URL de Íncipit (031 $u) - Repetible"""
    class Meta:
        model = IncipitURL
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '031 $u - URL del íncipit'
            })
        }


IncipitURLFormSet = forms.inlineformset_factory(
    IncipitMusical,
    IncipitURL,
    form=IncipitURLForm,
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True
)


class IdiomaObraForm(forms.ModelForm):
    """Formulario para Idioma de Obra (041 $a) - Repetible"""
    class Meta:
        model = IdiomaObra
        fields = ['codigo']
        widgets = {
            'codigo': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            })
        }


IdiomaObraFormSet = forms.inlineformset_factory(
    CodigoLengua,
    IdiomaObra,
    form=IdiomaObraForm,
    extra=1,
    min_num=1,
    max_num=10,
    can_delete=True
)


class CodigoLenguaForm(forms.ModelForm):
    """Formulario para Código de Lengua (041) - Principal"""
    class Meta:
        model = CodigoLengua
        fields = ['indicacion_traduccion', 'fuente_codigo', 'fuente_especificada']
        widgets = {
            'indicacion_traduccion': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'fuente_codigo': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'fuente_especificada': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '041 $2 - Fuente del código'
            })
        }


CodigoPaisEntidadFormSet = forms.inlineformset_factory(
    ObraGeneral,
    CodigoPaisEntidad,
    fields=['codigo_pais'],
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True,
    widgets={
        'codigo_pais': forms.Select(attrs={
            'class': 'form-select form-select-sm'
        })
    }
)

# ============================================================
# 📋 BLOQUE 1XX - PUNTOS DE ACCESO
# ============================================================

class FuncionCompositorForm(forms.ModelForm):
    """100 $e - Función del compositor (R)"""
    class Meta:
        model = FuncionCompositor
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select'
            })
        }


FuncionCompositorFormSet = forms.inlineformset_factory(
    ObraGeneral,
    FuncionCompositor,
    form=FuncionCompositorForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class AtribucionCompositorForm(forms.ModelForm):
    """100 $j - Atribución del compositor (R)"""
    class Meta:
        model = AtribucionCompositor
        fields = ['atribucion']
        widgets = {
            'atribucion': forms.Select(attrs={
                'class': 'form-select'
            })
        }


AtribucionCompositorFormSet = forms.inlineformset_factory(
    ObraGeneral,
    AtribucionCompositor,
    form=AtribucionCompositorForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Forma130Form(forms.ModelForm):
    """130 $k - Forma (R)"""
    class Meta:
        model = Forma130
        fields = ['forma']
        widgets = {
            'forma': forms.Select(attrs={
                'class': 'form-select'
            })
        }


Forma130FormSet = forms.inlineformset_factory(
    ObraGeneral,
    Forma130,
    form=Forma130Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class MedioInterpretacion130Form(forms.ModelForm):
    """130 $m - Medio de interpretación (R)"""
    class Meta:
        model = MedioInterpretacion130
        fields = ['medio']
        widgets = {
            'medio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '130 $m - Ej: piano, violín, orquesta'
            })
        }


MedioInterpretacion130FormSet = forms.inlineformset_factory(
    ObraGeneral,
    MedioInterpretacion130,
    form=MedioInterpretacion130Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class NumeroParteSección130Form(forms.ModelForm):
    """130 $n - Número de parte (R)"""
    class Meta:
        model = NumeroParteSección130
        fields = ['numero']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '130 $n - Ej: I, II, III o 1, 2, 3'
            })
        }


NumeroParteSección130FormSet = forms.inlineformset_factory(
    ObraGeneral,
    NumeroParteSección130,
    form=NumeroParteSección130Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class NombreParteSección130Form(forms.ModelForm):
    """130 $p - Nombre de parte (R)"""
    class Meta:
        model = NombreParteSección130
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '130 $p - Ej: Allegro, Andante, Finale'
            })
        }


NombreParteSección130FormSet = forms.inlineformset_factory(
    ObraGeneral,
    NombreParteSección130,
    form=NombreParteSección130Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


# Formularios 240 (idéntico patrón a 130)

class Forma240Form(forms.ModelForm):
    """240 $k - Forma (R)"""
    class Meta:
        model = Forma240
        fields = ['forma']
        widgets = {
            'forma': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '240 $k - Forma'
            })
        }


Forma240FormSet = forms.inlineformset_factory(
    ObraGeneral,
    Forma240,
    form=Forma240Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class MedioInterpretacion240Form(forms.ModelForm):
    """240 $m - Medio de interpretación (R)"""
    class Meta:
        model = MedioInterpretacion240
        fields = ['medio']
        widgets = {
            'medio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '240 $m - Medio de interpretación'
            })
        }


MedioInterpretacion240FormSet = forms.inlineformset_factory(
    ObraGeneral,
    MedioInterpretacion240,
    form=MedioInterpretacion240Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class NumeroParteSección240Form(forms.ModelForm):
    """240 $n - Número de parte (R)"""
    class Meta:
        model = NumeroParteSección240
        fields = ['numero']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '240 $n - Número'
            })
        }


NumeroParteSección240FormSet = forms.inlineformset_factory(
    ObraGeneral,
    NumeroParteSección240,
    form=NumeroParteSección240Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class NombreParteSección240Form(forms.ModelForm):
    """240 $p - Nombre de parte (R)"""
    class Meta:
        model = NombreParteSección240
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '240 $p - Nombre'
            })
        }


NombreParteSección240FormSet = forms.inlineformset_factory(
    ObraGeneral,
    NombreParteSección240,
    form=NombreParteSección240Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============================================================
# 📋 BLOQUE 2XX - TÍTULOS Y PUBLICACIÓN
# ============================================================

class TituloAlternativoForm(forms.ModelForm):
    """246 - Título alternativo (R)"""
    class Meta:
        model = TituloAlternativo
        fields = ['titulo', 'resto_titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '246 $a - Título alternativo'
            }),
            'resto_titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '246 $b - Resto del título'
            })
        }


TituloAlternativoFormSet = forms.inlineformset_factory(
    ObraGeneral,
    TituloAlternativo,
    form=TituloAlternativoForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class EdicionForm(forms.ModelForm):
    """250 - Edición (R)"""
    class Meta:
        model = Edicion
        fields = ['edicion']
        widgets = {
            'edicion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '250 $a - Edición (ej: 2a ed., Primera edición)'
            })
        }


EdicionFormSet = forms.inlineformset_factory(
    ObraGeneral,
    Edicion,
    form=EdicionForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class ProduccionPublicacionForm(forms.ModelForm):
    """264 - Producción/Publicación (R) - LIGADOS"""
    class Meta:
        model = ProduccionPublicacion
        fields = ['funcion', 'lugar', 'nombre_entidad', 'fecha']
        widgets = {
            'funcion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '264 $a - Lugar'
            }),
            'nombre_entidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '264 $b - Entidad'
            }),
            'fecha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '264 $c - Fecha'
            })
        }


ProduccionPublicacionFormSet = forms.inlineformset_factory(
    ObraGeneral,
    ProduccionPublicacion,
    form=ProduccionPublicacionForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============================================================
# 📋 BLOQUE 3XX - DESCRIPCIÓN FÍSICA
# ============================================================

class Extension300Form(forms.ModelForm):
    """300 $a - Extensión (R)"""
    class Meta:
        model = Extension300
        fields = ['extension']
        widgets = {
            'extension': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '300 $a - Ej: 1 partitura (24 p.)'
            })
        }


Extension300FormSet = forms.inlineformset_factory(
    DescripcionFisica,
    Extension300,
    form=Extension300Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Dimension300Form(forms.ModelForm):
    """300 $c - Dimensión (R)"""
    class Meta:
        model = Dimension300
        fields = ['dimension']
        widgets = {
            'dimension': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '300 $c - Ej: 30 cm'
            })
        }


Dimension300FormSet = forms.inlineformset_factory(
    DescripcionFisica,
    Dimension300,
    form=Dimension300Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class DescripcionFisicaForm(forms.ModelForm):
    """300 - Descripción Física (R)"""
    class Meta:
        model = DescripcionFisica
        fields = ['otras_caracteristicas_fisicas', 'material_acompanante']
        widgets = {
            'otras_caracteristicas_fisicas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '300 $b - Características'
            }),
            'material_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '300 $e - Material acompañante'
            })
        }


DescripcionFisicaFormSet = forms.inlineformset_factory(
    ObraGeneral,
    DescripcionFisica,
    form=DescripcionFisicaForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


# ============ 340 - MEDIO FÍSICO ============

class Tecnica340Form(forms.ModelForm):
    """340 $d - Técnica (R)"""
    class Meta:
        model = Tecnica340
        fields = ['tecnica']
        widgets = {
            'tecnica': forms.Select(attrs={
                'class': 'form-select'
            })
        }


Tecnica340FormSet = forms.inlineformset_factory(
    MedioFisico,
    Tecnica340,
    form=Tecnica340Form,
    extra=1,
    min_num=1,
    max_num=10,
    can_delete=True
)


class MedioFisicoForm(forms.ModelForm):
    """340 - Medio Físico (R)"""
    class Meta:
        model = MedioFisico
        fields = []
        widgets = {}


MedioFisicoFormSet = forms.inlineformset_factory(
    ObraGeneral,
    MedioFisico,
    form=MedioFisicoForm,
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True
)

# ============ 348 - CARACTERÍSTICAS MÚSICA NOTADA ============

class Formato348Form(forms.ModelForm):
    """348 $a - Formato (R)"""
    class Meta:
        model = Formato348
        fields = ['formato']
        widgets = {
            'formato': forms.Select(attrs={
                'class': 'form-select'
            })
        }


Formato348FormSet = forms.inlineformset_factory(
    CaracteristicaMusicaNotada,
    Formato348,
    form=Formato348Form,
    extra=1,
    min_num=1,
    max_num=10,
    can_delete=True
)


class CaracteristicaMusicaNotadaForm(forms.ModelForm):
    """348 - Características Música Notada (R)"""
    class Meta:
        model = CaracteristicaMusicaNotada
        fields = []
        widgets = {}


CaracteristicaMusicaNotadaFormSet = forms.inlineformset_factory(
    ObraGeneral,
    CaracteristicaMusicaNotada,
    form=CaracteristicaMusicaNotadaForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============ 382 - MEDIO DE INTERPRETACIÓN ============

class MedioInterpretacion382_aForm(forms.ModelForm):
    """382 $a - Medio (R)"""
    class Meta:
        model = MedioInterpretacion382_a
        fields = ['medio']
        widgets = {
            'medio': forms.Select(attrs={
                'class': 'form-select'
            })
        }


MedioInterpretacion382_aFormSet = forms.inlineformset_factory(
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    form=MedioInterpretacion382_aForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Solista382Form(forms.ModelForm):
    """382 $b - Solista (R)"""
    class Meta:
        model = Solista382
        fields = ['solista']
        widgets = {
            'solista': forms.Select(attrs={
                'class': 'form-select'
            })
        }


Solista382FormSet = forms.inlineformset_factory(
    MedioInterpretacion382,
    Solista382,
    form=Solista382Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class NumeroInterpretes382Form(forms.ModelForm):
    """382 $n - Número (R)"""
    class Meta:
        model = NumeroInterpretes382
        fields = ['numero']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '382 $n - Ej: 2, 4, 8'
            })
        }


NumeroInterpretes382FormSet = forms.inlineformset_factory(
    MedioInterpretacion382,
    NumeroInterpretes382,
    form=NumeroInterpretes382Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class MedioInterpretacion382Form(forms.ModelForm):
    """382 - Medio de Interpretación (R)"""
    class Meta:
        model = MedioInterpretacion382
        fields = []
        widgets = {}


MedioInterpretacion382FormSet = forms.inlineformset_factory(
    ObraGeneral,
    MedioInterpretacion382,
    form=MedioInterpretacion382Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============ 383 - DESIGNACIÓN NUMÉRICA ============

class NumeroObra383Form(forms.ModelForm):
    """383 $a - Número de obra (R)"""
    class Meta:
        model = NumeroObra383
        fields = ['numero_obra']
        widgets = {
            'numero_obra': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '383 $a - Ej: 1, K. 545, BWV 1001'
            })
        }


NumeroObra383FormSet = forms.inlineformset_factory(
    DesignacionNumericaObra,
    NumeroObra383,
    form=NumeroObra383Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Opus383Form(forms.ModelForm):
    """383 $b - Opus (R)"""
    class Meta:
        model = Opus383
        fields = ['opus']
        widgets = {
            'opus': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '383 $b - Ej: Op. 27, No. 2'
            })
        }


Opus383FormSet = forms.inlineformset_factory(
    DesignacionNumericaObra,
    Opus383,
    form=Opus383Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class DesignacionNumericaObraForm(forms.ModelForm):
    """383 - Designación Numérica (R)"""
    class Meta:
        model = DesignacionNumericaObra
        fields = []
        widgets = {}


DesignacionNumericaObraFormSet = forms.inlineformset_factory(
    ObraGeneral,
    DesignacionNumericaObra,
    form=DesignacionNumericaObraForm,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============================================================
# 📋 BLOQUE 4XX - SERIES
# ============================================================

class TituloSerie490Form(forms.ModelForm):
    """490 $a - Título de serie (R)"""
    class Meta:
        model = TituloSerie490
        fields = ['titulo_serie']
        widgets = {
            'titulo_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '490 $a - Título de serie'
            })
        }


TituloSerie490FormSet = forms.inlineformset_factory(
    MencionSerie490,
    TituloSerie490,
    form=TituloSerie490Form,
    extra=1,
    min_num=1,
    max_num=10,
    can_delete=True
)


class VolumenSerie490Form(forms.ModelForm):
    """490 $v - Volumen (R)"""
    class Meta:
        model = VolumenSerie490
        fields = ['volumen']
        widgets = {
            'volumen': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '490 $v - Volumen'
            })
        }


VolumenSerie490FormSet = forms.inlineformset_factory(
    MencionSerie490,
    VolumenSerie490,
    form=VolumenSerie490Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class MencionSerie490Form(forms.ModelForm):
    """490 - Mención de Serie (R)"""
    class Meta:
        model = MencionSerie490
        fields = ['relacion']
        widgets = {
            'relacion': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }


MencionSerie490FormSet = forms.inlineformset_factory(
    ObraGeneral,
    MencionSerie490,
    form=MencionSerie490Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

# ============================================================
# 📋 BLOQUE 5XX - NOTAS Y DESCRIPCIONES
# ============================================================

class NotaGeneral500Form(forms.ModelForm):
    """500 $a - Nota general (R)"""
    class Meta:
        model = NotaGeneral500
        fields = ['nota_general']
        widgets = {
            'nota_general': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '500 $a - Nota general (ej: Obra inédita conservada en el archivo X)',
            })
        }

NotaGeneral500FormSet = forms.inlineformset_factory(
    ObraGeneral,
    NotaGeneral500,
    form=NotaGeneral500Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Contenido505Form(forms.ModelForm):
    """505 $a - Contenido (R)"""
    class Meta:
        model = Contenido505
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '505 $a - Contenido (ej: 1. Allegro – 2. Andante – 3. Finale)',
            })
        }

Contenido505FormSet = forms.inlineformset_factory(
    ObraGeneral,
    Contenido505,
    form=Contenido505Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


class Sumario520Form(forms.ModelForm):
    """520 $a - Sumario (NR)"""
    class Meta:
        model = Sumario520
        fields = ['sumario']
        widgets = {
            'sumario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '520 $a - Breve resumen o descripción general de la obra',
            })
        }

Sumario520FormSet = forms.inlineformset_factory(
    ObraGeneral,
    Sumario520,
    form=Sumario520Form,
    extra=1,
    min_num=0,
    max_num=5,
    can_delete=True
)


class DatosBiograficos545Form(forms.ModelForm):
    """545 $a, $u - Datos biográficos del compositor (R)"""
    class Meta:
        model = DatosBiograficos545
        fields = ['datos_biograficos', 'url']
        widgets = {
            'datos_biograficos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '545 $a - Ej: Compositor austríaco del periodo clásico...',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '545 $u - URL relacionada (opcional)',
            }),
        }

DatosBiograficos545FormSet = forms.inlineformset_factory(
    ObraGeneral,
    DatosBiograficos545,
    form=DatosBiograficos545Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)
# ============================================================
# 📚 BLOQUE 6XX - MATERIAS Y GÉNERO/FORMA
# ============================================================

# ---------- 650 ## Materia (Temas) ----------

class Materia650Form(forms.ModelForm):
    """650 $a - Materia (NR)"""
    class Meta:
        model = Materia650
        fields = ['materia']
        widgets = {
            'materia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '650 $a - Materia (ej: Música barroca)',
                'maxlength': 255
            })
        }


class SubdivisionMateria650Form(forms.ModelForm):
    """650 $x - Subdivisión de materia (R)"""
    class Meta:
        model = SubdivisionMateria650
        fields = ['subdivision']
        widgets = {
            'subdivision': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '650 $x - Subdivisión de materia (ej: Historia y crítica)',
                'maxlength': 255
            })
        }


# --- Formsets (para gestión repetible) ---
SubdivisionMateria650FormSet = forms.inlineformset_factory(
    Materia650,
    SubdivisionMateria650,
    form=SubdivisionMateria650Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

Materia650FormSet = forms.inlineformset_factory(
    ObraGeneral,
    Materia650,
    form=Materia650Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


# ---------- 655 #4 Materia (Género/Forma) ----------

class MateriaGenero655Form(forms.ModelForm):
    """655 $a - Materia (Género/Forma) (NR)"""
    class Meta:
        model = MateriaGenero655
        fields = ['materia_genero']
        widgets = {
            'materia_genero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '655 $a - Materia (Género/Forma) (ej: Sinfonías, Sonatas, etc.)',
                'maxlength': 255
            })
        }


class SubdivisionGeneral655Form(forms.ModelForm):
    """655 $x - Subdivisión general (R)"""
    class Meta:
        model = SubdivisionGeneral655
        fields = ['subdivision_general']
        widgets = {
            'subdivision_general': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '655 $x - Subdivisión general (ej: Crítica e interpretación)',
                'maxlength': 255
            })
        }


# --- Formsets (para gestión repetible) ---
SubdivisionGeneral655FormSet = forms.inlineformset_factory(
    MateriaGenero655,
    SubdivisionGeneral655,
    form=SubdivisionGeneral655Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)

MateriaGenero655FormSet = forms.inlineformset_factory(
    ObraGeneral,
    MateriaGenero655,
    form=MateriaGenero655Form,
    extra=1,
    min_num=0,
    max_num=10,
    can_delete=True
)


# ============================================================
# 🎯 FORMULARIO PRINCIPAL - ObraGeneral
# ============================================================

class ObraGeneralForm(forms.ModelForm):
    """Formulario principal para catalogación MARC21"""
    
    class Meta:
        model = ObraGeneral
        fields = [
            'tipo_registro',
            'nivel_bibliografico',
            'titulo_principal',
            'subtitulo',
            'mencion_responsabilidad',
            'tonalidad_384',
            'compositor',
            'titulo_uniforme'
        ]
        widgets = {
            'tipo_registro': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'nivel_bibliografico': forms.Select(attrs={
                'class': 'form-select'
            }),
            'titulo_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '245 $a - Título principal (obligatorio)',
                'required': True
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '245 $b - Subtítulo'
            }),
            'mencion_responsabilidad': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '245 $c - Mención de responsabilidad'
            }),
            'tonalidad_384': forms.Select(attrs={
                'class': 'form-select'
            }),
            'compositor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'titulo_uniforme': forms.Select(attrs={
                'class': 'form-select'
            })
        }


# ============================================================
# 📦 EXPORTAR TODOS LOS FORMULARIOS
# ============================================================

__all__ = [
    # Bloque 0XX
    'ISBNForm',
    'ISMNFormSet',
    'NumeroEditorForm',
    'IncipitMusicalForm',
    'IncipitURLFormSet',
    'IdiomaObraFormSet',
    'CodigoLenguaForm',
    'CodigoPaisEntidadFormSet',
    # Bloque 1XX
    'FuncionCompositorFormSet',
    'AtribucionCompositorFormSet',
    'Forma130FormSet',
    'MedioInterpretacion130FormSet',
    'NumeroParteSección130FormSet',
    'NombreParteSección130FormSet',
    'Forma240FormSet',
    'MedioInterpretacion240FormSet',
    'NumeroParteSección240FormSet',
    'NombreParteSección240FormSet',
    # Bloque 2XX
    'TituloAlternativoFormSet',
    'EdicionFormSet',
    'ProduccionPublicacionFormSet',
    # Bloque 3XX
    'Extension300FormSet',
    'Dimension300FormSet',
    'DescripcionFisicaFormSet',
    'Tecnica340FormSet',
    'MedioFisicoFormSet',
    'Formato348FormSet',
    'CaracteristicaMusicaNotadaFormSet',
    'MedioInterpretacion382_aFormSet',
    'Solista382FormSet',
    'NumeroInterpretes382FormSet',
    'MedioInterpretacion382FormSet',
    'NumeroObra383FormSet',
    'Opus383FormSet',
    'DesignacionNumericaObraFormSet',
    # Bloque 4XX
    'TituloSerie490FormSet',
    'VolumenSerie490FormSet',
    'MencionSerie490FormSet',
    # Bloque 5XX
    'NotaGeneral500FormSet',
    'Contenido505FormSet',
    'Sumario520FormSet',
    'DatosBiograficos545FormSet',
    # Bloque 6XX
    'Materia650FormSet',
    'SubdivisionMateria650FormSet',
    'MateriaGenero655FormSet',
    'SubdivisionGeneral655FormSet',

    # Principal
    'ObraGeneralForm',
]
