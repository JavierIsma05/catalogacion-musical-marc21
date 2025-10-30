from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def plantillas(request):
    return render(request, 'plantillas.html')

def crear_obra(request):
    return render(request, 'crear_obra.html')

def coleccion_manuscrita(request):
    return render(request, 'ColeccionManuscrita/col_man.html')

def obra_individual_manuscrita(request):
    return render(request, 'ColeccionManuscrita/obra_in_man.html')

def coleccion_impresa(request):
    return render(request, 'ColeccionImpresa/col_imp.html')

def obra_individual_impresa(request):
    return render(request, 'ColeccionImpresa/obra_in_imp.html')