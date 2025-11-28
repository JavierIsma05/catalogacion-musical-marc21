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

# ========================================================================
# 700 – Nombre relacionado
# ========================================================================

class NombreRelacionado700Form(forms.ModelForm):
    # Campos extra para autocomplete (igual idea que 100)
    persona_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control persona700-input',
            'placeholder': 'Escriba o seleccione una persona…',
            'autocomplete': 'off',
        }),
        label='700 $a – Nombre de persona'
    )

    persona_coordenadas = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control persona700-coord-input',
            'placeholder': 'Ej: 1900-1980',
        }),
        label='700 $d – Coordenadas biográficas'
    )

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
            # ahora el FK va oculto, lo maneja el autocomplete
            'persona': forms.HiddenInput(attrs={
                'class': 'persona700-id'
            }),
            'coordenadas_biograficas': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'relacion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'autoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'titulo_obra': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'persona': '700 $a – Nombre de persona',
            'coordenadas_biograficas': '700 $d – Coordenadas biográficas',
            'relacion': '700 $i – Relación',
            'autoria': '700 $j – Autoría',
            'titulo_obra': '700 $t – Título de la obra',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estoy editando y ya hay persona, rellenar los campos de texto
        if self.instance.pk and self.instance.persona_id:
            persona = self.instance.persona
            self.fields['persona_texto'].initial = persona.apellidos_nombres
            self.fields['persona_coordenadas'].initial = (
                persona.coordenadas_biograficas or ''
            )

    def clean(self):
        cleaned_data = super().clean()

        persona_texto = cleaned_data.get('persona_texto', '').strip()
        persona_coord = cleaned_data.get('persona_coordenadas', '').strip()

        # Si el usuario escribió algo en el nombre, resolvemos/creamos la autoridad
        if persona_texto:
            from catalogacion.models import AutoridadPersona

            try:
                persona = AutoridadPersona.objects.get(
                    apellidos_nombres__iexact=persona_texto
                )
                # Actualizar coordenadas si cambiaron
                if persona_coord and persona.coordenadas_biograficas != persona_coord:
                    persona.coordenadas_biograficas = persona_coord
                    persona.save()
                cleaned_data['persona'] = persona
            except AutoridadPersona.DoesNotExist:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=persona_texto,
                    coordenadas_biograficas=persona_coord
                )
                cleaned_data['persona'] = persona
            except AutoridadPersona.MultipleObjectsReturned:
                persona = AutoridadPersona.objects.filter(
                    apellidos_nombres__iexact=persona_texto
                ).first()
                cleaned_data['persona'] = persona

        # Si no escribió nada y persona viene vacío → se tratará como formulario vacío,
        # el inlineformset no lo guardará si todos los campos están vacíos.
        return cleaned_data



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

    # Campo editable para el nombre (autocomplete)
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="773 $a – Encabezamiento principal",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Escriba para buscar o agregar...",
            "autocomplete": "off",
        })
    )

    class Meta:
        model = EnlaceDocumentoFuente773
        fields = [
            "primer_indicador",
            "segundo_indicador",
            "encabezamiento_principal",
            "titulo",
        ]
        widgets = {
            "primer_indicador": forms.Select(
                choices=PRIMER_INDICADOR_773,
                attrs={"class": "form-select"}
            ),
            "segundo_indicador": forms.Select(
                choices=SEGUNDO_INDICADOR_773,
                attrs={"class": "form-select"}
            ),

            # 👇 YA NO ES SELECT2 → ahora es hidden
            "encabezamiento_principal": forms.HiddenInput(),

            "titulo": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "primer_indicador": "773 – Primer indicador",
            "segundo_indicador": "773 – Segundo indicador",
            "encabezamiento_principal": "773 $a – Encabezamiento principal",
            "titulo": "773 $t – Título",
        }

    def clean(self):
        data = super().clean()

        texto = data.get("encabezamiento_principal_texto", "").strip()

        if texto:
            # Buscar persona existente
            obj = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=texto
            ).first()

            if not obj:
                # Crear nueva persona si no existe
                obj = AutoridadPersona.objects.create(
                    apellidos_nombres=texto
                )

            data["encabezamiento_principal"] = obj

        return data



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

    # Campo visible tipo "Muscat"
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="774 $a – Encabezamiento principal",
        widget=forms.TextInput(attrs={
            'class': 'form-control autocomplete-774',
            'placeholder': 'Escriba para buscar o agregar…',
            'autocomplete': 'off'
        })
    )

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
            # Campo real oculto
            'encabezamiento_principal': forms.HiddenInput(),

            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
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

    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="787 $a – Encabezamiento principal",
        widget=forms.TextInput(attrs={
            'class': 'form-control autocomplete-787',
            'placeholder': 'Escriba para buscar o agregar…',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = OtrasRelaciones787
        fields = [
            'primer_indicador',
            'segundo_indicador',
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            'primer_indicador': forms.Select(
                choices=PRIMER_INDICADOR_787,
                attrs={'class': 'form-select'}
            ),
            'segundo_indicador': forms.Select(
                choices=SEGUNDO_INDICADOR_787,
                attrs={'class': 'form-select'}
            ),

            'encabezamiento_principal': forms.HiddenInput(),

            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
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
