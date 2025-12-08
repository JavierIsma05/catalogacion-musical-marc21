#!/usr/bin/env python
"""
Script de prueba COMPLETO para guardar una obra con TODOS los campos requeridos.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
import logging

# Configurar logging para mostrar TODOS los mensajes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Cliente de prueba
client = Client()

# CREAR DATOS COMPLETOS CON TODOS LOS CAMPOS REQUERIDOS
post_data = {
    # CAMPOS REQUERIDOS DEL FORMULARIO PRINCIPAL
    'tipo_registro': 'd',  # Manuscrita (correcto para coleccion_manuscrita)
    'nivel_bibliografico': 'c',  # Colección (correcto para coleccion_manuscrita)
    'centro_catalogador': 'MxFLC',  # REQUERIDO
    'titulo_principal': 'Test Colección Manuscrita',  # REQUERIDO (131 o 245)
    'ms_imp': 'manuscrito',  # REQUERIDO: manuscrito, impreso, etc.
    
    # Campo de acceso principal: DEBE TENER 100 (Compositor) o 130 (Título Uniforme)
    'titulo_uniforme': '',  # Puede estar vacío si hay compositor
    'titulo_uniforme_texto': 'Colección de obras musicales',  # REQUERIDO para punto de acceso 130
    
    # Otros campos opcionales
    'tipo_creacion_contenido': 'a',
    'tipo_control': 'a',
    'idioma_principal': 'es',
    
    # FORMSETS - Usar los prefijos CORRECTOS
    'incipits-TOTAL_FORMS': '0',
    'incipits-INITIAL_FORMS': '0',
    'incipits-MIN_NUM_FORMS': '0',
    'incipits-MAX_NUM_FORMS': '1000',
    
    'lenguas-TOTAL_FORMS': '0',
    'lenguas-INITIAL_FORMS': '0',
    'lenguas-MIN_NUM_FORMS': '0',
    'lenguas-MAX_NUM_FORMS': '1000',
    
    'paises-TOTAL_FORMS': '0',
    'paises-INITIAL_FORMS': '0',
    'paises-MIN_NUM_FORMS': '0',
    'paises-MAX_NUM_FORMS': '1000',
    
    'funciones-TOTAL_FORMS': '0',
    'funciones-INITIAL_FORMS': '0',
    'funciones-MIN_NUM_FORMS': '0',
    'funciones-MAX_NUM_FORMS': '1000',
    
    'medios_382-TOTAL_FORMS': '0',
    'medios_382-INITIAL_FORMS': '0',
    'medios_382-MIN_NUM_FORMS': '0',
    'medios_382-MAX_NUM_FORMS': '1000',
    
    'titulos_alt-TOTAL_FORMS': '0',
    'titulos_alt-INITIAL_FORMS': '0',
    'titulos_alt-MIN_NUM_FORMS': '0',
    'titulos_alt-MAX_NUM_FORMS': '1000',
    
    'ediciones-TOTAL_FORMS': '0',
    'ediciones-INITIAL_FORMS': '0',
    'ediciones-MIN_NUM_FORMS': '0',
    'ediciones-MAX_NUM_FORMS': '1000',
    
    'produccion-TOTAL_FORMS': '0',
    'produccion-INITIAL_FORMS': '0',
    'produccion-MIN_NUM_FORMS': '0',
    'produccion-MAX_NUM_FORMS': '1000',
    
    'menciones_490-TOTAL_FORMS': '0',
    'menciones_490-INITIAL_FORMS': '0',
    'menciones_490-MIN_NUM_FORMS': '0',
    'menciones_490-MAX_NUM_FORMS': '1000',
    
    'notas_500-TOTAL_FORMS': '0',
    'notas_500-INITIAL_FORMS': '0',
    'notas_500-MIN_NUM_FORMS': '0',
    'notas_500-MAX_NUM_FORMS': '1000',
    
    'contenidos_505-TOTAL_FORMS': '0',
    'contenidos_505-INITIAL_FORMS': '0',
    'contenidos_505-MIN_NUM_FORMS': '0',
    'contenidos_505-MAX_NUM_FORMS': '1000',
    
    'sumarios_520-TOTAL_FORMS': '0',
    'sumarios_520-INITIAL_FORMS': '0',
    'sumarios_520-MIN_NUM_FORMS': '0',
    'sumarios_520-MAX_NUM_FORMS': '1000',
    
    'biograficos_545-TOTAL_FORMS': '0',
    'biograficos_545-INITIAL_FORMS': '0',
    'biograficos_545-MIN_NUM_FORMS': '0',
    'biograficos_545-MAX_NUM_FORMS': '1000',
    
    'materias_650-TOTAL_FORMS': '0',
    'materias_650-INITIAL_FORMS': '0',
    'materias_650-MIN_NUM_FORMS': '0',
    'materias_650-MAX_NUM_FORMS': '1000',
    
    'generos_655-TOTAL_FORMS': '0',
    'generos_655-INITIAL_FORMS': '0',
    'generos_655-MIN_NUM_FORMS': '0',
    'generos_655-MAX_NUM_FORMS': '1000',
    
    'nombres_700-TOTAL_FORMS': '0',
    'nombres_700-INITIAL_FORMS': '0',
    'nombres_700-MIN_NUM_FORMS': '0',
    'nombres_700-MAX_NUM_FORMS': '1000',
    
    'entidades_710-TOTAL_FORMS': '0',
    'entidades_710-INITIAL_FORMS': '0',
    'entidades_710-MIN_NUM_FORMS': '0',
    'entidades_710-MAX_NUM_FORMS': '1000',
    
    'enlaces_773-TOTAL_FORMS': '0',
    'enlaces_773-INITIAL_FORMS': '0',
    'enlaces_773-MIN_NUM_FORMS': '0',
    'enlaces_773-MAX_NUM_FORMS': '1000',
    
    'enlaces_774-TOTAL_FORMS': '0',
    'enlaces_774-INITIAL_FORMS': '0',
    'enlaces_774-MIN_NUM_FORMS': '0',
    'enlaces_774-MAX_NUM_FORMS': '1000',
    
    'relaciones_787-TOTAL_FORMS': '0',
    'relaciones_787-INITIAL_FORMS': '0',
    'relaciones_787-MIN_NUM_FORMS': '0',
    'relaciones_787-MAX_NUM_FORMS': '1000',
    
    'ubicaciones_852-TOTAL_FORMS': '0',
    'ubicaciones_852-INITIAL_FORMS': '0',
    'ubicaciones_852-MIN_NUM_FORMS': '0',
    'ubicaciones_852-MAX_NUM_FORMS': '1000',
    
    'disponibles_856-TOTAL_FORMS': '0',
    'disponibles_856-INITIAL_FORMS': '0',
    'disponibles_856-MIN_NUM_FORMS': '0',
    'disponibles_856-MAX_NUM_FORMS': '1000',
}

print("=" * 70)
print("TEST COMPLETO: GUARDAR OBRA CON TODOS LOS CAMPOS REQUERIDOS")
print("=" * 70)
print(f"Enviando {len(post_data)} parametros POST...")
print()

# Intentar POST
response = client.post(
    reverse('catalogacion:crear_obra', kwargs={'tipo': 'coleccion_manuscrita'}),
    data=post_data,
    follow=True
)

print(f"\n[RESULTADO POST]")
print(f"  Status Code: {response.status_code}")
print(f"  Redirect Chain: {response.redirect_chain}")
print(f"  URL Final: {response.request['PATH_INFO']}")

# Verificar si la obra se creó
from catalogacion.models import ObraGeneral
ultimas_obras = ObraGeneral.objects.all().order_by('-id')[:1]
print(f"\n[VERIFICACION DE GUARDADO]")

if response.status_code == 302:
    # Hubo redirección exitosa = forma válida
    print("  EXITOSO: Redirigió (forma válida)")
    if ultimas_obras:
        print(f"  Obra creada: ID {ultimas_obras[0].pk} - {ultimas_obras[0].num_control}")
else:
    print(f"  FALLO: Status {response.status_code}")
    if ultimas_obras:
        print(f"  Ultima obra: ID {ultimas_obras[0].pk}")

print("\n[COMPLETADO]")
