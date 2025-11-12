"""
Vistas Bloque 6XX - Materias
============================
Gestión de campos MARC21 del bloque 6XX (Términos de materia).

Campos incluidos:
- 650: Materia (temática general)
- 655: Género/Forma
"""

from ..models import (
    ObraGeneral,
    Materia650,
    MateriaGenero655,
)


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_materia_650(request, obra):
    """650 ## $a Materia (R)"""
    idx = 0
    while True:
        materia = request.POST.get(f'materia_650_a_{idx}', '').strip()
        if materia:
            Materia650.objects.create(obra=obra, materia=materia)
        else:
            if idx > 20:
                break
        idx += 1


def procesar_materia_genero_655(request, obra):
    """655 ## $a Género/Forma (R)"""
    idx = 0
    while True:
        genero = request.POST.get(f'materia_genero_655_a_{idx}', '').strip()
        if genero:
            MateriaGenero655.objects.create(obra=obra, genero_forma=genero)
        else:
            if idx > 20:
                break
        idx += 1
