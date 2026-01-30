#!/usr/bin/env python
"""Script para crear datos de prueba con covers"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from catalogacion.models import ObraGeneral
from digitalizacion.models import DigitalSet, DigitalPage, WorkSegment
from pathlib import Path

# Tomar una obra existente
obra = ObraGeneral.objects.activos().first()
if not obra:
    print("No hay obras activas")
    exit()

print(f"Usando obra: {obra.id} - {obra.titulo_principal}")

# 1. Crear un DigitalSet (simulando colección digitalizada)
ds, created = DigitalSet.objects.get_or_create(
    coleccion_id=obra.id,
    defaults={
        'estado': 'IMPORTADO',
        'total_pages': 10,
        'repository_path': '/media/digitalizado/coleccion_001/',
    }
)
print(f"DigitalSet: {ds} (creado={created})")

# 2. Crear una página con derivative (la imagen del cover)
# Simulamos que existe un archivo JPG
dp, created = DigitalPage.objects.get_or_create(
    digital_set=ds,
    page_number=1,
    defaults={
        'master_path': '/media/tif/page_001.tif',
        'derivative_path': 'derivatives/page_001.jpg',  # Esta es la ruta relativa
    }
)
print(f"DigitalPage: {dp} (creado={created})")

print("\nAhora deberia mostrar cover_url en el dashboard!")
