"""
Función de Debug - Mostrar datos que se van a guardar en consola
Muestra TODOS los campos de forma clara: campo_nombre: valor
Orden: Cabecera → 0XX → 1XX → 2XX → 3XX → 4XX → Autogenerados
"""

from datetime import datetime


def debug_obra_datos(request, obra=None):
    """
    Muestra TODOS los datos a guardar en formato simple: campo: valor
    """
    
    print("\n" + "=" * 100)
    print("🎵 DEBUG: DATOS A GUARDAR")
    print("=" * 100 + "\n")
    
    # ========================================
    # CABECERA (LÍDER)
    # ========================================
    print("📋 CABECERA")
    print("-" * 100)
    print(f"  tipo_registro: {request.POST.get('tipo_registro', 'NO DEFINIDO')}")
    print(f"  nivel_bibliografico: {request.POST.get('nivel_bibliografico', 'NO DEFINIDO')}")
    print()
    
    # ========================================
    # BLOQUE 0XX
    # ========================================
    print("📌 BLOQUE 0XX - IDENTIFICADORES Y CÓDIGOS")
    print("-" * 100)
    print(f"  centro_catalogador (040): {request.POST.get('centro_catalogador', '')}")
    
    # 020 - ISBN
    print(f"  isbn (020):")
    isbns = _extraer_datos_repetibles(request, 'isbn', ['isbn'])
    if isbns:
        for i, isbn in enumerate(isbns, 1):
            print(f"    [{i}] {isbn.get('isbn', '')}")
    else:
        print(f"    (vacío)")
    
    # 024 - ISMN
    print(f"  ismn (024):")
    ismns = _extraer_datos_repetibles(request, 'ismn', ['ismn'])
    if ismns:
        for i, ismn in enumerate(ismns, 1):
            print(f"    [{i}] {ismn.get('ismn', '')}")
    else:
        print(f"    (vacío)")
    
    # 028 - Número de Editor
    print(f"  numero_editor (028):")
    numeros_editor = _extraer_datos_repetibles(request, 'numero_editor', ['numero_editor'])
    if numeros_editor:
        for i, num in enumerate(numeros_editor, 1):
            print(f"    [{i}] {num.get('numero_editor', '')}")
    else:
        print(f"    (vacío)")
    
    # 031 - Incipit Musical
    print(f"  incipit (031):")
    incipits = _extraer_datos_repetibles(request, 'incipit', ['notacion_musica'])
    if incipits:
        for i, incipit in enumerate(incipits, 1):
            print(f"    [{i}] {incipit.get('notacion_musica', '')}")
            urls = _extraer_subcampos_anidados(request, f'url_incipit_{i-1}', 'url')
            if urls:
                for j, url in enumerate(urls, 1):
                    print(f"        URL [{j}]: {url}")
    else:
        print(f"    (vacío)")
    
    # 041 - Código de Lengua
    print(f"  codigo_lengua (041):")
    codigos_lengua = _extraer_datos_repetibles(request, 'codigo_lengua', ['es_traduccion'])
    if codigos_lengua:
        for i in range(len(codigos_lengua)):
            idiomas = _extraer_subcampos_anidados(request, f'idioma_codigo_lengua_{i}', 'idioma')
            if idiomas:
                print(f"    [{i+1}] idiomas: {', '.join(idiomas)}")
    else:
        print(f"    (vacío)")
    
    # 044 - Código de País
    print(f"  codigo_pais (044):")
    codigos_pais = _extraer_datos_repetibles(request, 'codigo_pais', ['codigo_pais'])
    if codigos_pais:
        for i, pais in enumerate(codigos_pais, 1):
            print(f"    [{i}] {pais.get('codigo_pais', '')}")
    else:
        print(f"    (vacío)")
    print()
    
    # ========================================
    # BLOQUE 1XX
    # ========================================
    print("📌 BLOQUE 1XX - COMPOSITOR Y TÍTULOS UNIFORMES")
    print("-" * 100)
    
    compositor_id = request.POST.get('compositor', '')
    print(f"  compositor (100): {compositor_id or '(vacío)'}")
    
    funciones = _extraer_datos_repetibles(request, 'funcion_compositor', ['funcion'])
    if funciones:
        print(f"  funciones_compositor (100 $e):")
        for i, func in enumerate(funciones, 1):
            print(f"    [{i}] {func.get('funcion', '')}")
    
    titulo_130 = request.POST.get('titulo_uniforme', '')
    print(f"  titulo_uniforme (130): {titulo_130 or '(vacío)'}")
    
    titulo_240 = request.POST.get('titulo_240', '')
    print(f"  titulo_uniforme_compositor (240): {titulo_240 or '(vacío)'}")
    print()
    
    # ========================================
    # BLOQUE 2XX
    # ========================================
    print("📌 BLOQUE 2XX - TÍTULOS Y PUBLICACIÓN")
    print("-" * 100)
    
    print(f"  titulo_principal (245): {request.POST.get('titulo_principal', '(vacío)')}")
    print(f"  subtitulo (245): {request.POST.get('subtitulo', '(vacío)')}")
    print(f"  mencion_responsabilidad (245): {request.POST.get('mencion_responsabilidad', '(vacío)')}")
    
    # 246 - Título Alternativo
    print(f"  titulo_alternativo (246):")
    titulos_alt = _extraer_datos_repetibles(request, 'titulo_alternativo', ['titulo'])
    if titulos_alt:
        for i, tit in enumerate(titulos_alt, 1):
            print(f"    [{i}] {tit.get('titulo', '')}")
    else:
        print(f"    (vacío)")
    
    # 250 - Edición
    print(f"  edicion (250):")
    ediciones = _extraer_datos_repetibles(request, 'edicion', ['edicion'])
    if ediciones:
        for i, ed in enumerate(ediciones, 1):
            print(f"    [{i}] {ed.get('edicion', '')}")
    else:
        print(f"    (vacío)")
    
    # 264 - Producción/Publicación
    print(f"  produccion_publicacion (264):")
    produccion = _extraer_datos_repetibles(request, 'produccion_publicacion', 
                                          ['lugar_produccion', 'nombre_productor', 'fecha_produccion'])
    if produccion:
        for i, prod in enumerate(produccion, 1):
            lugar = prod.get('lugar_produccion', '')
            productor = prod.get('nombre_productor', '')
            fecha = prod.get('fecha_produccion', '')
            detalles = [x for x in [lugar, productor, fecha] if x]
            print(f"    [{i}] {' - '.join(detalles)}")
    else:
        print(f"    (vacío)")
    print()
    
    # ========================================
    # BLOQUE 3XX
    # ========================================
    print("📌 BLOQUE 3XX - DESCRIPCIÓN FÍSICA")
    print("-" * 100)
    
    # 300 - Descripción Física
    print(f"  descripcion_fisica (300):")
    desc_fisicas = _extraer_datos_repetibles(request, 'descripcion_fisica', ['otras_caracteristicas'])
    if desc_fisicas:
        for i in range(len(desc_fisicas)):
            extensiones = _extraer_subcampos_anidados(request, f'extension_300_{i}', 'extension')
            dimensiones = _extraer_subcampos_anidados(request, f'dimension_300_{i}', 'dimension')
            
            datos_desc = []
            if extensiones:
                datos_desc.append(f"extensiones: {', '.join(extensiones)}")
            if dimensiones:
                datos_desc.append(f"dimensiones: {', '.join(dimensiones)}")
            
            if datos_desc:
                print(f"    [{i+1}] {'; '.join(datos_desc)}")
    else:
        print(f"    (vacío)")
    
    # 340 - Medio Físico
    print(f"  medio_fisico (340):")
    medios_fisicos = _extraer_datos_repetibles(request, 'medio_fisico', ['material_base'])
    if medios_fisicos:
        for i in range(len(medios_fisicos)):
            tecnicas = _extraer_subcampos_anidados(request, f'tecnica_340_{i}', 'tecnica')
            if tecnicas:
                print(f"    [{i+1}] técnicas: {', '.join(tecnicas)}")
    else:
        print(f"    (vacío)")
    
    # 348 - Características Música Notada
    print(f"  caracteristica_musica_notada (348):")
    formatos = _extraer_subcampos_anidados_multiples(request, 'formato_348')
    if formatos:
        for i, formato in enumerate(formatos, 1):
            print(f"    [{i}] {formato}")
    else:
        print(f"    (vacío)")
    
    # 382 - Medio de Interpretación
    print(f"  medio_interpretacion (382):")
    medios_interp = _extraer_datos_repetibles(request, 'medio_382', ['tipo_agrupacion'])
    if medios_interp or _extraer_subcampos_anidados_multiples(request, 'medio_382_a'):
        for i in range(max(len(medios_interp), 10)):
            medios = _extraer_subcampos_anidados(request, f'medio_382_a_{i}', 'medio')
            solistas = _extraer_subcampos_anidados(request, f'solista_382_{i}', 'solista')
            numeros = _extraer_subcampos_anidados(request, f'numero_interpretes_382_{i}', 'numero')
            
            datos_interp = []
            if medios:
                datos_interp.append(f"medios: {', '.join(medios)}")
            if solistas:
                datos_interp.append(f"solistas: {', '.join(solistas)}")
            if numeros:
                datos_interp.append(f"intérpretes: {', '.join(numeros)}")
            
            if datos_interp:
                print(f"    [{i+1}] {'; '.join(datos_interp)}")
        if not any([_extraer_subcampos_anidados(request, f'medio_382_a_{i}', 'medio') for i in range(10)]):
            print(f"    (vacío)")
    else:
        print(f"    (vacío)")
    
    # 383 - Designación Numérica
    print(f"  designacion_numerica (383):")
    num_obras = _extraer_subcampos_anidados_multiples(request, 'numero_obra_383')
    opus_list = _extraer_subcampos_anidados_multiples(request, 'opus_383')
    if num_obras or opus_list:
        if num_obras:
            print(f"    números de obra: {', '.join(num_obras)}")
        if opus_list:
            print(f"    opus: {', '.join(opus_list)}")
    else:
        print(f"    (vacío)")
    
    # 384 - Tonalidad
    print(f"  tonalidad (384): {request.POST.get('tonalidad_384', '(vacío)')}")
    print()
    
    # ========================================
    # BLOQUE 4XX
    # ========================================
    print("📌 BLOQUE 4XX - SERIES")
    print("-" * 100)
    
    # 490 - Mención de Serie
    print(f"  mencion_serie (490):")
    menciones_serie = _extraer_datos_repetibles(request, 'mencion_serie', ['relacion'])
    if menciones_serie or _extraer_subcampos_anidados_multiples(request, 'titulo_serie_490'):
        for i in range(max(len(menciones_serie), 10)):
            titulos = _extraer_subcampos_anidados(request, f'titulo_serie_490_{i}', 'titulo')
            volumenes = _extraer_subcampos_anidados(request, f'volumen_serie_490_{i}', 'volumen')
            
            datos_serie = []
            if titulos:
                datos_serie.append(f"títulos: {', '.join(titulos)}")
            if volumenes:
                datos_serie.append(f"volúmenes: {', '.join(volumenes)}")
            
            if datos_serie:
                print(f"    [{i+1}] {'; '.join(datos_serie)}")
        if not any([_extraer_subcampos_anidados(request, f'titulo_serie_490_{i}', 'titulo') for i in range(10)]):
            print(f"    (vacío)")
    else:
        print(f"    (vacío)")
    print()
    
    # ========================================
    # CAMPOS AUTOGENERADOS
    # ========================================
    print("📌 CAMPOS AUTOGENERADOS")
    print("-" * 100)
    print(f"  num_control (001): Generado automáticamente")
    print(f"  estado_registro (005): n")
    print(f"  codigo_informacion (008): Generado con fecha y hora")
    print(f"  clasificacion_092 ($a): {request.POST.get('centro_catalogador', 'UNL')}")
    print(f"  clasificacion_092 ($b): BLMP")
    print(f"  clasificacion_092 ($c): {request.POST.get('codigo_pais_0_codigo_pais', 'ec')}")
    print(f"  clasificacion_092 ($d): Ms o Imp (según tipo_registro)")
    print()
    
    if obra:
        print("📌 DATOS GUARDADOS EN BD")
        print("-" * 100)
        print(f"  id: {obra.id}")
        print(f"  num_control: {obra.num_control}")
        print(f"  fecha_creacion_sistema: {obra.fecha_creacion_sistema}")
        print()
    
    print("=" * 100)
    print("✅ FIN DEL DEBUG")
    print("=" * 100 + "\n")


# ================================================
# FUNCIONES AUXILIARES
# ================================================

def _extraer_datos_repetibles(request, prefijo, campos):
    """Extrae datos repetibles del formulario."""
    datos = []
    indice = 0
    
    while True:
        valores = {campo: request.POST.get(f'{prefijo}_{indice}_{campo}', '').strip() 
                  for campo in campos}
        
        if any(valores.values()):
            datos.append(valores)
            indice += 1
        else:
            indice += 1
            if indice > 50:
                break
    
    return datos


def _extraer_subcampos_anidados(request, prefijo_padre, nombre_campo):
    """Extrae subcampos anidados (URLs, idiomas, etc)."""
    valores = []
    indice = 0
    
    while True:
        valor = request.POST.get(f'{prefijo_padre}_{indice}_{nombre_campo}', '').strip()
        
        if valor:
            valores.append(valor)
        
        indice += 1
        if indice > 20:
            break
    
    return valores


def _extraer_subcampos_anidados_multiples(request, prefijo):
    """Extrae subcampos anidados sin padre explícito."""
    valores = []
    indice = 0
    sub_indice = 0
    
    while True:
        for key in request.POST.keys():
            if key.startswith(f'{prefijo}_{indice}_{sub_indice}_'):
                valor = request.POST.get(key, '').strip()
                if valor and valor not in valores:
                    valores.append(valor)
        
        sub_indice += 1
        if sub_indice > 20:
            sub_indice = 0
            indice += 1
            if indice > 50:
                break
    
    return valores
