# """
# Vistas Bloque 1XX - Puntos de Acceso Principal
# ==============================================

# Gestion de campos MARC21 del bloque 1XX (Puntos de acceso principal).

# Campos incluidos:
# - 100: Punto de acceso principal - Nombre de persona (Compositor)
# - 130: Punto de acceso principal - Titulo uniforme
# - 240: Titulo uniforme

# Subcampos relacionados:
# - Funciones del compositor
# - Atribuciones del compositor
# - Formas musicales (130/240)
# - Medio de interpretacion (130/240)
# - Numero de parte/seccion (130/240)
# - Nombre de parte/seccion (130/240)
# """

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages

# from django.db import transaction
# from ..models import (
#     ObraGeneral,
#     FuncionCompositor,
#     AtribucionCompositor,
#     Forma130,
#     MedioInterpretacion130,
#     NumeroParteSeccion130,
#     NombreParteSeccion130,
#     Forma240,
#     MedioInterpretacion240,
#     NumeroParteSeccion240,
#     NombreParteSeccion240,
#     AutoridadPersona,
#     AutoridadTituloUniforme,
#     AutoridadFormaMusical,
# )


# from ..forms import (
#     FuncionCompositorFormSet,
#     AtribucionCompositorFormSet,
#     Forma130FormSet,
#     MedioInterpretacion130FormSet,
#     NumeroParteSeccion130FormSet,
#     NombreParteSeccion130FormSet,
#     Forma240FormSet,
#     MedioInterpretacion240FormSet,
#     NumeroParteSeccion240FormSet,
#     NombreParteSeccion240FormSet,
# )

# # =============================================================================
# # FUNCIONES DE PROCESAMIENTO MASIVO (para formulario principal de obra_general)
# # =============================================================================
# def procesar_compositor(request, obra):
#     """
#     Procesa todos los campos 100 - Compositor desde el formulario principal
    
#     Maneja:
#     - Compositor con AutoridadPersona ($a y $d)
#     - Funciones de compositor ($e) - repetibles
#     - Atribuciones ($j) - repetibles
    
#     Args:
#         request: HttpRequest con datos POST
#         obra: Instancia de ObraGeneral
#     """
#     # Obtener datos del compositor
#     apellidos_nombres = request.POST.get('compositor_apellidos_nombres', '').strip()
#     fechas = request.POST.get('compositor_fechas', '').strip()
    
#     if apellidos_nombres:
#         # Crear o recuperar la autoridad de persona
#         # Si existe con el mismo nombre, actualiza las fechas si son diferentes
#         persona, created = AutoridadPersona.objects.get_or_create(
#             apellidos_nombres=apellidos_nombres,
#             defaults={'fechas': fechas}
#         )
        
#         # Si ya existe pero tiene fechas diferentes, actualizar
#         if not created and fechas and persona.fechas != fechas:
#             persona.fechas = fechas
#             persona.save()
        
#         # Asignar compositor a la obra
#         obra.compositor = persona
#         obra.save()
        
#         # Procesar funciones del compositor ($e) - repetibles
#         idx = 0
#         while True:
#             funcion = request.POST.get(f'funcion_compositor_e_{idx}')
#             if funcion is None:
#                 break
#             if funcion.strip():
#                 FuncionCompositor.objects.create(
#                     obra=obra,
#                     funcion=funcion.strip()
#                 )
#             idx += 1
        
#         # Procesar atribución ($j) - NR (No Repetible)
#         atribucion = request.POST.get('atribucion_compositor_j', '').strip()
#         if atribucion:
#             obra.atribucion_compositor = atribucion
#             obra.save()


# def procesar_titulo_uniforme_130(request, obra):
#     """
#     Procesa el campo 130 - Titulo Uniforme Musical (solo si NO hay compositor)
    
#     Maneja:
#     - Titulo uniforme base ($a)
#     - Arreglo ($o)
#     - Tonalidad ($r)
#     - Subcampos $k, $m, $n, $p (procesados por procesar_subcampos_130)
    
#     Args:
#         request: HttpRequest con datos POST
#         obra: Instancia de ObraGeneral
#     """
#     titulo_130 = request.POST.get('titulo_uniforme_130', '').strip()
#     arreglo_130 = request.POST.get('titulo_uniforme_arreglo', '').strip()
#     tonalidad_130 = request.POST.get('titulo_uniforme_tonalidad', '').strip()
    
#     if titulo_130:
#         # Crear o recuperar autoridad de titulo uniforme
#         titulo_autoridad, created = AutoridadTituloUniforme.objects.get_or_create(
#             titulo=titulo_130
#         )
        
#         # Asignar a la obra
#         obra.titulo_uniforme = titulo_autoridad
        
#         # Asignar arreglo si existe
#         if arreglo_130:
#             obra.titulo_uniforme_arreglo = arreglo_130
        
#         # Asignar tonalidad si existe
#         if tonalidad_130:
#             obra.titulo_uniforme_tonalidad = tonalidad_130
            
#         obra.save()
        
#         # Procesar subcampos $k, $m, $n, $p
#         procesar_subcampos_130(request, obra)


# def procesar_subcampos_130(request, obra):
#     """
#     Procesa los subcampos del campo 130 - Titulo Uniforme
    
#     Maneja (ahora todos NR - No Repetibles):
#     - $k Forma musical (ForeignKey a AutoridadFormaMusical)
#     - $m Medio de interpretacion
#     - $n Numero de parte/seccion
#     - $p Nombre de parte/seccion
    
#     Args:
#         request: HttpRequest con datos POST
#         obra: Instancia de ObraGeneral
#     """
#     # Procesar $k - Forma musical (NR, con autoridad)
#     forma_nombre = request.POST.get('forma_130_k', '').strip()
#     if forma_nombre:
#         forma_autoridad, created = AutoridadFormaMusical.objects.get_or_create(
#             forma=forma_nombre
#         )
#         obra.forma_130 = forma_autoridad
    
#     # Procesar $m - Medio de interpretacion (NR)
#     medio = request.POST.get('medio_interpretacion_130_m', '').strip()
#     if medio:
#         obra.medio_interpretacion_130 = medio
    
#     # Procesar $n - Numero de parte/seccion (NR)
#     numero = request.POST.get('numero_parte_130_n', '').strip()
#     if numero:
#         obra.numero_parte_130 = numero
    
#     # Procesar $p - Nombre de parte/seccion (NR)
#     nombre = request.POST.get('nombre_parte_130_p', '').strip()
#     if nombre:
#         obra.nombre_parte_130 = nombre
    
#     if forma_nombre or medio or numero or nombre:
#         obra.save()


# def procesar_titulo_uniforme_240(request, obra):
#     """
#     Procesa el campo 240 - Titulo Uniforme con Compositor (solo si HAY compositor)
    
#     Maneja:
#     - Titulo uniforme base ($a)
#     - Arreglo ($o)
#     - Tonalidad ($r)
#     - Subcampos $k, $m, $n, $p (procesados por procesar_subcampos_240)
    
#     Args:
#         request: HttpRequest con datos POST
#         obra: Instancia de ObraGeneral
#     """
#     titulo_240 = request.POST.get('titulo_240', '').strip()
#     arreglo_240 = request.POST.get('titulo_240_arreglo', '').strip()
#     tonalidad_240 = request.POST.get('titulo_240_tonalidad', '').strip()
    
#     if titulo_240:
#         # Crear o recuperar autoridad de titulo uniforme
#         titulo_autoridad, created = AutoridadTituloUniforme.objects.get_or_create(
#             titulo=titulo_240
#         )
        
#         # Asignar a la obra
#         obra.titulo_240 = titulo_autoridad
        
#         # Asignar arreglo si existe
#         if arreglo_240:
#             obra.titulo_240_arreglo = arreglo_240
        
#         # Asignar tonalidad si existe
#         if tonalidad_240:
#             obra.titulo_240_tonalidad = tonalidad_240
            
#         obra.save()
        
#         # Procesar subcampos $k, $m, $n, $p
#         procesar_subcampos_240(request, obra)


# def procesar_subcampos_240(request, obra):
#     """
#     Procesa los subcampos del campo 240 - Titulo Uniforme con Compositor
    
#     Maneja (ahora todos NR - No Repetibles):
#     - $k Forma musical (ForeignKey a AutoridadFormaMusical)
#     - $m Medio de interpretacion
#     - $n Numero de parte/seccion
#     - $p Nombre de parte/seccion
    
#     Args:
#         request: HttpRequest con datos POST
#         obra: Instancia de ObraGeneral
#     """
#     # Procesar $k - Forma musical (NR, con autoridad)
#     forma_nombre = request.POST.get('forma_240_k', '').strip()
#     if forma_nombre:
#         forma_autoridad, created = AutoridadFormaMusical.objects.get_or_create(
#             forma=forma_nombre
#         )
#         obra.forma_240 = forma_autoridad
    
#     # Procesar $m - Medio de interpretacion (NR)
#     medio = request.POST.get('medio_interpretacion_240_m', '').strip()
#     if medio:
#         obra.medio_interpretacion_240 = medio
    
#     # Procesar $n - Numero de parte/seccion (NR)
#     numero = request.POST.get('numero_parte_240_n', '').strip()
#     if numero:
#         obra.numero_parte_240 = numero
    
#     # Procesar $p - Nombre de parte/seccion (NR)
#     nombre = request.POST.get('nombre_parte_240_p', '').strip()
#     if nombre:
#         obra.nombre_parte_240 = nombre
    
#     if forma_nombre or medio or numero or nombre:
#         obra.save()