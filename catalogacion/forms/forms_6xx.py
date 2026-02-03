"""
Formularios para bloque 6XX - Materias
"""
from django import forms
from catalogacion.models import (
    Materia650,
    MateriaGenero655,
    AutoridadMateria,
    AutoridadFormaMusical,
)
from .widgets import Select2Widget


class Materia650Form(forms.ModelForm):

    materia_texto = forms.CharField(
        label="650 $a – Encabezamiento de materia",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control materia-input",
            "placeholder": "Escriba materia…",
            "autocomplete": "off",
        })
    )

    class Meta:
        model = Materia650
        fields = ["materia"]
        widgets = {
            "materia": forms.HiddenInput(attrs={"class": "materia-id"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer materia no requerido para permitir filas vacías en el formset
        self.fields["materia"].required = False

        if self.instance.pk and self.instance.materia:
            self.fields["materia_texto"].initial = self.instance.materia.termino
        elif not self.instance.pk:
            # Valor por defecto para nuevos registros
            self.fields["materia_texto"].initial = "Música para piano"

    def clean(self):
        cleaned = super().clean()
        texto = cleaned.get("materia_texto", "").strip()
        materia_id = cleaned.get("materia")

        # Si no hay texto ni ID → fila vacía, permitir
        if not texto and not materia_id:
            return cleaned

        # Si solo hay texto → buscarlo o crearlo
        if texto:
            existente = AutoridadMateria.objects.filter(
                termino__iexact=texto
            ).first()

            if existente:
                cleaned["materia"] = existente
            else:
                nuevo = AutoridadMateria.objects.create(termino=texto)
                cleaned["materia"] = nuevo

        return cleaned




class MateriaGenero655Form(forms.ModelForm):
    """Formulario para campo 655 con autocomplete (como 100 y 650)."""

    # campo visible
    materia_texto = forms.CharField(
        label="655 $a – Término de género/forma",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control genero-input",
            "placeholder": "Escriba género/forma…",
            "autocomplete": "off",
        })
    )

    class Meta:
        model = MateriaGenero655
        fields = ['materia']   # campo real (hidden en template)
        widgets = {
            'materia': forms.HiddenInput(attrs={
                "class": "genero-id"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer materia no requerido para permitir filas vacías en el formset
        self.fields['materia'].required = False

        # si ya existe, mostrar el texto en el input visible
        if self.instance.pk and self.instance.materia:
            self.fields['materia_texto'].initial = self.instance.materia.forma

    def clean(self):
        cleaned = super().clean()

        texto = cleaned.get("materia_texto")
        materia_id = cleaned.get("materia")

        # Si no hay texto ni ID → fila vacía, permitir
        if not texto and not materia_id:
            return cleaned

        if texto and texto.strip():
            texto = texto.strip()

            # buscar si ya existe
            existente = AutoridadFormaMusical.objects.filter(
                forma__iexact=texto
            ).first()

            if existente:
                cleaned["materia"] = existente
            else:
                # crear un nuevo término
                nuevo = AutoridadFormaMusical.objects.create(forma=texto)
                cleaned["materia"] = nuevo

        return cleaned
