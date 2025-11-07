"""
Vistas Bloque 6XX - Materias y Género/Forma
============================================

Gestión de campos MARC21 del bloque 6XX.

Campos incluidos:
- 650: Materia (R)
- 655: Género/Forma (R)
"""

from django.shortcuts import get_object_or_404
from ..models import (
    ObraGeneral,
    Materia650,
    SubdivisionMateria650,
    MateriaGenero655,
    SubdivisionGeneral655,
)

# ============================================================
# FUNCIONES DE PROCESAMIENTO MASIVO - GUARDADO DE OBRA
# ============================================================

def procesar_6xx(request, obra):
    """Procesa todos los campos del bloque 6XX."""
    procesar_materia_650(request, obra)
    procesar_genero_forma_655(request, obra)


# ------------------------------
# 650 - Materia (R)
# ------------------------------
def procesar_materia_650(request, obra):
    """
    Procesa múltiples Materias (650)
    Campos esperados:
        materia_a_0, materia_a_1, ...
        materia_x_0_0, materia_x_0_1, ... (subdivisiones de materia 0)
    """
    index = 0
    while True:
        tema = request.POST.get(f'materia_a_{index}')
        if not tema:
            break

        if tema.strip():
            # Crear la materia principal
            materia = Materia650.objects.create(
                obra=obra,
                materia=tema.strip()
            )

            # Procesar subdivisiones ($x)
            sub_index = 0
            while True:
                subdiv = request.POST.get(f'materia_x_{index}_{sub_index}')
                if not subdiv:
                    break

                if subdiv.strip():
                    SubdivisionMateria650.objects.create(
                        materia=materia,
                        subdivision=subdiv.strip()
                    )

                sub_index += 1

        index += 1


# ------------------------------
# 655 - Género/Forma (R)
# ------------------------------
def procesar_genero_forma_655(request, obra):
    """
    Procesa múltiples Géneros/Formas (655)
    Campos esperados:
        genero_a_0, genero_a_1, ...
        genero_x_0_0, genero_x_0_1, ... (subdivisiones generales)
    """
    index = 0
    while True:
        genero = request.POST.get(f'genero_a_{index}')
        if not genero:
            break

        if genero.strip():
            gen = MateriaGenero655.objects.create(
                obra=obra,
                genero_forma=genero.strip()
            )

            # Subdivisiones ($x)
            sub_index = 0
            while True:
                subdiv = request.POST.get(f'genero_x_{index}_{sub_index}')
                if not subdiv:
                    break

                if subdiv.strip():
                    SubdivisionGeneral655.objects.create(
                        genero=gen,
                        subdivision=subdiv.strip()
                    )

                sub_index += 1

        index += 1
