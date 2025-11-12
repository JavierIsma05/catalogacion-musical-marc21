"""
Vistas Bloque 7XX - Entradas adicionales
========================================
Gestión de campos MARC21 del bloque 7XX (nombres, entidades, relaciones).

Campos incluidos:
- 700: Nombre relacionado
- 710: Entidad relacionada
- 773: Colección
- 774: Obra en esta colección
- 787: Otras relaciones
"""

from ..models import (
    ObraGeneral,
    TerminoAsociado700,
    Funcion700,
    Relacion700,
    Autoria700,
    FuncionEntidad710,
    NumeroDocumentoRelacionado773,
    NumeroObraRelacionada774,
    NumeroObraRelacionada787,
)


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_nombre_relacionado_700(request, obra):
    """
    700 ## Subcampos:
      - $c Término asociado al nombre (R)
      - $e Función (R)
      - $i Relación (R)
      - $j Autoría (R)
    """
    idx = 0
    while True:
        termino = request.POST.get(f'termino_asociado_700_c_{idx}', '').strip()
        funcion = request.POST.get(f'funcion_700_e_{idx}', '').strip()
        relacion = request.POST.get(f'relacion_700_i_{idx}', '').strip()
        autoria = request.POST.get(f'autoria_700_j_{idx}', '').strip()

        if any([termino, funcion, relacion, autoria]):
            if termino:
                TerminoAsociado700.objects.create(obra=obra, termino=termino)
            if funcion:
                Funcion700.objects.create(obra=obra, funcion=funcion)
            if relacion:
                Relacion700.objects.create(obra=obra, relacion=relacion)
            if autoria:
                Autoria700.objects.create(obra=obra, autoria=autoria)
        else:
            if idx > 30:
                break
        idx += 1


def procesar_entidad_relacionada_710(request, obra):
    """710 ## $e Función (R)"""
    idx = 0
    while True:
        funcion = request.POST.get(f'funcion_entidad_710_e_{idx}', '').strip()
        if funcion:
            FuncionEntidad710.objects.create(obra=obra, funcion=funcion)
        else:
            if idx > 30:
                break
        idx += 1


def procesar_coleccion_773(request, obra):
    """773 ## $w Número de documento fuente (R)"""
    idx = 0
    while True:
        numero = request.POST.get(f'coleccion_773_w_{idx}', '').strip()
        if numero:
            NumeroDocumentoRelacionado773.objects.create(obra=obra, numero_documento=numero)
        else:
            if idx > 30:
                break
        idx += 1


def procesar_obra_en_coleccion_774(request, obra):
    """774 ## $w Número de esta obra en la colección (R)"""
    idx = 0
    while True:
        numero = request.POST.get(f'obra_coleccion_774_w_{idx}', '').strip()
        if numero:
            NumeroObraRelacionada774.objects.create(obra=obra, numero_obra_relacionada=numero)
        else:
            if idx > 30:
                break
        idx += 1


def procesar_otras_relaciones_787(request, obra):
    """787 ## $w Número de obra relacionada (R)"""
    idx = 0
    while True:
        numero = request.POST.get(f'otras_relaciones_787_w_{idx}', '').strip()
        if numero:
            NumeroObraRelacionada787.objects.create(obra=obra, numero_obra_relacionada=numero)
        else:
            if idx > 30:
                break
        idx += 1
