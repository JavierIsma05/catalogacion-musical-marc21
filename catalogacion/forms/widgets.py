"""
Widgets personalizados para formularios MARC21
"""
from django import forms


class Select2Widget(forms.Select):
    """Widget Select2 para autocompletado de autoridades"""
    
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            'class': 'form-select select2',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)
    
    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/select2@4.1.0/dist/css/select2.min.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/select2@4.1.0/dist/js/select2.min.js',
        )


class DatePickerWidget(forms.DateInput):
    """Widget de selección de fecha"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control datepicker',
            'type': 'date',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, format='%Y-%m-%d')


class TextAreaAutosize(forms.Textarea):
    """Textarea que se autoajusta al contenido"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control autosize-textarea',
            'rows': 3,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
