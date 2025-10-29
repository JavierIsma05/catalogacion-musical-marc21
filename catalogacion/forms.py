from django import forms
from .models import ObraMarc

class ObraMarcForm(forms.ModelForm):
    class Meta:
        model = ObraMarc
        fields = '__all__'
        widgets = {
            'notacion_token': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ejemplo: #@%G4^/A#FGB...'}),
            'nota_general': forms.Textarea(attrs={'rows': 3}),
        }
