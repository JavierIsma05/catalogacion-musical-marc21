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
    AutoridadTituloUniforme,
    EncabezamientoEnlace,
)
from .widgets import Select2Widget


def ensure_titulo_uniforme_registrado(valor):
    """Devuelve (o crea) la autoridad correspondiente al título uniforme dado."""
    titulo = (valor or "").strip()
    if not titulo:
        return None

    existente = AutoridadTituloUniforme.objects.filter(
        titulo__iexact=titulo
    ).first()

    if existente:
        return existente

    return AutoridadTituloUniforme.objects.create(titulo=titulo)


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
                'class': 'form-control',
                'data-autocomplete': 'titulo',
                'autocomplete': 'off'
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

        titulo_obra = cleaned_data.get('titulo_obra', '')
        if titulo_obra:
            ensure_titulo_uniforme_registrado(titulo_obra)

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

    entidad_texto = forms.CharField(
        required=False,
        label="710 $a – Entidad relacionada",
        widget=forms.TextInput(
            attrs={
                "class": "form-control autocomplete-entidad-710",
                "placeholder": "Escriba para buscar o agregar entidad…",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = EntidadRelacionada710
        fields = ["entidad", "funcion"]
        widgets = {
            "entidad": forms.HiddenInput(),  # 👉 Escondido como en 700/787
            "funcion": forms.Select(attrs={"class": "form-select"}),
        }



# ========================================================================
# 773 – Enlace a documento fuente
# ========================================================================

class EnlaceDocumentoFuente773Form(forms.ModelForm):

    # Campo editable para el nombre (autocomplete)
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="773 $a – Encabezamiento principal",
        widget=forms.TextInput(attrs={
            "class": "form-control autoridad-input",
            "placeholder": "Buscar en Autoridades de Personas…",
            "autocomplete": "off",
            "data-autoridad-input": "1",
            "data-hidden-field": "encabezamiento_principal",
        })
    )

    titulo_texto = forms.CharField(
        required=False,
        label="773 $t – Título",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Buscar en Títulos Uniformes…",
            "autocomplete": "off",
            "data-autocomplete": "titulo",
            "data-hidden-field": "titulo",
        })
    )

    class Meta:
        model = EnlaceDocumentoFuente773
        fields = [
        
            "encabezamiento_principal",
            "titulo",
        ]
        widgets = {
            # 👇 YA NO ES SELECT2 → ahora es hidden
            "encabezamiento_principal": forms.HiddenInput(),

            "titulo": forms.HiddenInput(),
        }
        labels = {
       
            "encabezamiento_principal": "773 $a – Encabezamiento principal",
            "titulo": "773 $t – Título",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["encabezamiento_principal"].required = False
        self.fields["titulo"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput(),
        )

        if self.instance.pk:
            if self.instance.encabezamiento_principal_id:
                persona = self.instance.encabezamiento_principal
                self.fields["encabezamiento_principal_texto"].initial = (
                    persona.apellidos_nombres
                )
            if self.instance.titulo_id:
                self.fields["titulo"].initial = str(self.instance.titulo_id)
                self.fields["titulo_texto"].initial = self.instance.titulo.titulo

    def clean(self):
        data = super().clean()

        if not self.has_changed():
            return data

        texto = data.get("encabezamiento_principal_texto", "").strip()

        if texto:
            obj = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=texto
            ).first()

            if not obj:
                obj = AutoridadPersona.objects.create(
                    apellidos_nombres=texto
                )

            data["encabezamiento_principal"] = obj
        elif not data.get("encabezamiento_principal"):
            self.add_error(
                "encabezamiento_principal_texto",
                "Debe ingresar o seleccionar un encabezamiento principal.",
            )

        titulo_actual = (data.get("titulo") or "").strip()
        titulo_texto = data.get("titulo_texto", "").strip()

        titulo_obj = None
        if titulo_actual:
            try:
                titulo_obj = AutoridadTituloUniforme.objects.filter(
                    pk=int(titulo_actual)
                ).first()
            except (TypeError, ValueError):
                titulo_obj = AutoridadTituloUniforme.objects.filter(
                    titulo__iexact=titulo_actual
                ).first()

            if not titulo_obj:
                titulo_obj = ensure_titulo_uniforme_registrado(titulo_actual)

        if not titulo_obj and titulo_texto:
            titulo_obj = ensure_titulo_uniforme_registrado(titulo_texto)

        if titulo_obj:
            data["titulo"] = titulo_obj
        else:
            self.add_error(
                "titulo_texto",
                "Debe ingresar o seleccionar un título para 773 $t.",
            )

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
class EnlaceUnidadConstituyente774Form(forms.ModelForm):

    # Campo visible tipo "Muscat"
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="774 $a – Encabezamiento principal",
        widget=forms.TextInput(attrs={
            'class': 'form-control autoridad-input',
            'placeholder': 'Buscar en Autoridades de Personas…',
            'autocomplete': 'off',
            'data-autoridad-input': '1',
            'data-hidden-field': 'encabezamiento_principal'
        })
    )

    titulo_texto = forms.CharField(
        required=False,
        label="774 $t – Título",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en Títulos Uniformes…',
            'autocomplete': 'off',
            'data-autocomplete': 'titulo',
            'data-hidden-field': 'titulo'
        })
    )

    class Meta:
        model = EnlaceUnidadConstituyente774
        fields = [
           
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            # Campo real oculto
            'encabezamiento_principal': forms.HiddenInput(),

            'titulo': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['encabezamiento_principal'].required = False
        self.fields['titulo'] = forms.CharField(
            required=False,
            widget=forms.HiddenInput(),
        )

        if self.instance.pk:
            if self.instance.encabezamiento_principal_id:
                self.fields['encabezamiento_principal_texto'].initial = (
                    self.instance.encabezamiento_principal.apellidos_nombres
                )
            if self.instance.titulo_id:
                self.fields['titulo'].initial = str(self.instance.titulo_id)
                self.fields['titulo_texto'].initial = self.instance.titulo.titulo

    def clean(self):
        data = super().clean()

        if not self.has_changed():
            return data

        texto = data.get('encabezamiento_principal_texto', '').strip()
        if texto:
            persona = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=texto
            ).first()
            if not persona:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=texto
                )
            data['encabezamiento_principal'] = persona
        elif not data.get('encabezamiento_principal'):
            self.add_error(
                'encabezamiento_principal_texto',
                'Debe ingresar o seleccionar un encabezamiento principal.',
            )

        titulo_actual = (data.get('titulo') or '').strip()
        titulo_texto = data.get('titulo_texto', '').strip()

        titulo_obj = None
        if titulo_actual:
            try:
                titulo_obj = AutoridadTituloUniforme.objects.filter(
                    pk=int(titulo_actual)
                ).first()
            except (TypeError, ValueError):
                titulo_obj = AutoridadTituloUniforme.objects.filter(
                    titulo__iexact=titulo_actual
                ).first()

            if not titulo_obj:
                titulo_obj = ensure_titulo_uniforme_registrado(titulo_actual)

        if not titulo_obj and titulo_texto:
            titulo_obj = ensure_titulo_uniforme_registrado(titulo_texto)

        if titulo_obj:
            data['titulo'] = titulo_obj
        else:
            self.add_error(
                'titulo_texto',
                'Debe ingresar o seleccionar un título para 774 $t.',
            )

        return data


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
            
            'encabezamiento_principal',
            'titulo'
        ]
        widgets = {
            

            'encabezamiento_principal': forms.HiddenInput(),

            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'data-autocomplete': 'titulo',
                'autocomplete': 'off'
            }),
        }

    def clean(self):
        data = super().clean()

        texto = data.get('encabezamiento_principal_texto', '').strip()
        if texto:
            persona = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=texto
            ).first()
            if not persona:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=texto
                )
            data['encabezamiento_principal'] = persona

        ensure_titulo_uniforme_registrado(data.get('titulo', ''))

        return data

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
