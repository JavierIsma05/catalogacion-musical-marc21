from django import forms
from .models import ObraGeneral

class ObraForm(forms.ModelForm):
    class Meta:
        model = ObraGeneral
        fields = [
            'tipo_registro', 'nivel_bibliografico',
            'isbn', 'ismn', 'numero_editor', 'indicador_028',
            'incipit_num_obra', 'incipit_num_movimiento', 'incipit_num_pasaje',
            'incipit_titulo', 'incipit_voz_instrumento', 'incipit_notacion', 'incipit_url',
            'centro_catalogador', 'codigo_lengua', 'codigo_pais',
            'clasif_institucion', 'clasif_proyecto', 'clasif_pais', 'clasif_ms_imp'
        ]
        widgets = {
            'tipo_registro': forms.Select(attrs={'class': 'form-select'}),
            'nivel_bibliografico': forms.Select(attrs={'class': 'form-select'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'ismn': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_editor': forms.TextInput(attrs={'class': 'form-control'}),
            'incipit_titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'incipit_notacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'incipit_url': forms.URLInput(attrs={'class': 'form-control'}),
            'codigo_lengua': forms.Select(attrs={'class': 'form-select'}),
            'codigo_pais': forms.Select(attrs={'class': 'form-select'}),
            'clasif_ms_imp': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'isbn': '020 $a – ISBN tomado tal como aparece en la fuente. Genera vista de usuario.',
            'ismn': '024 $a – ISMN tomado tal como aparece en la fuente. Genera vista de usuario.',
            'numero_editor': '028 $a – Número de plancha, placa o código distintivo del editor. Genera vista de usuario.',
            'indicador_028': "028 Indicador. Predeterminado '20', con opción de cambiar.",
            'incipit_num_obra': '031 $a – Número de la obra.',
            'incipit_num_movimiento': '031 $b – Número del movimiento.',
            'incipit_num_pasaje': '031 $c – Número de pasaje.',
            'incipit_titulo': '031 $d – Título o encabezamiento del íncipit.',
            'incipit_voz_instrumento': '031 $m – Voz o instrumento.',
            'incipit_notacion': '031 $p – Íncipit musical codificado.',
            'incipit_url': '031 $u – URL del íncipit en otra base de datos.',
            'centro_catalogador': '040 $a – Centro catalogador de origen (UNL).',
        }   