from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def plantillas(request):
    return render(request, 'plantillas.html')

def crear_obra(request):
    return render(request, 'crear_obra.html')
