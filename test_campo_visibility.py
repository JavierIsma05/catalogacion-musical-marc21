"""
Script de prueba para verificar la configuración de visibilidad de campos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from catalogacion.views.obra_config import CAMPOS_POR_TIPO_OBRA, get_campos_visibles, debe_mostrar_campo, debe_mostrar_formset

def test_visibilidad():
    """Probar la configuración de visibilidad para cada tipo de obra"""
    
    print("=" * 80)
    print("PRUEBA DE CONFIGURACIÓN DE VISIBILIDAD DE CAMPOS")
    print("=" * 80)
    
    tipos_obra = [
        'coleccion_manuscrita',
        'obra_en_coleccion_manuscrita',
        'obra_manuscrita_individual',
        'coleccion_impresa',
        'obra_en_coleccion_impresa',
        'obra_impresa_individual'
    ]
    
    # Campos críticos a verificar
    campos_criticos = {
        '100': 'Compositor',
        '130': 'Título Uniforme Principal',
        '031': 'Íncipit Musical',
        '773': 'Documento Fuente',
        '774': 'Unidades Constituyentes',
        '787': 'Otras Relaciones'
    }
    
    formsets_criticos = {
        'incipits_musicales': 'Íncipit Musical',
        'funciones_compositor': 'Funciones Compositor',
        'enlaces_documento_fuente_773': 'Enlace Documento Fuente',
        'enlaces_unidad_constituyente_774': 'Unidades Constituyentes',
        'otras_relaciones_787': 'Otras Relaciones'
    }
    
    for tipo in tipos_obra:
        print(f"\n{'='*80}")
        print(f"TIPO DE OBRA: {tipo.upper()}")
        print(f"{'='*80}")
        
        config = get_campos_visibles(tipo)
        
        print("\n📋 CAMPOS CRÍTICOS:")
        for campo, nombre in campos_criticos.items():
            visible = debe_mostrar_campo(tipo, campo)
            estado = "✅ VISIBLE" if visible else "❌ OCULTO"
            print(f"  {campo} ({nombre}): {estado}")
        
        print("\n📦 FORMSETS CRÍTICOS:")
        for formset, nombre in formsets_criticos.items():
            visible = debe_mostrar_formset(tipo, formset)
            estado = "✅ VISIBLE" if visible else "❌ OCULTO"
            print(f"  {formset}: {estado}")
        
        print(f"\n📊 RESUMEN:")
        print(f"  Total campos simples: {len(config['campos_simples'])}")
        print(f"  Total formsets visibles: {len(config['formsets_visibles'])}")
    
    # Verificar diferencias críticas según plantillas
    print(f"\n\n{'='*80}")
    print("VERIFICACIÓN DE DIFERENCIAS CRÍTICAS SEGÚN PLANTILLAS")
    print(f"{'='*80}")
    
    print("\n1️⃣ COLECCIONES (deben mostrar 100 y 130, sin 773 y con 774):")
    for tipo in ['coleccion_manuscrita', 'coleccion_impresa']:
        tiene_100 = debe_mostrar_campo(tipo, '100')
        tiene_130 = debe_mostrar_campo(tipo, '130')
        tiene_773 = debe_mostrar_formset(tipo, 'enlaces_documento_fuente_773')
        tiene_774 = debe_mostrar_formset(tipo, 'enlaces_unidad_constituyente_774')
        print(f"  {tipo}:")
        print(f"    Campo 100 (Compositor): {'✅ CORRECTO (visible)' if tiene_100 else '⚠️ ERROR (oculto)'}")
        print(f"    Campo 130 (Título Uniforme): {'✅ CORRECTO (visible)' if tiene_130 else '⚠️ ERROR (oculto)'}")
        print(f"    Campo 773 (Doc. Fuente): {'❌ CORRECTO (oculto)' if not tiene_773 else '⚠️ ERROR (visible)'}")
        print(f"    Campo 774 (Constituyentes): {'✅ CORRECTO (visible)' if tiene_774 else '⚠️ ERROR (oculto)'}")
    
    print("\n2️⃣ OBRAS EN COLECCIÓN (deben tener 773, no 774):")
    for tipo in ['obra_en_coleccion_manuscrita', 'obra_en_coleccion_impresa']:
        tiene_773 = debe_mostrar_formset(tipo, 'enlaces_documento_fuente_773')
        tiene_774 = debe_mostrar_formset(tipo, 'enlaces_unidad_constituyente_774')
        print(f"  {tipo}:")
        print(f"    Campo 773 (Doc. Fuente): {'✅ CORRECTO (visible)' if tiene_773 else '⚠️ ERROR (oculto)'}")
        print(f"    Campo 774 (Constituyentes): {'❌ CORRECTO (oculto)' if not tiene_774 else '⚠️ ERROR (visible)'}")
    
    print("\n3️⃣ OBRAS INDIVIDUALES (deben tener 787, no 773 ni 774):")
    for tipo in ['obra_manuscrita_individual', 'obra_impresa_individual']:
        tiene_773 = debe_mostrar_formset(tipo, 'enlaces_documento_fuente_773')
        tiene_774 = debe_mostrar_formset(tipo, 'enlaces_unidad_constituyente_774')
        tiene_787 = debe_mostrar_formset(tipo, 'otras_relaciones_787')
        print(f"  {tipo}:")
        print(f"    Campo 773 (Doc. Fuente): {'❌ CORRECTO (oculto)' if not tiene_773 else '⚠️ ERROR (visible)'}")
        print(f"    Campo 774 (Constituyentes): {'❌ CORRECTO (oculto)' if not tiene_774 else '⚠️ ERROR (visible)'}")
        print(f"    Campo 787 (Otras Relaciones): {'✅ CORRECTO (visible)' if tiene_787 else '⚠️ ERROR (oculto)'}")
    
    print("\n4️⃣ ÍNCIPIT MUSICAL (solo obras individuales y en colección, no colecciones):")
    for tipo in tipos_obra:
        tiene_incipit = debe_mostrar_formset(tipo, 'incipits_musicales')
        es_coleccion = 'coleccion_' in tipo and 'obra_en_' not in tipo
        esperado = not es_coleccion
        if tiene_incipit == esperado:
            estado = "✅ CORRECTO"
        else:
            estado = "⚠️ ERROR"
        print(f"  {tipo}: {estado} ({'visible' if tiene_incipit else 'oculto'})")
    
    print(f"\n{'='*80}")
    print("✅ PRUEBA COMPLETADA")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    test_visibilidad()
