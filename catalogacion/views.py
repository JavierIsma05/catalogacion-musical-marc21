from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def plantillas(request):
    return render(request, 'plantillas.html')

def crear_obra(request):
    return render(request, 'crear_obra.html')

# este obra_general vamos a usar para ir rellenando los campos de la obra general en base al excel 
# los otros segun veo son herencias del general pero igual hagamos este genral en base al excel 
# en el mismo excel se visualiza que campos son para manuscrita y cuales para impresa
# pero a mi modo de verlo todos son campos de la obra general que si bien no se va a visualizar de momento si pongamolo como
# si fuese el padre de los demas
def obra_general(request):
    
    return render(request, 'ObraGeneral/obra_general.html')

def coleccion_manuscrita(request):
    return render(request, 'ColeccionManuscrita/col_man.html')

def obra_individual_manuscrita(request):
    return render(request, 'ColeccionManuscrita/obra_in_man.html')

def coleccion_impresa(request):
    return render(request, 'ColeccionImpresa/col_imp.html')

def obra_individual_impresa(request):
    return render(request, 'ColeccionImpresa/obra_in_imp.html')