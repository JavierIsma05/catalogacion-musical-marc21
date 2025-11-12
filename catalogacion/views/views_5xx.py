"""
Vistas Bloque 5XX - Notas
=========================
Gestión de campos MARC21 del bloque 5XX (Notas y descripciones).

Campos incluidos:
- 500: Nota general
- 505: Contenido
- 545: Nota biográfica del compositor
"""

from ..models import (
    ObraGeneral,
    NotaGeneral500,
    NotaContenido505,
    NotaBiografica545,
)


# ================================================
# FUNCIONES DE PROCESAMIENTO PARA crear_obra()
# ================================================

def procesar_nota_general_500(request, obra):
    """500 ## $a Nota general (R)"""
    idx = 0
    while True:
        nota = request.POST.get(f'nota_general_500_a_{idx}', '').strip()
        if nota:
            NotaGeneral500.objects.create(obra=obra, nota_general=nota)
        else:
            if idx > 20:
                break
        idx += 1


def procesar_nota_contenido_505(request, obra):
    """505 ## $a Contenido (R)"""
    idx = 0
    while True:
        contenido = request.POST.get(f'nota_contenido_505_a_{idx}', '').strip()
        if contenido:
            NotaContenido505.objects.create(obra=obra, contenido=contenido)
        else:
            if idx > 20:
                break
        idx += 1


def procesar_nota_biografica_545(request, obra):
    """
    545 ## $a Datos biográficos del compositor (R)
           $u URL (R)
    """
    idx = 0
    while True:
        bio = request.POST.get(f'nota_biografica_545_a_{idx}', '').strip()
        url = request.POST.get(f'nota_biografica_545_u_{idx}', '').strip()

        if bio or url:
            NotaBiografica545.objects.create(
                obra=obra,
                datos_biograficos=bio or '',
                url=url or ''
            )
        else:
            if idx > 20:
                break
        idx += 1
