from django.shortcuts import render

# Create your views here.

'''
def formulario_marc21(request):
    return render(request, 'catalogacion/formulario.html')
'''

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ObraMarc
from .forms import ObraMarcForm

def formulario_marc21(request):
    if request.method == 'POST':
        form = ObraMarcForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Obra MARC guardada correctamente.")
            return redirect('formulario_marc21')
        else:
            messages.error(request, "⚠️ Verifica los campos, hay errores en el formulario.")
    else:
        form = ObraMarcForm()
    return render(request, 'catalogacion/formulario.html', {'form': form})
