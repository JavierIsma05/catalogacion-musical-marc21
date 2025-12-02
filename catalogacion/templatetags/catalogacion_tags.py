"""
Template tags para la aplicación de catalogación
Proporciona acceso a constantes y utilidades en los templates
"""
import json
from django import template
from catalogacion.models.constantes import (
    CODIGOS_LENGUAJE,
    CODIGOS_PAIS,
    MEDIOS_INTERPRETACION,
    TONALIDADES,
    TECNICAS,
    FORMATOS,
    FUNCIONES_PERSONA,
    FUNCIONES_ENTIDAD,
    AUTORIAS_CHOICES,
)

register = template.Library()


@register.simple_tag
def get_codigos_lenguaje():
    """Retorna la lista de códigos de lenguaje"""
    return CODIGOS_LENGUAJE


@register.simple_tag
def get_codigos_lenguaje_json():
    """Retorna la lista de códigos de lenguaje en formato JSON para JavaScript"""
    data = [{'codigo': codigo, 'nombre': nombre} for codigo, nombre in CODIGOS_LENGUAJE]
    return json.dumps(data, ensure_ascii=False)


@register.simple_tag
def get_codigos_pais():
    """Retorna la lista de códigos de país"""
    return CODIGOS_PAIS


@register.simple_tag
def get_codigos_pais_json():
    """Retorna la lista de códigos de país en formato JSON para JavaScript"""
    data = [{'codigo': codigo, 'nombre': nombre} for codigo, nombre in CODIGOS_PAIS]
    return json.dumps(data, ensure_ascii=False)


@register.simple_tag
def get_medios_interpretacion():
    """Retorna la lista de medios de interpretación"""
    return MEDIOS_INTERPRETACION


@register.simple_tag
def get_medios_interpretacion_json():
    """Retorna la lista de medios de interpretación en formato JSON para JavaScript"""
    data = [{'codigo': codigo, 'nombre': nombre} for codigo, nombre in MEDIOS_INTERPRETACION]
    return json.dumps(data, ensure_ascii=False)


@register.simple_tag
def get_tonalidades():
    """Retorna la lista de tonalidades"""
    return TONALIDADES


@register.simple_tag
def get_tecnicas():
    """Retorna la lista de técnicas"""
    return TECNICAS


@register.simple_tag
def get_formatos():
    """Retorna la lista de formatos"""
    return FORMATOS


@register.simple_tag
def get_funciones_persona():
    """Retorna la lista de funciones de persona"""
    return FUNCIONES_PERSONA


@register.simple_tag
def get_funciones_entidad():
    """Retorna la lista de funciones de entidad"""
    return FUNCIONES_ENTIDAD


@register.simple_tag
def get_autorias():
    """Retorna la lista de tipos de autoría"""
    return AUTORIAS_CHOICES
