#!/usr/bin/env python
"""
Script de prueba para intentar guardar una obra y capturar TODOS los logs.
Este script simula una solicitud POST a través del cliente de prueba de Django.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
import json
import logging

# Configurar logging para mostrar TODOS los mensajes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Cliente de prueba
client = Client()

# Datos POST mínimos para crear una obra
post_data = {
    # Formulario principal
    'tipo_registro': 'a',  # Text
    'nivel_bibliografico': 'm',  # Monograph
    'tipo_creacion_contenido': 'a',
    'tipo_control': 'a',
    'titulo_130': 'Test Obra',
    'medio_100': 'para piano',
    
    # Formsets vacíos pero con ManagementForm
    'incipits-TOTAL_FORMS': '1',
    'incipits-INITIAL_FORMS': '0',
    'incipits-0-id': '',
    'incipits-0-obra': '',
    
    'codigos_lengua-TOTAL_FORMS': '1',
    'codigos_lengua-INITIAL_FORMS': '0',
    'codigos_lengua-0-id': '',
    'codigos_lengua-0-obra': '',
    
    'codigos_pais-TOTAL_FORMS': '1',
    'codigos_pais-INITIAL_FORMS': '0',
    'codigos_pais-0-id': '',
    'codigos_pais-0-obra': '',
    
    # ... y así para todos los demás formsets
    'funciones_compositor-TOTAL_FORMS': '1',
    'funciones_compositor-INITIAL_FORMS': '0',
    'funciones_compositor-0-id': '',
    'funciones_compositor-0-obra': '',
    
    'medios_382-TOTAL_FORMS': '1',
    'medios_382-INITIAL_FORMS': '0',
    'medios_382-0-id': '',
    'medios_382-0-obra': '',
    'medios_382-0-DELETE': '',
    
    'titulos_alt-TOTAL_FORMS': '1',
    'titulos_alt-INITIAL_FORMS': '0',
    'titulos_alt-0-id': '',
    'titulos_alt-0-obra': '',
    
    'ediciones-TOTAL_FORMS': '1',
    'ediciones-INITIAL_FORMS': '0',
    'ediciones-0-id': '',
    'ediciones-0-obra': '',
    
    'produccion_publicacion-TOTAL_FORMS': '1',
    'produccion_publicacion-INITIAL_FORMS': '0',
    'produccion_publicacion-0-id': '',
    'produccion_publicacion-0-obra': '',
    
    'menciones_490-TOTAL_FORMS': '1',
    'menciones_490-INITIAL_FORMS': '0',
    'menciones_490-0-id': '',
    'menciones_490-0-obra': '',
    
    'notas_500-TOTAL_FORMS': '1',
    'notas_500-INITIAL_FORMS': '0',
    'notas_500-0-id': '',
    'notas_500-0-obra': '',
    
    'contenidos_505-TOTAL_FORMS': '1',
    'contenidos_505-INITIAL_FORMS': '0',
    'contenidos_505-0-id': '',
    'contenidos_505-0-obra': '',
    
    'sumarios_520-TOTAL_FORMS': '1',
    'sumarios_520-INITIAL_FORMS': '0',
    'sumarios_520-0-id': '',
    'sumarios_520-0-obra': '',
    
    'datos_biograficos_545-TOTAL_FORMS': '1',
    'datos_biograficos_545-INITIAL_FORMS': '0',
    'datos_biograficos_545-0-id': '',
    'datos_biograficos_545-0-obra': '',
    
    'materias_650-TOTAL_FORMS': '1',
    'materias_650-INITIAL_FORMS': '0',
    'materias_650-0-id': '',
    'materias_650-0-obra': '',
    'materias_650-0-materia': '',
    
    'materias_655-TOTAL_FORMS': '1',
    'materias_655-INITIAL_FORMS': '0',
    'materias_655-0-id': '',
    'materias_655-0-obra': '',
    'materias_655-0-genero': '',
    
    'nombres_700-TOTAL_FORMS': '1',
    'nombres_700-INITIAL_FORMS': '0',
    'nombres_700-0-id': '',
    'nombres_700-0-obra': '',
    
    'entidades_710-TOTAL_FORMS': '1',
    'entidades_710-INITIAL_FORMS': '0',
    'entidades_710-0-id': '',
    'entidades_710-0-obra': '',
    
    'enlaces_773-TOTAL_FORMS': '1',
    'enlaces_773-INITIAL_FORMS': '0',
    'enlaces_773-0-id': '',
    'enlaces_773-0-obra': '',
    
    'enlaces_774-TOTAL_FORMS': '1',
    'enlaces_774-INITIAL_FORMS': '0',
    'enlaces_774-0-id': '',
    'enlaces_774-0-obra': '',
    
    'relaciones_787-TOTAL_FORMS': '1',
    'relaciones_787-INITIAL_FORMS': '0',
    'relaciones_787-0-id': '',
    'relaciones_787-0-obra': '',
    
    'ubicaciones_852-TOTAL_FORMS': '1',
    'ubicaciones_852-INITIAL_FORMS': '0',
    'ubicaciones_852-0-id': '',
    'ubicaciones_852-0-obra': '',
    
    'disponibles_856-TOTAL_FORMS': '1',
    'disponibles_856-INITIAL_FORMS': '0',
    'disponibles_856-0-id': '',
    'disponibles_856-0-obra': '',
}

print("=" * 70)
print("ENVIANDO POST A crear_obra (coleccion_manuscrita)...")
print("=" * 70)

# Intentar POST
response = client.post(
    reverse('catalogacion:crear_obra', kwargs={'tipo': 'coleccion_manuscrita'}),
    data=post_data,
    follow=True
)

print(f"\n[RESULTADO]")
print(f"  Status Code: {response.status_code}")
print(f"  Redirect Chain: {response.redirect_chain}")
print(f"  URL Final: {response.request['PATH_INFO']}")

# Verificar si la obra se creó
from catalogacion.models import ObraGeneral
ultimas_obras = ObraGeneral.objects.all().order_by('-id')[:3]
print(f"\n[ULTIMAS OBRAS EN BD]")
for obra in ultimas_obras:
    print(f"  ID {obra.pk}: {obra.num_control or 'Sin num_control'}")

print("\n[COMPLETADO] Test completado. Revisar logs arriba.")
