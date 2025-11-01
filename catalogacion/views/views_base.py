"""
Vistas Base - Sistema de Catalogación MARC21 Musical
====================================================

Vistas generales de navegación y páginas principales.
No están relacionadas directamente con bloques MARC específicos.
"""

from django.shortcuts import render


def index(request):
    """
    Vista principal del sistema - Página de inicio
    
    Muestra enlaces a las diferentes secciones del sistema de catalogación.
    """
    return render(request, 'index.html')


def plantillas(request):
    """
    Vista de plantillas de catalogación
    
    Muestra las diferentes plantillas MARC21 disponibles para catalogación.
    """
    return render(request, 'plantillas.html')


def crear_obra(request):
    """
    Vista para iniciar la creación de una nueva obra
    
    Punto de entrada para crear registros MARC21 de obras musicales.
    """
    return render(request, 'crear_obra.html')


def coleccion_manuscrita(request):
    """
    Vista para gestión de colecciones manuscritas
    
    Lista y gestiona obras musicales manuscritas catalogadas.
    """
    return render(request, 'ColeccionManuscrita/col_man.html')


def obra_individual_manuscrita(request):
    """
    Vista de detalle para obra manuscrita individual
    
    Muestra el detalle completo de una obra musical manuscrita.
    """
    return render(request, 'ColeccionManuscrita/obra_in_man.html')


def coleccion_impresa(request):
    """
    Vista para gestión de colecciones impresas
    
    Lista y gestiona obras musicales impresas catalogadas.
    """
    return render(request, 'ColeccionImpresa/col_imp.html')


def obra_individual_impresa(request):
    """
    Vista de detalle para obra impresa individual
    
    Muestra el detalle completo de una obra musical impresa.
    """
    return render(request, 'ColeccionImpresa/obra_in_imp.html')
