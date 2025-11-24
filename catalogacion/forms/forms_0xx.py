"""
Formularios para bloque 0XX - Campos de control e identificación
"""
from django import forms
from catalogacion.models import (
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
)
from .widgets import TextAreaAutosize

CLAVES_PAE = [
    ("G-2", "Clave de Sol (G-2)"),
    ("C-3", "Clave de Do en 3ª (C-3)"),
    ("F-4", "Clave de Fa en 4ª (F-4)"),

]

ARMADURAS_PAE = [
    ("", "Sin armadura"),
    ("xF", "1 sostenido (F#)"),
    ("xFC", "2 sostenidos (F#, C#)"),
    ("xFCG", "3 sostenidos (F#, C#, G#)"),
    ("xFCGD", "4 sostenidos"),
    ("xFCGDA", "5 sostenidos"),
    ("xFCGDAE", "6 sostenidos"),
    ("xFCGDAEB", "7 sostenidos"),
    ("bB", "1 bemol (Bb)"),
    ("bBE", "2 bemoles (Bb, Eb)"),
    ("bBEA", "3 bemoles"),
    ("bBEAD", "4 bemoles"),
    ("bBEADG", "5 bemoles"),
    ("bBEADGC", "6 bemoles"),
    ("bBEADGCF", "7 bemoles"),
]

TIEMPOS_MUSICALES = [
    ("2/4", "2/4"),
    ("3/4", "3/4"),
    ("4/4", "4/4"),
    ("3/8", "3/8"),
    ("6/8", "6/8"),
    ("9/8", "9/8"),
    ("12/8", "12/8"),
]

CLAVES_PAE = [
    ("%G-2", "Clave de Sol (G-2)"),
    ("%C-3", "Clave de Do en 3ª (C-3)"),
    ("%F-4", "Clave de Fa en 4ª (F-4)"),

]

ARMADURAS_PAE = [
    ("", "Sin armadura"),
    ("F", "1 sostenido (F#)"),
    ("FC", "2 sostenidos (F#, C#)"),
    ("FCG", "3 sostenidos (F#, C#, G#)"),
    ("FCGD", "4 sostenidos"),
    ("FCGDA", "5 sostenidos"),
    ("FCGDAE", "6 sostenidos"),
    ("FCGDAEB", "7 sostenidos"),
    ("bB", "1 bemol (Bb)"),
    ("bBE", "2 bemoles (Bb, Eb)"),
    ("bBEA", "3 bemoles"),
    ("bBEAD", "4 bemoles"),
    ("bBEADG", "5 bemoles"),
    ("bBEADGC", "6 bemoles"),
    ("bBEADGCF", "7 bemoles"),
]

TIEMPOS_MUSICALES = [
    ("2/4", "2/4"),
    ("3/4", "3/4"),
    ("4/4", "4/4"),
    ("3/8", "3/8"),
    ("6/8", "6/8"),
    ("9/8", "9/8"),
    ("12/8", "12/8"),
]


class IncipitMusicalForm(forms.ModelForm):
    """Formulario para campo 031 - Íncipit musical"""


    class Meta:
        model = IncipitMusical
        fields = [
            "numero_obra",
            "numero_movimiento",
            "numero_pasaje",
            "titulo_encabezamiento",
            "personaje",
            "clave",
            "voz_instrumento",
            "armadura",
            "tiempo",
            "notacion_musical",
            "numero_obra",
            "numero_movimiento",
            "numero_pasaje",
            "titulo_encabezamiento",
            "personaje",
            "clave",
            "voz_instrumento",
            "armadura",
            "tiempo",
            "notacion_musical",
            "nota_general",
            "tonalidad_modo",
            "nota_validez_codificada",
        ]
        widgets = {
            "numero_obra": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "numero_movimiento": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "numero_pasaje": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "titulo_encabezamiento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $d - Título/tempo",
                }
            ),
            "personaje": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $e - Personaje",
                }
            ),
            "clave": forms.Select(
                choices=CLAVES_PAE,
                attrs={"class": "form-select"},

            ),
            "voz_instrumento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $m - Voz/instrumento",
                }
            ),
            "armadura": forms.Select(
                choices=ARMADURAS_PAE,
                attrs={"class": "form-select"},
            ),
            "tiempo": forms.Select(
                choices=TIEMPOS_MUSICALES,
                attrs={"class": "form-select"},
            ),
            "notacion_musical": TextAreaAutosize(
                attrs={
                    "placeholder": "031 $p - Notación musical codificada",
                    "rows": 4,
                }
            ),
            "numero_obra": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "numero_movimiento": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "numero_pasaje": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "titulo_encabezamiento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $d - Título/tempo",
                }
            ),
            "personaje": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $e - Personaje",
                }
            ),
            "clave": forms.Select(
                choices=CLAVES_PAE,
                attrs={"class": "form-select"},
            ),
            "voz_instrumento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $m - Voz/instrumento",
                }
            ),
            "armadura": forms.Select(
                choices=ARMADURAS_PAE,
                attrs={"class": "form-select"},
            ),
            "tiempo": forms.Select(
                choices=TIEMPOS_MUSICALES,
                attrs={"class": "form-select"},
            ),
            "notacion_musical": TextAreaAutosize(
                attrs={
                    "placeholder": "031 $p - Notación musical codificada",
                    "rows": 4,
                }
            ),
            "nota_general": TextAreaAutosize(
                attrs={
                    "placeholder": "031 $q - Nota general",
                    "rows": 3,
                }
            ),
            "tonalidad_modo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $r - Tonalidad o modo",
                }
            ),
            "nota_validez_codificada": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "031 $s - Nota de validez codificada",
                }
            ),
        }


class IncipitURLForm(forms.ModelForm):
    """Formulario para campo 031 $u - URL de íncipit"""


    class Meta:
        model = IncipitURL
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '031 $u - URL del íncipit',
            }),
        }


class CodigoLenguaForm(forms.ModelForm):
    """Formulario para campo 041 - Código de lengua"""


    class Meta:
        model = CodigoLengua
        fields = [
            'indicacion_traduccion',
            'fuente_codigo',
        ]
        widgets = {
            'indicacion_traduccion': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fuente_codigo': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class IdiomaObraForm(forms.ModelForm):
    """Formulario para campo 041 $a - Idioma"""


    class Meta:
        model = IdiomaObra
        fields = ['codigo_idioma']
        widgets = {
            'codigo_idioma': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'codigo_idioma': '041 $a - Código de idioma',
        }


class CodigoPaisEntidadForm(forms.ModelForm):
    """Formulario para campo 044 $a - País de entidad"""


    class Meta:
        model = CodigoPaisEntidad
        fields = ['codigo_pais']
        widgets = {
            'codigo_pais': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'codigo_pais': '044 $a - Código de país',
        }
