"""
Formularios para bloque 7XX - Puntos de acceso adicionales y enlaces
"""

from django import forms

from catalogacion.models import (
    AutoridadEntidad,
    # Autoridades
    AutoridadPersona,
    AutoridadTituloUniforme,
    # 773, 774, 787
    EnlaceDocumentoFuente773,
    EnlaceUnidadConstituyente774,
    # 710
    EntidadRelacionada710,
    Funcion700,
    # 700
    NombreRelacionado700,
    NumeroControl773,
    NumeroControl774,
    NumeroControl787,
    OtrasRelaciones787,
    TerminoAsociado700,
)

from .widgets import Select2Widget


def ensure_titulo_uniforme_registrado(valor):
    """Devuelve (o crea) la autoridad correspondiente al título uniforme dado."""
    titulo = (valor or "").strip()
    if not titulo:
        return None

    existente = AutoridadTituloUniforme.objects.filter(titulo__iexact=titulo).first()

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
        widget=forms.TextInput(
            attrs={
                "class": "form-control persona700-input",
                "placeholder": "Escriba o seleccione una persona…",
                "autocomplete": "off",
            }
        ),
        label="700 $a – Nombre de persona",
    )

    persona_coordenadas = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control persona700-coord-input",
                "placeholder": "Ej: 1900-1980",
            }
        ),
        label="700 $d – Coordenadas biográficas",
    )

    class Meta:
        model = NombreRelacionado700
        fields = [
            "persona",
            "coordenadas_biograficas",
            "relacion",
            "autoria",
            "titulo_obra",
        ]
        widgets = {
            # ahora el FK va oculto, lo maneja el autocomplete
            "persona": forms.HiddenInput(attrs={"class": "persona700-id"}),
            "coordenadas_biograficas": forms.TextInput(attrs={"class": "form-control"}),
            "relacion": forms.TextInput(attrs={"class": "form-control"}),
            "autoria": forms.Select(attrs={"class": "form-select"}),
            "titulo_obra": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "data-autocomplete": "titulo",
                    "placeholder": "Ej.: Emma Mercedes, Vals N° 3, etc",
                    "autocomplete": "off",
                }
            ),
        }
        labels = {
            "persona": "700 $a – Nombre de persona",
            "coordenadas_biograficas": "700 $d – Coordenadas biográficas",
            "relacion": "700 $i – Relación",
            "autoria": "700 $j – Autoría",
            "titulo_obra": "700 $t – Título de la obra",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estoy editando y ya hay persona, rellenar los campos de texto
        if self.instance.pk and self.instance.persona_id:
            persona = self.instance.persona
            self.fields["persona_texto"].initial = persona.apellidos_nombres
            self.fields["persona_coordenadas"].initial = (
                persona.coordenadas_biograficas or ""
            )

    def clean(self):
        cleaned_data = super().clean()

        persona = cleaned_data.get("persona")
        persona_texto = cleaned_data.get("persona_texto", "").strip()
        coords = cleaned_data.get("persona_coordenadas", "").strip()
        coords_relacion = (cleaned_data.get("coordenadas_biograficas") or "").strip()
        relacion = cleaned_data.get("relacion", "")
        autoria = cleaned_data.get("autoria", "")
        titulo = cleaned_data.get("titulo_obra", "")

        # ============================================================
        # 1️⃣ SI EL FORM ESTÁ VACÍO → MARCAR COMO DELETE
        # ============================================================
        if not (persona or persona_texto or coords or relacion or autoria or titulo):
            cleaned_data["DELETE"] = True
            return cleaned_data

        # ============================================================
        # 2️⃣ CREAR AUTORIDAD PERSONA SI SE ESCRIBIÓ TEXTO
        # ============================================================
        if persona_texto and not persona:
            try:
                persona = AutoridadPersona.objects.get(
                    apellidos_nombres__iexact=persona_texto
                )
            except AutoridadPersona.DoesNotExist:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=persona_texto,
                    coordenadas_biograficas=coords or None,
                )
            cleaned_data["persona"] = persona

        # ============================================================
        # 2️⃣.1️⃣ Sincronizar coordenadas de la autoridad y del 700 $d
        # ============================================================
        if persona and coords:
            if persona.coordenadas_biograficas != coords:
                persona.coordenadas_biograficas = coords
                persona.save(update_fields=["coordenadas_biograficas"])

        if persona and not coords_relacion:
            cleaned_data["coordenadas_biograficas"] = (
                coords or persona.coordenadas_biograficas or None
            )

        # ============================================================
        # 3️⃣ REGISTRAR TÍTULO UNIFORME AUTOMÁTICAMENTE
        # ============================================================
        if titulo:
            ensure_titulo_uniforme_registrado(titulo)

        # ============================================================
        # 4️⃣ VALIDACIÓN NUEVA: 100 vs 700
        #    Evita duplicados o doble compositor
        # ============================================================
        compositor_100 = getattr(self, "compositor_100", None)

        if compositor_100 and persona:
            # ❌ PROHIBIDO: duplicar exactamente el del 100
            if (
                compositor_100.apellidos_nombres.strip().lower()
                == persona.apellidos_nombres.strip().lower()
            ):
                raise forms.ValidationError(
                    "La persona del campo 700 no puede ser la misma que el compositor del campo 100."
                )

        # ✅ Si son distintos → permitido
        return cleaned_data


class TerminoAsociado700Form(forms.ModelForm):
    class Meta:
        model = TerminoAsociado700
        fields = ["termino"]
        widgets = {"termino": forms.TextInput(attrs={"class": "form-control"})}
        labels = {"termino": "700 $c – Término asociado"}


class Funcion700Form(forms.ModelForm):
    class Meta:
        model = Funcion700
        fields = ["funcion"]
        widgets = {"funcion": forms.Select(attrs={"class": "form-select"})}
        labels = {"funcion": "700 $e – Función"}


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
        fields = ["entidad"]
        widgets = {
            "entidad": forms.HiddenInput(),  # 👉 Escondido como en 700/787
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo 'id' lo agrega el inline formset; para forms nuevos llega vacío
        if "id" in self.fields:
            self.fields["id"].required = False
        # Si estamos editando, rellenar el texto de la entidad
        if self.instance.pk and self.instance.entidad_id:
            self.fields["entidad_texto"].initial = self.instance.entidad.nombre

    def clean(self):
        cleaned_data = super().clean()

        entidad = cleaned_data.get("entidad")
        texto = cleaned_data.get("entidad_texto", "").strip()

        # 🟩 1. SI EL FORM ESTÁ COMPLETAMENTE VACÍO → borrar
        if not (entidad or texto):
            self.cleaned_data["DELETE"] = True
            return cleaned_data

        # 🟩 2. SI EL USUARIO ESCRIBIÓ TEXTO PERO NO SELECCIONÓ NADA → buscar o crear
        if texto and not entidad:
            entidad, _created = AutoridadEntidad.objects.get_or_create(nombre=texto)
            cleaned_data["entidad"] = entidad

        return cleaned_data


# ========================================================================
# 773 – Enlace a documento fuente
# ========================================================================


class EnlaceDocumentoFuente773Form(forms.ModelForm):
    # Campo editable para el nombre (autocomplete)
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="773 $a – Encabezamiento principal",
        widget=forms.TextInput(
            attrs={
                "class": "form-control autoridad-input",
                "placeholder": "Buscar en Autoridades de Personas…",
                "autocomplete": "off",
                "data-autoridad-input": "1",
                "data-hidden-field": "encabezamiento_principal",
            }
        ),
    )

    titulo_texto = forms.CharField(
        required=False,
        label="773 $t – Título",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar en Títulos Uniformes…",
                "autocomplete": "off",
                "data-autocomplete": "titulo",
                "data-hidden-field": "titulo",
            }
        ),
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
                self.fields[
                    "encabezamiento_principal_texto"
                ].initial = persona.apellidos_nombres
            if self.instance.titulo_id:
                self.fields["titulo"].initial = str(self.instance.titulo_id)
                self.fields["titulo_texto"].initial = self.instance.titulo.titulo

    def clean(self):
        data = super().clean()

        encabez = data.get("encabezamiento_principal")
        encabez_texto = data.get("encabezamiento_principal_texto", "").strip()

        titulo_value = data.get("titulo")

        # 👉 Normalizamos el valor del título
        if hasattr(titulo_value, "pk"):
            # Es un objeto AutoridadTituloUniforme
            titulo_field = titulo_value.titulo
        else:
            # Es string o None
            titulo_field = (titulo_value or "").strip()

        titulo_texto = data.get("titulo_texto", "").strip()

        # 🟥 1. Formulario vacío → ELIMINAR
        if not (encabez or encabez_texto or titulo_field or titulo_texto):
            self.cleaned_data["DELETE"] = True
            return data

        # 🟦 2. Resolver encabezamiento principal
        if encabez_texto and not encabez:
            persona = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=encabez_texto
            ).first()
            if not persona:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=encabez_texto
                )
            data["encabezamiento_principal"] = persona

        # 🟦 3. Resolver título uniforme
        titulo_obj = None

        # Si vino ID o string que parece ID
        if titulo_value and hasattr(titulo_value, "pk"):
            titulo_obj = titulo_value
        elif titulo_field.isdigit():
            titulo_obj = AutoridadTituloUniforme.objects.filter(
                pk=int(titulo_field)
            ).first()

        # Si no existe, buscar por texto
        if not titulo_obj and titulo_texto:
            titulo_obj = AutoridadTituloUniforme.objects.filter(
                titulo__iexact=titulo_texto
            ).first()
            if not titulo_obj:
                titulo_obj = AutoridadTituloUniforme.objects.create(titulo=titulo_texto)

        if titulo_obj:
            data["titulo"] = titulo_obj
        else:
            self.add_error(
                "titulo_texto", "Debe ingresar o seleccionar un título válido."
            )

        return data


class NumeroControl773Form(forms.ModelForm):
    class Meta:
        model = NumeroControl773
        fields = ["obra_relacionada"]
        widgets = {
            "obra_relacionada": Select2Widget(
                attrs={
                    "data-url": "/catalogacion/autocompletar/obra/",
                }
            )
        }
        labels = {
            "obra_relacionada": "773 $w – Número de control (001)",
        }


# ========================================================================
# 774 – Enlace a unidad constituyente
# ========================================================================
class EnlaceUnidadConstituyente774Form(forms.ModelForm):
    # Campo visible tipo "Muscat"
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="774 $a – Encabezamiento principal",
        widget=forms.TextInput(
            attrs={
                "class": "form-control autoridad-input",
                "placeholder": "Buscar en Autoridades de Personas…",
                "autocomplete": "off",
                "data-autoridad-input": "1",
                "data-hidden-field": "encabezamiento_principal",
            }
        ),
    )

    titulo_texto = forms.CharField(
        required=False,
        label="774 $t – Título",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar en Títulos Uniformes…",
                "autocomplete": "off",
                "data-autocomplete": "titulo",
                "data-hidden-field": "titulo",
            }
        ),
    )

    class Meta:
        model = EnlaceUnidadConstituyente774
        fields = ["encabezamiento_principal", "titulo"]
        widgets = {
            # Campo real oculto
            "encabezamiento_principal": forms.HiddenInput(),
            "titulo": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["encabezamiento_principal"].required = False
        self.fields["titulo"].required = False

        if self.instance.pk:
            if self.instance.encabezamiento_principal_id:
                self.fields[
                    "encabezamiento_principal_texto"
                ].initial = self.instance.encabezamiento_principal.apellidos_nombres
            if self.instance.titulo_id:
                self.fields["titulo"].initial = str(self.instance.titulo_id)
                self.fields["titulo_texto"].initial = self.instance.titulo.titulo

    def clean(self):
        data = super().clean()

        encabez = data.get("encabezamiento_principal")
        encabez_texto = data.get("encabezamiento_principal_texto", "").strip()

        # --- Normalizar valor de título ---
        titulo_value = data.get("titulo")  # puede ser objeto, string o None

        if hasattr(titulo_value, "pk"):
            # Es un objeto AutoridadTituloUniforme
            titulo_field = titulo_value.titulo
        else:
            # Es string o None
            titulo_field = (titulo_value or "").strip()

        titulo_texto = data.get("titulo_texto", "").strip()

        # 🟩 1. Formulario completamente vacío → eliminar
        # Si está totalmente vacío → eliminarlo
        if not (encabez or encabez_texto or titulo_field or titulo_texto):
            self.cleaned_data["DELETE"] = True
            return data

        # Si hay título pero no encabezamiento → ERROR
        if (titulo_field or titulo_texto) and not (encabez or encabez_texto):
            self.add_error(
                "encabezamiento_principal_texto",
                "Debe ingresar un encabezamiento para 774 $a si incluye un título.",
            )
            return data

        # 🟩 2. Resolver encabezamiento principal
        if encabez_texto and not encabez:
            persona = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=encabez_texto
            ).first()
            if not persona:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=encabez_texto
                )
            data["encabezamiento_principal"] = persona

        # 🟩 3. Resolver título uniforme
        titulo_obj = None

        # Caso 1: ya vino como objeto FK
        if hasattr(titulo_value, "pk"):
            titulo_obj = titulo_value

        # Caso 2: vino como ID string
        elif titulo_field.isdigit():
            titulo_obj = AutoridadTituloUniforme.objects.filter(
                pk=int(titulo_field)
            ).first()

        # Caso 3: buscar por texto
        if not titulo_obj and titulo_texto:
            titulo_obj = AutoridadTituloUniforme.objects.filter(
                titulo__iexact=titulo_texto
            ).first()
            if not titulo_obj:
                titulo_obj = AutoridadTituloUniforme.objects.create(titulo=titulo_texto)

        # Validar que sí exista título
        if titulo_obj:
            data["titulo"] = titulo_obj
        else:
            self.add_error(
                "titulo_texto", "Debe ingresar o seleccionar un título para 774 $t."
            )

        return data


class NumeroControl774Form(forms.ModelForm):
    class Meta:
        model = NumeroControl774
        fields = ["obra_relacionada"]
        widgets = {
            "obra_relacionada": Select2Widget(
                attrs={
                    "data-url": "/catalogacion/autocompletar/obra/",
                }
            )
        }
        labels = {
            "obra_relacionada": "774 $w – Número de control (001)",
        }


# ========================================================================
# 787 – Otras relaciones
# ========================================================================


class OtrasRelaciones787Form(forms.ModelForm):
    encabezamiento_principal_texto = forms.CharField(
        required=False,
        label="787 $a – Encabezamiento principal",
        widget=forms.TextInput(
            attrs={
                "class": "form-control autocomplete-787",
                "placeholder": "Escriba para buscar o agregar…",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = OtrasRelaciones787
        fields = ["encabezamiento_principal", "titulo"]
        widgets = {
            "encabezamiento_principal": forms.HiddenInput(),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "data-autocomplete": "titulo",
                    "autocomplete": "off",
                }
            ),
        }

    def clean(self):
        data = super().clean()

        encabez = data.get("encabezamiento_principal")
        encabez_texto = data.get("encabezamiento_principal_texto", "").strip()
        titulo = data.get("titulo", "").strip()

        # 🟥 1. Form vacío → eliminarlo
        if not (encabez or encabez_texto or titulo):
            self.cleaned_data["DELETE"] = True
            return data

        # 🟥 2. Resolver/crear encabezamiento principal
        if encabez_texto and not encabez:
            persona = AutoridadPersona.objects.filter(
                apellidos_nombres__iexact=encabez_texto
            ).first()
            if not persona:
                persona = AutoridadPersona.objects.create(
                    apellidos_nombres=encabez_texto
                )
            data["encabezamiento_principal"] = persona

        # 🟥 3. Registrar título si existe
        if titulo:
            ensure_titulo_uniforme_registrado(titulo)

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitir que el formulario esté completamente vacío y sea marcado para borrado
        # evitando errores de "This field is required" a nivel de campo.
        if "encabezamiento_principal" in self.fields:
            self.fields["encabezamiento_principal"].required = False
        if "titulo" in self.fields:
            self.fields["titulo"].required = False


class NumeroControl787Form(forms.ModelForm):
    class Meta:
        model = NumeroControl787
        fields = ["obra_relacionada"]
        widgets = {
            "obra_relacionada": Select2Widget(
                attrs={
                    "data-url": "/catalogacion/autocompletar/obra/",
                }
            )
        }
        labels = {
            "obra_relacionada": "787 $w – Número de control (001)",
        }
