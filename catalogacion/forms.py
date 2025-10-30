from django import forms
from .models import ObraGeneral

class ObraForm(forms.ModelForm):
    class Meta:
        model = ObraGeneral
        fields = ['tipo_registro', 'nivel_bibliografico', 'descripcion']
        widgets = {
            'tipo_registro': forms.Select(attrs={'class': 'form-select'}),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción opcional'}),
        }
