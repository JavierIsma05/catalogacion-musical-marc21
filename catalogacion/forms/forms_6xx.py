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
    """Formulario para campo 650 – Materia (Tema)"""

    materia = forms.ModelChoiceField(
        label="650 $a – Encabezamiento de materia",
        queryset=AutoridadMateria.objects.all().order_by("termino"),
        widget=Select2Widget(attrs={
            "class": "materia-autocomplete",
            "data-url": "/catalogacion/api/autocompletar/materia/",
            "placeholder": "Buscar o crear materia…"
        }),
        required=False,
    )

    class Meta:
        model = Materia650
        fields = ["materia"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # IF editing an existing Materia650, ensure the current one appears preloaded
        if self.instance.pk and self.instance.materia:
            self.fields["materia"].initial = self.instance.materia


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

        # si ya existe, mostrar el texto en el input visible
        if self.instance.pk and self.instance.materia:
            self.fields['materia_texto'].initial = self.instance.materia.forma

    def clean(self):
        cleaned = super().clean()

        texto = cleaned.get("materia_texto")
        materia_id = cleaned.get("materia")

        if materia_id:
            # ya seleccionado — ok
            return cleaned

        if texto and texto.strip():
            texto = texto.strip()

            # buscar si ya existe
            existente = AutoridadFormaMusical.objects.filter(
                forma__iexact=texto
            ).first()

            if existente:
                cleaned["materia"] = existente.id
            else:
                # crear un nuevo término
                nuevo = AutoridadFormaMusical.objects.create(forma=texto)
                cleaned["materia"] = nuevo.id

        return cleaned
