from django.shortcuts import render,redirect
from .models import ObraGeneral
# from .forms import (
#     ObraForm, 
#     TituloAlternativoFormSet, 
#     EdicionFormSet, 
#     ProduccionPublicacionFormSet
# )

# Importar vistas de prueba
from .views_prueba_300 import prueba_campo_300, limpiar_prueba_300

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

# def obra_general(request):
#     obras = ObraGeneral.objects.all().order_by('-id')
    
#     if request.method == 'POST':
#         form = ObraForm(request.POST)
#         formset_246 = TituloAlternativoFormSet(request.POST, prefix='titulo_alt')
#         formset_250 = EdicionFormSet(request.POST, prefix='edicion')
#         formset_264 = ProduccionPublicacionFormSet(request.POST, prefix='prod_pub')
        
#         if form.is_valid() and formset_246.is_valid() and formset_250.is_valid() and formset_264.is_valid():
#             obra = form.save()
            
#             # Guardar títulos alternativos
#             titulos = formset_246.save(commit=False)
#             for titulo in titulos:
#                 titulo.obra = obra
#                 titulo.save()
            
#             # Guardar ediciones
#             ediciones = formset_250.save(commit=False)
#             for edicion in ediciones:
#                 edicion.obra = obra
#                 edicion.save()
            
#             # Guardar producción/publicación
#             registros_264 = formset_264.save(commit=False)
#             for registro in registros_264:
#                 registro.obra = obra
#                 registro.save()
            
#             return redirect('obra_general')
#     else:
#         form = ObraForm()
#         formset_246 = TituloAlternativoFormSet(prefix='titulo_alt')
#         formset_250 = EdicionFormSet(prefix='edicion')
#         formset_264 = ProduccionPublicacionFormSet(prefix='prod_pub')
    
#     contexto = {
#         'form': form,
#         'formset_246': formset_246,
#         'formset_250': formset_250,
#         'formset_264': formset_264,
#         'obras': obras,
#     }
#     return render(request, 'ObraGeneral/obra_general.html', contexto)

def coleccion_manuscrita(request):
    return render(request, 'ColeccionManuscrita/col_man.html')

def obra_individual_manuscrita(request):
    return render(request, 'ColeccionManuscrita/obra_in_man.html')

def coleccion_impresa(request):
    return render(request, 'ColeccionImpresa/col_imp.html')

def obra_individual_impresa(request):
    return render(request, 'ColeccionImpresa/obra_in_imp.html')

# --------------------------------------------------------
# VISTA PARA OBTENER AUTORIDADES EN FORMATO JSON PARA SELECT2
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import AutoridadPersona, AutoridadTituloUniforme, AutoridadFormaMusical

@require_GET
def get_autoridades_json(request):
    """
    Endpoint para obtener autoridades en formato JSON para Select2
    """
    modelo = request.GET.get('model')
    busqueda = request.GET.get('q', '')
    
    resultados = []
    
    if modelo == 'compositor':
        if busqueda:
            query = AutoridadPersona.objects.filter(
                apellidos_nombres__icontains=busqueda
            )[:20]
        else:
            # Devolver todos si no hay búsqueda
            query = AutoridadPersona.objects.all()[:100]
        
        resultados = [
            {
                'id': p.apellidos_nombres,
                'text': f"{p.apellidos_nombres} {p.fechas}" if p.fechas else p.apellidos_nombres,
                'fechas': p.fechas
            }
            for p in query
        ]
    
    elif modelo == 'titulo_uniforme':
        if busqueda:
            query = AutoridadTituloUniforme.objects.filter(
                titulo__icontains=busqueda
            )[:20]
        else:
            query = AutoridadTituloUniforme.objects.all()[:100]
        
        resultados = [
            {'id': t.titulo, 'text': t.titulo}
            for t in query
        ]
    
    elif modelo == 'forma_musical':
        if busqueda:
            query = AutoridadFormaMusical.objects.filter(
                forma__icontains=busqueda
            )[:20]
        else:
            query = AutoridadFormaMusical.objects.all()[:100]
        
        resultados = [
            {'id': f.forma, 'text': f.forma}
            for f in query
        ]
    
    return JsonResponse({'results': resultados})

