"""
Vistas Bloque 8XX – Ubicación y Disponibilidad
==============================================
Gestión de campos MARC21 del bloque 8XX.

Campos incluidos:
- 852: Ubicación (R)
- 856: Disponible (R)
"""

from django.shortcuts import get_object_or_404
from ..models import (
    ObraGeneral,
    Ubicacion852,
    Estanteria852,
    Disponible856,
)

# ============================================================
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO MASIVO
# ============================================================

def procesar_8xx(request, obra):
    """
    Procesa todos los campos del bloque 8XX.
    Se ejecuta al guardar la obra principal.
    """
    procesar_ubicaciones_852(request, obra)
    procesar_disponibles_856(request, obra)


# ============================================================
# 852 ## Ubicación (R)
# ============================================================

def procesar_ubicaciones_852(request, obra):
    """
    Procesa los datos de ubicación (852).
    Campos esperados:
      - ubicacion_a_0, ubicacion_a_1, ...
      - ubicacion_h_0, ubicacion_h_1, ...
      - estanteria_c_0_0, estanteria_c_0_1, ...
    """
    index = 0
    while True:
        institucion = request.POST.get(f'ubicacion_a_{index}')
        signatura = request.POST.get(f'ubicacion_h_{index}')
        if not institucion and not signatura:
            break

        if institucion or signatura:
            ubicacion = Ubicacion852.objects.create(
                obra=obra,
                institucion_persona=institucion.strip() if institucion else "",
                signatura_original=signatura.strip() if signatura else None
            )

            # Subcampos repetibles $c – Estantería
            subindex = 0
            while True:
                estanteria = request.POST.get(f'estanteria_c_{index}_{subindex}')
                if not estanteria:
                    break

                if estanteria.strip():
                    Estanteria852.objects.create(
                        ubicacion=ubicacion,
                        estanteria=estanteria.strip()
                    )
                subindex += 1

        index += 1


# ============================================================
# 856 4# Disponible (R)
# ============================================================

def procesar_disponibles_856(request, obra):
    """
    Procesa los datos de recursos disponibles (856).
    Campos esperados:
      - disponible_u_0, disponible_u_1, ...
      - disponible_y_0, disponible_y_1, ...
    """
    index = 0
    while True:
        url = request.POST.get(f'disponible_u_{index}')
        texto = request.POST.get(f'disponible_y_{index}')
        if not url and not texto:
            break

        if url or texto:
            Disponible856.objects.create(
                obra=obra,
                url=url.strip() if url else "",
                texto_enlace=texto.strip() if texto else None
            )
        index += 1


# ============================================================
# 🔍 Función de depuración (opcional)
# ============================================================


