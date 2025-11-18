"""
Formularios para bloque 4XX - Series
"""
from django import forms
from catalogacion.models import (
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
)


class MencionSerie490Form(forms.ModelForm):
    """
    Formulario para campo 490 - Mención de serie
    Los subcampos $a (título) y $v (volumen) se manejan con JavaScript
    """
    
    class Meta:
        model = MencionSerie490
        fields = []  # Sin campos directos, los subcampos se manejan con JavaScript
    
    def __str__(self):
        return "490 - Mención de serie"


# Los formularios TituloSerie490Form y VolumenSerie490Form no son necesarios
# porque los subcampos se manejan dinámicamente con JavaScript
