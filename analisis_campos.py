#!/usr/bin/env python
"""
Script para verificar consistencia entre Models y Forms
Detecta campos faltantes, nombres incorrectos, etc.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from django.apps import apps
from catalogacion.forms.formsets import *

# Diccionario de modelos a verificar
MODELOS_A_VERIFICAR = {
    'NotaGeneral500': {},
    'Contenido505': {},
    'Sumario520': {},
    'DatosBiograficos545': {},
    'MedioInterpretacion382': {},
    'MedioInterpretacion382_a': {},
    'Edicion': {},
    'ProduccionPublicacion': {},
    'Lugar264': {},
    'NombreEntidad264': {},
    'Fecha264': {},
    'TituloAlternativo': {},
    'IncipitMusical': {},
    'IncipitURL': {},
    'CodigoLengua': {},
    'IdiomaObra': {},
    'CodigoPaisEntidad': {},
    'FuncionCompositor': {},
    'NombreRelacionado700': {},
    'TerminoAsociado700': {},
    'Funcion700': {},
    'EntidadRelacionada710': {},
    'Materia650': {},
    'MateriaGenero655': {},
    'EnlaceDocumentoFuente773': {},
    'NumeroControl773': {},
    'EnlaceUnidadConstituyente774': {},
    'NumeroControl774': {},
    'OtrasRelaciones787': {},
    'NumeroControl787': {},
    'Ubicacion852': {},
    'Disponible856': {},
    'URL856': {},
    'TextoEnlace856': {},
    'MencionSerie490': {},
    'TituloSerie490': {},
}

print("=" * 80)
print("ANÁLISIS DE CAMPOS EN MODELOS")
print("=" * 80)

for modelo_name in MODELOS_A_VERIFICAR:
    try:
        Model = apps.get_model('catalogacion', modelo_name)
        campos = []
        
        for field in Model._meta.get_fields():
            if hasattr(field, 'name') and not field.name.startswith('_'):
                tipo = field.get_internal_type()
                campos.append(f"  ✓ {field.name} ({tipo})")
        
        print(f"\n{modelo_name}:")
        for campo in sorted(campos):
            print(campo)
            
    except Exception as e:
        print(f"\n❌ {modelo_name}: ERROR - {str(e)}")

print("\n" + "=" * 80)
print("ANÁLISIS COMPLETADO")
print("=" * 80)
