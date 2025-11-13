"""
Vistas Bloque 5XX - Notas y Descripciones
=========================================

Gestión de campos MARC21 del bloque 5XX.

Campos incluidos:
- 500: Nota general (R)
- 505: Contenido (R)
- 520: Sumario (NR)
- 545: Datos biográficos del compositor (R)
"""

from django.shortcuts import get_object_or_404
from ..models import (
    ObraGeneral,
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
)

# ============================================================
# FUNCIONES DE PROCESAMIENTO MASIVO - GUARDADO DE OBRA
# ============================================================

def procesar_5xx(request, obra):
    """Procesa todos los campos del bloque 5XX."""
    procesar_nota_general_500(request, obra)
    procesar_contenido_505(request, obra)
    procesar_sumario_520(request, obra)
    procesar_datos_biograficos_545(request, obra)


# ------------------------------
# 500 - Nota general
# ------------------------------
def procesar_nota_general_500(request, obra):
    """
    Procesa múltiples notas generales (500)
    Campos esperados: nota_general_a_0, nota_general_a_1, ...
    """
    index = 0
    while True:
        valor = request.POST.get(f'nota_general_a_{index}')
        if not valor:
            break

        if valor.strip():
            NotaGeneral500.objects.create(
                obra=obra,
                nota_general=valor.strip()
            )
        index += 1


# ------------------------------
# 505 - Contenido
# ------------------------------
def procesar_contenido_505(request, obra):
    """
    Procesa múltiples contenidos (505)
    Campos esperados: contenido_a_0, contenido_a_1, ...
    """
    index = 0
    while True:
        valor = request.POST.get(f'contenido_a_{index}')
        if not valor:
            break

        if valor.strip():
            Contenido505.objects.create(
                obra=obra,
                contenido=valor.strip()
            )
        index += 1


# ------------------------------
# 520 - Sumario
# ------------------------------
def procesar_sumario_520(request, obra):
    """
    Procesa sumario (520)
    Campo esperado: sumario_a
    (no repetible)
    """
    valor = request.POST.get('sumario_a', '').strip()
    if valor:
        Sumario520.objects.create(
            obra=obra,
            sumario=valor
        )


# ------------------------------
# 545 - Datos biográficos del compositor
# ------------------------------
def procesar_datos_biograficos_545(request, obra):
    """
    Procesa datos biográficos del compositor (545)
    Campos esperados:
        biografia_a_0, biografia_a_1, ...
        biografia_u_0, biografia_u_1, ...
    """
    index = 0
    while True:
        datos = request.POST.get(f'biografia_a_{index}')
        url = request.POST.get(f'biografia_u_{index}')
        if not datos and not url:
            break

        if datos or url:
            DatosBiograficos545.objects.create(
                obra=obra,
                datos_biograficos=datos.strip() if datos else None,
                url=url.strip() if url else None
            )
        index += 1
