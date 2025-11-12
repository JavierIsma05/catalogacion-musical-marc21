"""
Vistas Bloque 8XX - Ubicación y Disponibilidad
==============================================
Gestión de campos MARC21 del bloque 8XX.

Campos incluidos:
- 852: Ubicación
- 856: Disponible en línea
"""

from ..models import (
    ObraGeneral,
    Estanteria852,
    Disponible856,
)


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_ubicacion_852(request, obra):
    """
    852 ## Subcampos:
      - $c Estantería (R)
    """
    idx = 0
    while True:
        estanteria = request.POST.get(f'ubicacion_852_c_{idx}', '').strip()
        if estanteria:
            Estanteria852.objects.create(obra=obra, estanteria=estanteria)
        else:
            if idx > 20:
                break
        idx += 1


def procesar_disponible_856(request, obra):
    """
    856 ## Subcampos:
      - $u URL (R)
      - $y Texto del enlace (R)
    """
    idx = 0
    while True:
        url = request.POST.get(f'disponible_856_u_{idx}', '').strip()
        texto = request.POST.get(f'disponible_856_y_{idx}', '').strip()

        if url or texto:
            Disponible856.objects.create(
                obra=obra,
                url=url or '',
                texto_enlace=texto or ''
            )
        else:
            if idx > 20:
                break
        idx += 1
