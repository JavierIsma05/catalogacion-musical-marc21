"""
Configuraciones y constantes para gestión de obras MARC21
"""

# Mapeo de tipos de obra a configuraciones MARC21
TIPO_OBRA_CONFIG = {
    'coleccion_manuscrita': {
        'titulo': 'Colección Manuscrita',
        'descripcion': 'Conjunto de obras manuscritas sin compositor único',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'c',
        'punto_acceso': '130',  # Título uniforme principal
    },
    'obra_en_coleccion_manuscrita': {
        'titulo': 'Obra en Colección Manuscrita',
        'descripcion': 'Obra individual manuscrita dentro de una colección',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'a',
        'punto_acceso': '100',  # Compositor
    },
    'obra_manuscrita_individual': {
        'titulo': 'Obra Manuscrita Individual',
        'descripcion': 'Obra manuscrita completa e independiente',
        'tipo_registro': 'd',
        'nivel_bibliografico': 'm',
        'punto_acceso': '100',  # Compositor
    },
    'coleccion_impresa': {
        'titulo': 'Colección Impresa',
        'descripcion': 'Conjunto de obras publicadas',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'c',
        'punto_acceso': '130',  # Título uniforme principal
    },
    'obra_en_coleccion_impresa': {
        'titulo': 'Obra en Colección Impresa',
        'descripcion': 'Obra individual publicada dentro de una colección',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'a',
        'punto_acceso': '100',  # Compositor
    },
    'obra_impresa_individual': {
        'titulo': 'Obra Impresa Individual',
        'descripcion': 'Obra publicada completa e independiente',
        'tipo_registro': 'c',
        'nivel_bibliografico': 'm',
        'punto_acceso': '100',  # Compositor
    },
}


# Formsets para cada bloque MARC21
FORMSETS_CONFIG = {
    # Bloque 0XX - Números de control e información codificada
    '0xx': [
        'incipit_musical_formset',
        'codigo_lengua_formset',
        'codigo_pais_entidad_formset',
    ],
    
    # Bloque 1XX - Encabezamiento principal
    '1xx': [
        'funcion_compositor_formset',
    ],
    
    # Bloque 2XX - Títulos y menciones de edición/publicación
    '2xx': [
        'titulo_alternativo_formset',
        'edicion_formset',
        'produccion_publicacion_formset',
    ],
    
    # Bloque 3XX - Descripción física
    '3xx': [
        'medio_interpretacion_382_a_formset',
    ],
    
    # Bloque 4XX - Mención de serie
    '4xx': [
        'mencion_serie_490_formset',
    ],
    
    # Bloque 5XX - Notas
    '5xx': [
        'nota_general_500_formset',
        'contenido_505_formset',
        'sumario_520_formset',
        'datos_biograficos_545_formset',
    ],
    
    # Bloque 6XX - Encabezamientos de materia
    '6xx': [
        'materia_650_formset',
        'materia_genero_655_formset',
    ],
    
    # Bloque 7XX - Asientos secundarios
    '7xx': [
        'nombre_relacionado_700_formset',
        'entidad_relacionada_710_formset',
        'enlace_documento_fuente_773_formset',
        'enlace_unidad_constituyente_774_formset',
        'otras_relaciones_787_formset',
    ],
    
    # Bloque 8XX - Números y códigos alternativos
    '8xx': [
        'ubicacion_852_formset',
        'disponible_856_formset',
    ],
}


# Formsets que requieren procesamiento especial de subcampos
FORMSETS_CON_SUBCAMPOS = {
    # Campo 773 - Entrada del documento fuente
    'enlace_documento_fuente_773_formset': {
        'subcampos': ['numero'],
        'handler': '_save_numeros_obra_773',
    },
    # Campo 774 - Entrada de la unidad constituyente
    'enlace_unidad_constituyente_774_formset': {
        'subcampos': ['numero'],
        'handler': '_save_numeros_obra_774',
    },
    # Campo 787 - Otras relaciones
    'otras_relaciones_787_formset': {
        'subcampos': ['numero'],
        'handler': '_save_numeros_obra_787',
    },
    # Campo 852 - Ubicación
    'ubicacion_852_formset': {
        'subcampos': ['estanteria'],
        'handler': '_save_estanterias_852',
    },
    # Campo 856 - Ubicación y acceso electrónico
    'disponible_856_formset': {
        'subcampos': ['url', 'texto_enlace'],
        'handler_url': '_save_urls_856',
        'handler_texto': '_save_textos_enlace_856',
    },
    # Campo 490 - Mención de serie
    'mencion_serie_490_formset': {
        'subcampos': ['titulo', 'volumen'],
        'handler_titulo': '_save_titulos_490',
        'handler_volumen': '_save_volumenes_490',
    },
    # Campo 545 - Datos biográficos o históricos
    'datos_biograficos_545_formset': {
        'subcampos': ['texto_biografico', 'uri'],
        'handler_texto': '_save_textos_biograficos_545',
        'handler_uri': '_save_uris_545',
    },
    # Campo 650 - Encabezamiento de materia
    'materia_650_formset': {
        'subcampos': ['subdivision'],
        'handler': '_save_subdivisiones_650',
    },
    # Campo 655 - Término de indización - Género/forma
    'materia_genero_655_formset': {
        'subcampos': ['subdivision'],
        'handler': '_save_subdivisiones_655',
    },
}
