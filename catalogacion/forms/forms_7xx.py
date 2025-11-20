"""
Formularios para bloque 7XX - Puntos de acceso adicionales y enlaces
"""
from django import forms
from catalogacion.models import (
    # 700
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,

    # 710
    EntidadRelacionada710,

    # 773, 774, 787
    EnlaceDocumentoFuente773,
    NumeroControl773,
    EnlaceUnidadConstituyente774,
    NumeroControl774,
    OtrasRelaciones787,
    NumeroControl787,

    # Autoridades
    AutoridadPersona,
    AutoridadEntidad,
    EncabezamientoEnlace,
)
from .widgets import Select2Widget


# ========================================================================
# 700 – Nombre relacionado
# ========================================================================

class NombreRelacionado700Form(forms.ModelForm):
    class Meta:
        model = NombreRelacionado700
        fields = [
            'persona',
            'coordenadas_biograficas',
            'relacion',
            'autoria',
            'titulo_obra'
        ]
        widgets = {
            'persona': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/persona/',
            }),
            'coordenadas_biograficas': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion': forms.TextInput(attrs={'class': 'form-control'}),
            'autoria': forms.Select(attrs={'class': 'form-select'}),
            'titulo_obra': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'persona': '700 $a – Nombre de persona',
            'coordenadas_biograficas': '700 $d – Coordenadas biográficas',
            'relacion': '700 $i – Relación',
            'autoria': '700 $j – Autoría',
            'titulo_obra': '700 $t – Título de la obra',
        }


class TerminoAsociado700Form(forms.ModelForm):
    class Meta:
        model = TerminoAsociado700
        fields = ['termino']
        widgets = {
            'termino': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'termino': '700 $c – Término asociado'
        }


class Funcion700Form(forms.ModelForm):
    class Meta:
        model = Funcion700
        fields = ['funcion']
        widgets = {
            'funcion': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'funcion': '700 $e – Función'
        }


# ========================================================================
# 710 – Entidad relacionada
# ========================================================================

class EntidadRelacionada710Form(forms.ModelForm):
    class Meta:
        model = EntidadRelacionada710
        fields = ['entidad', 'funcion']
        widgets = {
            'entidad': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/entidad/',
            }),
            'funcion': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'entidad': '710 $a – Entidad relacionada',
            'funcion': '710 $e – Función institucional',
        }


# ========================================================================
# 773 – Enlace a documento fuente
# ========================================================================
PRIMER_INDICADOR_773 = [('1', '1 – No genera nota')]
SEGUNDO_INDICADOR_773 = [('#', "# – Visualización 'En'")]
class EnlaceDocumentoFuente773Form(forms.ModelForm):
    

    class Meta:
        model = EnlaceDocumentoFuente773
        fields = [
            'primer_indicador',
            'segundo_indicador',
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            'primer_indicador': forms.Select(choices=PRIMER_INDICADOR_773, attrs={'class': 'form-select'}),
            'segundo_indicador': forms.Select(choices=SEGUNDO_INDICADOR_773, attrs={'class': 'form-select'}),
            'encabezamiento_principal': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/encabezamiento/',
            }),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'primer_indicador': '773 – Primer indicador',
            'segundo_indicador': '773 – Segundo indicador',
            'encabezamiento_principal': '773 $a – Encabezamiento principal',
            'titulo': '773 $t – Título',
        }


class NumeroControl773Form(forms.ModelForm):
    class Meta:
        model = NumeroControl773
        fields = ['obra_relacionada']
        widgets = {
            'obra_relacionada': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/obra/',
            })
        }
        labels = {
            'obra_relacionada': '773 $w – Número de control (001)',
        }


# ========================================================================
# 774 – Enlace a unidad constituyente
# ========================================================================
PRIMER_INDICADOR_774 = [('1', '1 – No genera nota')]
SEGUNDO_INDICADOR_774 = [('#', "# – Visualización 'Contiene'")]
class EnlaceUnidadConstituyente774Form(forms.ModelForm):
    

    class Meta:
        model = EnlaceUnidadConstituyente774
        fields = [
            'primer_indicador',
            'segundo_indicador',
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            'primer_indicador': forms.Select(
                choices=PRIMER_INDICADOR_774,
                attrs={'class': 'form-select'}
            ),
            'segundo_indicador': forms.Select(
                choices=SEGUNDO_INDICADOR_774,
                attrs={'class': 'form-select'}
            ),
            'encabezamiento_principal': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/encabezamiento/',
            }),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'primer_indicador': '774 – Primer indicador',
            'segundo_indicador': '774 – Segundo indicador',
            'encabezamiento_principal': '774 $a – Encabezamiento principal',
            'titulo': '774 $t – Título',
        }

class NumeroControl774Form(forms.ModelForm):
    class Meta:
        model = NumeroControl774
        fields = ['obra_relacionada']
    widgets = {
            'obra_relacionada': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/obra/',
            })
        }
    labels = {
            'obra_relacionada': '774 $w – Número de control (001)',
        }


# ========================================================================
# 787 – Otras relaciones
# ========================================================================

PRIMER_INDICADOR_787 = [('1', '1 – No genera nota')]
SEGUNDO_INDICADOR_787 = [('#', "# – Visualización 'Documento relacionado'")]
class OtrasRelaciones787Form(forms.ModelForm):

    class Meta:
        model = OtrasRelaciones787
        fields = [
            'primer_indicador',
            'segundo_indicador',
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            'primer_indicador': forms.Select(choices=PRIMER_INDICADOR_787, attrs={'class': 'form-select'}),
            'segundo_indicador': forms.Select(choices=SEGUNDO_INDICADOR_787, attrs={'class': 'form-select'}),
            'encabezamiento_principal': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/encabezamiento/',
            }),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'primer_indicador': '787 – Primer indicador',
            'segundo_indicador': '787 – Segundo indicador',
            'encabezamiento_principal': '787 $a – Encabezamiento principal',
            'titulo': '787 $t – Título',
        }


class NumeroControl787Form(forms.ModelForm):
    class Meta:
        model = NumeroControl787
        fields = ['obra_relacionada']
        widgets = {
            'obra_relacionada': Select2Widget(attrs={
                'data-url': '/catalogacion/autocompletar/obra/',
            })
        }
        labels = {
            'obra_relacionada': '787 $w – Número de control (001)',
        }
