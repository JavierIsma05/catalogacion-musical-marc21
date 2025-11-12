"""
Función de Debug - Mostrar datos que se van a guardar en consola
Muestra TODOS los campos Y SUBCAMPOS en formato MARC21
Orden: Cabecera → 0XX → 1XX → 2XX → 3XX → 4XX → Autogenerados
"""

from datetime import datetime


def debug_obra_datos(request, obra=None):
    """
    Muestra TODOS los datos a guardar en formato MARC21: campo_nombre ($subcampo): valor
    """
    
    print("\n" + "=" * 110)
    print("🎵 DEBUG: DATOS A GUARDAR (FORMATO MARC21)")
    print("=" * 110 + "\n")
    
    # ========================================
    # CABECERA (LÍDER)
    # ========================================
    print("📋 CABECERA")
    print("-" * 110)
    print(f"  tipo_registro: {request.POST.get('tipo_registro', 'NO DEFINIDO')}")
    print(f"  nivel_bibliografico: {request.POST.get('nivel_bibliografico', 'NO DEFINIDO')}")
    print()
    
    # ========================================
    # BLOQUE 0XX
    # ========================================
    print("📌 BLOQUE 0XX - IDENTIFICADORES Y CÓDIGOS")
    print("-" * 110)
    print(f"  040 ($a): {request.POST.get('centro_catalogador', '')}")
    
    # 020 - ISBN
    print(f"  020:")
    isbns = _extraer_datos_repetibles(request, 'isbn', ['isbn', 'calificador'])
    if isbns:
        for i, isbn in enumerate(isbns, 1):
            print(f"    [{i}] $a: {isbn.get('isbn', '')}", end="")
            if isbn.get('calificador'):
                print(f"\n        $q: {isbn.get('calificador', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    
    # 024 - ISMN
    print(f"  024:")
    ismns = _extraer_datos_repetibles(request, 'ismn', ['ismn', 'calificador'])
    if ismns:
        for i, ismn in enumerate(ismns, 1):
            print(f"    [{i}] $a: {ismn.get('ismn', '')}", end="")
            if ismn.get('calificador'):
                print(f"\n        $q: {ismn.get('calificador', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    
    # 028 - Número de Editor
    print(f"  028:")
    numeros_editor = _extraer_datos_repetibles(request, 'numero_editor', 
                                               ['codigo_fuente', 'numero_editor', 'numero_edicion'])
    if numeros_editor:
        for i, num in enumerate(numeros_editor, 1):
            print(f"    [{i}] $b: {num.get('codigo_fuente', '')}", end="")
            print(f"\n        $a: {num.get('numero_editor', '')}", end="")
            if num.get('numero_edicion'):
                print(f"\n        $c: {num.get('numero_edicion', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    
    # 031 - Incipit Musical
    print(f"  031:")
    incipits = _extraer_datos_repetibles(request, 'incipit', 
                                        ['notacion_musica', 'tonalidad', 'rol_agente_catalogador'])
    if incipits:
        for i, incipit in enumerate(incipits, 1):
            print(f"    [{i}] $g: {incipit.get('notacion_musica', '')}", end="")
            if incipit.get('tonalidad'):
                print(f"\n        $m: {incipit.get('tonalidad', '')}", end="")
            if incipit.get('rol_agente_catalogador'):
                print(f"\n        $q: {incipit.get('rol_agente_catalogador', '')}", end="")
            
            # URLs anidadas
            urls_por_incipit = _extraer_subcampos_anidados(request, f'url_incipit_{i-1}', 'url')
            if urls_por_incipit:
                for j, url in enumerate(urls_por_incipit, 1):
                    print(f"\n        $u[{j}]: {url}", end="")
            print()
    else:
        print(f"    (vacío)")
    
    # 041 - Código de Lengua
    print(f"  041:")
    codigos_lengua = _extraer_datos_repetibles(request, 'codigo_lengua', ['es_traduccion'])
    if codigos_lengua:
        for i in range(len(codigos_lengua)):
            es_traduccion = request.POST.get(f'codigo_lengua_{i}_es_traduccion', '')
            idiomas = _extraer_subcampos_anidados(request, f'idioma_codigo_lengua_{i}', 'idioma')
            
            print(f"    [{i+1}]", end="")
            if es_traduccion:
                print(f" ind2: {es_traduccion}", end="")
            if idiomas:
                for j, idioma in enumerate(idiomas, 1):
                    print(f"\n        $a[{j}]: {idioma}", end="")
            print()
    else:
        print(f"    (vacío)")
    
    # 044 - Código de País
    print(f"  044:")
    codigos_pais = _extraer_datos_repetibles(request, 'codigo_pais', ['codigo_pais'])
    if codigos_pais:
        for i, pais in enumerate(codigos_pais, 1):
            print(f"    [{i}] $a: {pais.get('codigo_pais', '')}")
    else:
        print(f"    (vacío)")
    print()
    
    # ========================================
    # BLOQUE 1XX
    # ========================================
    print("📌 BLOQUE 1XX - COMPOSITOR Y TÍTULOS UNIFORMES")
    print("-" * 110)
    
    # 100 - Compositor
    compositor_id = request.POST.get('compositor', '')
    print(f"  100:")
    print(f"    $a: {compositor_id or '(vacío)'}", end="")
    
    funciones = _extraer_datos_repetibles(request, 'funcion_compositor', ['funcion'])
    if funciones:
        for i, func in enumerate(funciones, 1):
            print(f"\n    $e[{i}]: {func.get('funcion', '')}", end="")
    print()
    print()
    
    # 130 - Título Uniforme
    print(f"  130:")
    titulo_130 = request.POST.get('titulo_uniforme', '')
    print(f"    $a: {titulo_130 or '(vacío)'}")
    print()
    
    # 240 - Título Uniforme con Compositor
    print(f"  240:")
    titulo_240 = request.POST.get('titulo_240', '')
    print(f"    $a: {titulo_240 or '(vacío)'}")
    print()
    
    # ========================================
    # BLOQUE 2XX
    # ========================================
    print("📌 BLOQUE 2XX - TÍTULOS Y PUBLICACIÓN")
    print("-" * 110)
    
    # 245 - Título Principal
    print(f"  245:")
    print(f"    $a: {request.POST.get('titulo_principal', '(vacío)')}", end="")
    if request.POST.get('subtitulo'):
        print(f"\n    $b: {request.POST.get('subtitulo', '')}", end="")
    if request.POST.get('mencion_responsabilidad'):
        print(f"\n    $c: {request.POST.get('mencion_responsabilidad', '')}", end="")
    print()
    print()
    
    # 246 - Título Alternativo
    print(f"  246:")
    titulos_alt = _extraer_datos_repetibles(request, 'titulo_alternativo', 
                                           ['titulo', 'resto_titulo'])
    if titulos_alt:
        for i, tit in enumerate(titulos_alt, 1):
            print(f"    [{i}] $a: {tit.get('titulo', '')}", end="")
            if tit.get('resto_titulo'):
                print(f"\n        $b: {tit.get('resto_titulo', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    print()
    
    # 250 - Edición
    print(f"  250:")
    ediciones = _extraer_datos_repetibles(request, 'edicion', 
                                         ['edicion', 'mencion_responsabilidad_edicion'])
    if ediciones:
        for i, ed in enumerate(ediciones, 1):
            print(f"    [{i}] $a: {ed.get('edicion', '')}", end="")
            if ed.get('mencion_responsabilidad_edicion'):
                print(f"\n        $b: {ed.get('mencion_responsabilidad_edicion', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    print()
    
    # 264 - Producción/Publicación
    print(f"  264:")
    produccion = _extraer_datos_repetibles(request, 'produccion_publicacion', 
                                          ['funcion', 'lugar_produccion', 'nombre_productor', 'fecha_produccion'])
    if produccion:
        for i, prod in enumerate(produccion, 1):
            print(f"    [{i}] ind1: {prod.get('funcion', '')}", end="")
            if prod.get('lugar_produccion'):
                print(f"\n        $a: {prod.get('lugar_produccion', '')}", end="")
            if prod.get('nombre_productor'):
                print(f"\n        $b: {prod.get('nombre_productor', '')}", end="")
            if prod.get('fecha_produccion'):
                print(f"\n        $c: {prod.get('fecha_produccion', '')}", end="")
            print()
    else:
        print(f"    (vacío)")
    print()
    
    # ========================================
    # BLOQUE 3XX
    # ========================================
    print("📌 BLOQUE 3XX - DESCRIPCIÓN FÍSICA")
    print("-" * 110)
    
    # 300 - Descripción Física
    print(f"  300:")
    desc_fisicas = _extraer_datos_repetibles(request, 'descripcion_fisica', 
                                            ['otras_caracteristicas', 'material_acompanante'])
    if desc_fisicas:
        for i in range(len(desc_fisicas)):
            extensiones = _extraer_subcampos_anidados(request, f'extension_300_{i}', 'extension')
            dimensiones = _extraer_subcampos_anidados(request, f'dimension_300_{i}', 'dimension')
            otras = request.POST.get(f'descripcion_fisica_{i}_otras_caracteristicas', '')
            material = request.POST.get(f'descripcion_fisica_{i}_material_acompanante', '')
            
            print(f"    [{i+1}]", end="")
            if extensiones:
                for j, ext in enumerate(extensiones, 1):
                    print(f"\n        $a[{j}]: {ext}", end="")
            if otras:
                print(f"\n        $b: {otras}", end="")
            if dimensiones:
                for j, dim in enumerate(dimensiones, 1):
                    print(f"\n        $c[{j}]: {dim}", end="")
            if material:
                print(f"\n        $e: {material}", end="")
            print()
    else:
        print(f"    (vacío)")
    print()
    
    # 340 - Medio Físico
    print(f"  340:")
    medios_fisicos = _extraer_datos_repetibles(request, 'medio_fisico', ['material_base'])
    if medios_fisicos:
        for i in range(len(medios_fisicos)):
            tecnicas = _extraer_subcampos_anidados(request, f'tecnica_340_{i}', 'tecnica')
            
            print(f"    [{i+1}]", end="")
            if tecnicas:
                for j, tec in enumerate(tecnicas, 1):
                    print(f"\n        $d[{j}]: {tec}", end="")
            print()
    else:
        print(f"    (vacío)")
    print()
    
    # 348 - Características Música Notada
    print(f"  348:")
    formatos = _extraer_subcampos_anidados_multiples(request, 'formato_348')
    if formatos:
        for i, formato in enumerate(formatos, 1):
            print(f"    [{i}] $a: {formato}")
    else:
        print(f"    (vacío)")
    print()
    
    # 382 - Medio de Interpretación
    print(f"  382:")
    medios_interp = _extraer_datos_repetibles(request, 'medio_382', ['tipo_agrupacion'])
    if medios_interp or _extraer_subcampos_anidados_multiples(request, 'medio_382_a'):
        tiene_datos = False
        for i in range(max(len(medios_interp), 10)):
            medios = _extraer_subcampos_anidados(request, f'medio_382_a_{i}', 'medio')
            solistas = _extraer_subcampos_anidados(request, f'solista_382_{i}', 'solista')
            numeros = _extraer_subcampos_anidados(request, f'numero_interpretes_382_{i}', 'numero')
            
            if medios or solistas or numeros:
                tiene_datos = True
                print(f"    [{i+1}]", end="")
                if medios:
                    for j, m in enumerate(medios, 1):
                        print(f"\n        $a[{j}]: {m}", end="")
                if solistas:
                    for j, s in enumerate(solistas, 1):
                        print(f"\n        $b[{j}]: {s}", end="")
                if numeros:
                    for j, n in enumerate(numeros, 1):
                        print(f"\n        $n[{j}]: {n}", end="")
                print()
        if not tiene_datos:
            print(f"    (vacío)")
    else:
        print(f"    (vacío)")
    print()
    
    # 383 - Designación Numérica
    print(f"  383:")
    num_obras = _extraer_subcampos_anidados_multiples(request, 'numero_obra_383')
    opus_list = _extraer_subcampos_anidados_multiples(request, 'opus_383')
    if num_obras or opus_list:
        print(f"    [1]", end="")
        if num_obras:
            for i, num in enumerate(num_obras, 1):
                print(f"\n        $a[{i}]: {num}", end="")
        if opus_list:
            for i, op in enumerate(opus_list, 1):
                print(f"\n        $b[{i}]: {op}", end="")
        print()
    else:
        print(f"    (vacío)")
    print()
    
    # 384 - Tonalidad
    print(f"  384:")
    tonalidad = request.POST.get('tonalidad_384', '')
    print(f"    $a: {tonalidad or '(vacío)'}")
    print()
    
    # ========================================
    # BLOQUE 4XX
    # ========================================
    print("📌 BLOQUE 4XX - SERIES")
    print("-" * 110)
    
    # 490 - Mención de Serie
    print(f"  490:")
    menciones_serie = _extraer_datos_repetibles(request, 'mencion_serie', ['relacion'])
    if menciones_serie or _extraer_subcampos_anidados_multiples(request, 'titulo_serie_490'):
        tiene_datos = False
        for i in range(max(len(menciones_serie), 10)):
            relacion = request.POST.get(f'mencion_serie_{i}_relacion', '')
            titulos = _extraer_subcampos_anidados(request, f'titulo_serie_490_{i}', 'titulo')
            volumenes = _extraer_subcampos_anidados(request, f'volumen_serie_490_{i}', 'volumen')
            
            if relacion or titulos or volumenes:
                tiene_datos = True
                print(f"    [{i+1}]", end="")
                if relacion:
                    print(f" ind1: {relacion}", end="")
                if titulos:
                    for j, t in enumerate(titulos, 1):
                        print(f"\n        $a[{j}]: {t}", end="")
                if volumenes:
                    for j, v in enumerate(volumenes, 1):
                        print(f"\n        $v[{j}]: {v}", end="")
                print()
        if not tiene_datos:
            print(f"    (vacío)")
    else:
        print(f"    (vacío)")
    print()
        # ========================================
    # BLOQUE 5XX
    # ========================================
    print("📌 BLOQUE 5XX - NOTAS")
    print("-" * 110)

    # 500 - Nota General
    print(f"  500:")
    notas_generales = _extraer_subcampos_anidados_multiples(request, 'nota_general_500_a')
    if notas_generales:
        for i, nota in enumerate(notas_generales, 1):
            print(f"    [{i}] $a: {nota}")
    else:
        print("    (vacío)")
    print()

    # 505 - Nota de Contenido
    print(f"  505:")
    notas_contenido = _extraer_subcampos_anidados_multiples(request, 'nota_contenido_505_a')
    if notas_contenido:
        for i, nota in enumerate(notas_contenido, 1):
            print(f"    [{i}] $a: {nota}")
    else:
        print("    (vacío)")
    print()

    # 545 - Nota Biográfica
    print(f"  545:")
    notas_bio = _extraer_datos_repetibles(request, 'nota_biografica_545', ['a', 'u'])
    if notas_bio:
        for i, nota in enumerate(notas_bio, 1):
            print(f"    [{i}] $a: {nota.get('a', '')}")
            if nota.get('u'):
                print(f"        $u: {nota.get('u', '')}")
    else:
        print("    (vacío)")
    print()


    # ========================================
    # BLOQUE 6XX
    # ========================================
    print("📌 BLOQUE 6XX - MATERIAS Y GÉNEROS")
    print("-" * 110)

    # 650 - Materia
    print(f"  650:")
    materias = _extraer_subcampos_anidados_multiples(request, 'materia_650_a')
    if materias:
        for i, mat in enumerate(materias, 1):
            print(f"    [{i}] $a: {mat}")
    else:
        print("    (vacío)")
    print()

    # 655 - Género/Forma
    print(f"  655:")
    generos = _extraer_subcampos_anidados_multiples(request, 'materia_genero_655_a')
    if generos:
        for i, gen in enumerate(generos, 1):
            print(f"    [{i}] $a: {gen}")
    else:
        print("    (vacío)")
    print()


    # ========================================
    # BLOQUE 7XX
    # ========================================
    print("📌 BLOQUE 7XX - ENTRADAS ADICIONALES")
    print("-" * 110)

    # 700 - Nombre relacionado
    print(f"  700:")
    idx = 0
    tiene_700 = False
    while True:
        termino = request.POST.get(f'termino_asociado_700_c_{idx}', '')
        funcion = request.POST.get(f'funcion_700_e_{idx}', '')
        relacion = request.POST.get(f'relacion_700_i_{idx}', '')
        autoria = request.POST.get(f'autoria_700_j_{idx}', '')
        if any([termino, funcion, relacion, autoria]):
            tiene_700 = True
            print(f"    [{idx+1}]")
            if termino: print(f"        $c: {termino}")
            if funcion: print(f"        $e: {funcion}")
            if relacion: print(f"        $i: {relacion}")
            if autoria: print(f"        $j: {autoria}")
        else:
            if idx > 20:
                break
        idx += 1
    if not tiene_700:
        print("    (vacío)")
    print()

    # 710 - Entidad relacionada
    print(f"  710:")
    funciones_entidad = _extraer_subcampos_anidados_multiples(request, 'funcion_entidad_710_e')
    if funciones_entidad:
        for i, func in enumerate(funciones_entidad, 1):
            print(f"    [{i}] $e: {func}")
    else:
        print("    (vacío)")
    print()

    # 773 - Documento fuente
    print(f"  773:")
    docs = _extraer_subcampos_anidados_multiples(request, 'coleccion_773_w')
    if docs:
        for i, doc in enumerate(docs, 1):
            print(f"    [{i}] $w: {doc}")
    else:
        print("    (vacío)")
    print()

    # 774 - Obra en colección
    print(f"  774:")
    obras_rel = _extraer_subcampos_anidados_multiples(request, 'obra_coleccion_774_w')
    if obras_rel:
        for i, num in enumerate(obras_rel, 1):
            print(f"    [{i}] $w: {num}")
    else:
        print("    (vacío)")
    print()

    # 787 - Otras relaciones
    print(f"  787:")
    otras_rel = _extraer_subcampos_anidados_multiples(request, 'otras_relaciones_787_w')
    if otras_rel:
        for i, num in enumerate(otras_rel, 1):
            print(f"    [{i}] $w: {num}")
    else:
        print("    (vacío)")
    print()


    # ========================================
    # BLOQUE 8XX
    # ========================================
    print("📌 BLOQUE 8XX - UBICACIÓN Y DISPONIBILIDAD")
    print("-" * 110)

    # 852 - Ubicación
    print(f"  852:")
    ubicaciones = _extraer_subcampos_anidados_multiples(request, 'ubicacion_852_c')
    if ubicaciones:
        for i, ubi in enumerate(ubicaciones, 1):
            print(f"    [{i}] $c: {ubi}")
    else:
        print("    (vacío)")
    print()

    # 856 - Recurso electrónico
    print(f"  856:")
    urls = _extraer_datos_repetibles(request, 'disponible_856', ['u', 'y'])
    if urls:
        for i, u in enumerate(urls, 1):
            print(f"    [{i}] $u: {u.get('u', '')}")
            if u.get('y'):
                print(f"        $y: {u.get('y', '')}")
    else:
        print("    (vacío)")
    print()

    
    # ========================================
    # CAMPOS AUTOGENERADOS
    # ========================================
    print("📌 CAMPOS AUTOGENERADOS")
    print("-" * 110)
    print(f"  001 (num_control): Generado automáticamente")
    print(f"  005 (estado_registro): n")
    print(f"  008 (codigo_informacion): Generado con fecha y hora")
    print(f"  092 ($a): {request.POST.get('centro_catalogador', 'UNL')}")
    print(f"  092 ($b): BLMP")
    print(f"  092 ($c): {request.POST.get('codigo_pais_0_codigo_pais', 'ec')}")
    print(f"  092 ($d): Ms o Imp (según tipo_registro)")
    print()
    
    if obra:
        print("📌 DATOS GUARDADOS EN BD")
        print("-" * 110)
        print(f"  id: {obra.id}")
        print(f"  num_control: {obra.num_control}")
        print(f"  fecha_creacion_sistema: {obra.fecha_creacion_sistema}")
        print()
    
    print("=" * 110)
    print("✅ FIN DEL DEBUG")
    print("=" * 110 + "\n")


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
