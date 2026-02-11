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
        'punto_acceso': '100',  # Compositor
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


# =====================================================
# CAMPOS VISIBLES POR TIPO DE OBRA
# Basado en las plantillas MARC21 específicas
# =====================================================

CAMPOS_POR_TIPO_OBRA = {
    'coleccion_manuscrita': {
        # Campos principales
        'campos_simples': [
            '001', '005', '008', '040', '041', '044', '092',  # 0XX
            '100', '130',  # 1XX - Compositor y título uniforme principal
            '240', '245', '246', '264',  # 2XX
            '300', '340', '348', '382',  # 3XX
            '500', '505', '520', '545',  # 5XX
            '650', '655',  # 6XX
            '700', '710', '774',  # 7XX - Obras constituyentes (NO 773)
            '852', '856',  # 8XX
        ],
        # Formsets que deben mostrarse
        'formsets_visibles': [
            'codigos_lengua',
            'codigos_pais',
            # NO incluye incipits_musicales
            'funciones_compositor',
            'titulos_alternativos',
            'produccion_publicacion',
            'medios_interpretacion',
            'notas_generales',
            'contenidos',
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            # NO incluye enlaces_documento_fuente_773
            'enlaces_unidad_constituyente_774',  # Obras en esta colección
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
    'obra_en_coleccion_manuscrita': {
        'campos_simples': [
            '001', '005', '008', '031', '040', '041', '044', '092',  # 0XX con íncipit
            '100',  # 1XX - Compositor
            '240', '245', '246', '264',  # 2XX
            '300', '340', '348', '382', '383', '384',  # 3XX con designación y tonalidad
            '500', '520', '545',  # 5XX (sin 505 contenido)
            '650', '655',  # 6XX
            '700', '710', '773',  # 7XX - Enlace a colección padre (NO 774)
            '852', '856',  # 8XX
        ],
        'formsets_visibles': [
            'incipits_musicales',  # Incluye íncipit
            'codigos_lengua',
            'codigos_pais',
            'funciones_compositor',  # Incluye compositor
            'titulos_alternativos',
            'produccion_publicacion',
            'medios_interpretacion',
            'notas_generales',
            # NO incluye contenidos (505)
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            'enlaces_documento_fuente_773',  # Enlace a colección
            # NO incluye enlaces_unidad_constituyente_774
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
    'obra_manuscrita_individual': {
        'campos_simples': [
            '001', '005', '008', '031', '040', '041', '044', '092',  # 0XX con íncipit
            '100',  # 1XX - Compositor
            '240', '245', '246', '264',  # 2XX
            '300', '340', '348', '382', '383', '384',  # 3XX completo
            '500', '520', '545',  # 5XX
            '650', '655',  # 6XX
            '700', '710', '787',  # 7XX - Otras relaciones (NO 773 ni 774)
            '852', '856',  # 8XX
        ],
        'formsets_visibles': [
            'incipits_musicales',
            'codigos_lengua',
            'codigos_pais',
            'funciones_compositor',
            'titulos_alternativos',
            'produccion_publicacion',
            'medios_interpretacion',
            'notas_generales',
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            # NO incluye enlaces_documento_fuente_773
            # NO incluye enlaces_unidad_constituyente_774
            'otras_relaciones_787',  # Otras relaciones
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
    'coleccion_impresa': {
        # Igual que coleccion_manuscrita pero con tipo_registro='c'
        'campos_simples': [
            '001', '005', '008', '020', '024', '028', '040', '041', '044', '092',  # 0XX
            '100', '130',  # 1XX - Compositor y título uniforme principal
            '240', '245', '246', '250', '264',  # 2XX
            '300', '340', '348', '382',  # 3XX
            '490',  # 4XX
            '500', '505', '520', '545',  # 5XX
            '650', '655',  # 6XX
            '700', '710', '774',  # 7XX
            '852', '856',  # 8XX
        ],
        'formsets_visibles': [
            'codigos_lengua',
            'codigos_pais',
            'funciones_compositor',
            'titulos_alternativos',
            'ediciones',
            'produccion_publicacion',
            'medios_interpretacion',
            'menciones_serie_490',
            'notas_generales',
            'contenidos',
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            'enlaces_unidad_constituyente_774',
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
    'obra_en_coleccion_impresa': {
        # Igual que obra_en_coleccion_manuscrita
        'campos_simples': [
            '001', '005', '008', '031', '040', '041', '044', '092',
            '100',
            '240', '245', '246', '264',
            '300', '340', '348', '382', '383', '384',
            '500', '520', '545',
            '650', '655',
            '700', '710', '773',
            '852', '856',
        ],
        'formsets_visibles': [
            'incipits_musicales',
            'codigos_lengua',
            'codigos_pais',
            'funciones_compositor',
            'titulos_alternativos',
            'produccion_publicacion',
            'medios_interpretacion',
            'notas_generales',
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            'enlaces_documento_fuente_773',
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
    'obra_impresa_individual': {
        # Igual que obra_manuscrita_individual
        'campos_simples': [
            '001', '005', '008', '020', '024', '028', '031', '040', '041', '044', '092',
            '100',
            '240', '245', '246', '250', '264',
            '300', '340', '348', '382', '383', '384',
            '490',
            '500', '520', '545',
            '650', '655',
            '700', '710', '787',
            '852', '856',
        ],
        'formsets_visibles': [
            'incipits_musicales',
            'codigos_lengua',
            'codigos_pais',
            'funciones_compositor',
            'titulos_alternativos',
            'ediciones',
            'produccion_publicacion',
            'medios_interpretacion',
            'menciones_serie_490',
            'notas_generales',
            'sumarios',
            'datos_biograficos',
            'materias_650',
            'materias_genero_655',
            'nombres_relacionados_700',
            'entidades_relacionadas_710',
            'otras_relaciones_787',
            'ubicaciones_852',
            'disponibles_856',
        ],
    },
}


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def get_campos_visibles(tipo_obra):
    """
    Retorna la configuración de campos visibles para un tipo de obra.
    
    Args:
        tipo_obra: clave del tipo de obra en TIPO_OBRA_CONFIG
        
    Returns:
        dict con 'campos_simples' y 'formsets_visibles'
    """
    return CAMPOS_POR_TIPO_OBRA.get(tipo_obra, {})


def debe_mostrar_campo(tipo_obra, campo_marc):
    """
    Determina si un campo MARC debe mostrarse para un tipo de obra.
    
    Args:
        tipo_obra: clave del tipo de obra
        campo_marc: número de campo MARC (ej: '031', '100', '773')
        
    Returns:
        bool: True si el campo debe mostrarse
    """
    config = CAMPOS_POR_TIPO_OBRA.get(tipo_obra, {})
    return campo_marc in config.get('campos_simples', [])


def debe_mostrar_formset(tipo_obra, formset_name):
    """
    Determina si un formset debe mostrarse para un tipo de obra.
    
    Args:
        tipo_obra: clave del tipo de obra
        formset_name: nombre del formset (ej: 'incipit_musical_formset')
        
    Returns:
        bool: True si el formset debe mostrarse
    """
    config = CAMPOS_POR_TIPO_OBRA.get(tipo_obra, {})
    return formset_name in config.get('formsets_visibles', [])



FORMSETS_CONFIG = {
    # Bloque 0XX - Números de control e información codificada
    '0xx': [
        'incipits_musicales',
        'codigos_lengua',
        'codigos_pais',
    ],
    
    # Bloque 1XX - Encabezamiento principal
    '1xx': [
        'funciones_compositor',
    ],
    
    # Bloque 2XX - Títulos y menciones de edición/publicación
    '2xx': [
        'titulos_alternativos',
        'ediciones',
        'produccion_publicacion',
    ],
    
    # Bloque 3XX - Descripción física
    '3xx': [
        'medios_interpretacion',
    ],
    
    # Bloque 4XX - Mención de serie
    '4xx': [
        'menciones_serie_490',
    ],
    
    # Bloque 5XX - Notas
    '5xx': [
        'notas_generales',
        'contenidos',
        'sumarios',
        'datos_biograficos',
    ],
    
    # Bloque 6XX - Encabezamientos de materia
    '6xx': [
        'materias_650',
        'materias_genero_655',
    ],
    
    # Bloque 7XX - Asientos secundarios
    '7xx': [
        'nombres_relacionados_700',
        'entidades_relacionadas_710',
        'enlaces_documento_fuente_773',
        'enlaces_unidad_constituyente_774',
        'otras_relaciones_787',
    ],
    
    # Bloque 8XX - Números y códigos alternativos
    '8xx': [
        'ubicaciones_852',
        'disponibles_856',
    ],
}


# Formsets que requieren procesamiento especial de subcampos
FORMSETS_CON_SUBCAMPOS = {
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
    # Campo 264 - Producción/Publicación
    'produccion_publicacion_formset': {
        'subcampos': ['lugar', 'entidad', 'fecha'],
        'handler_lugar': '_save_lugares_264',
        'handler_entidad': '_save_entidades_264',
        'handler_fecha': '_save_fechas_264',
    },
    # Campo 382 - Medio de interpretación
    'medio_interpretacion_382_formset': {
        'subcampos': ['medio'],
        'handler': '_save_medios_382',
    },
    # Campo 490 - Mención de serie
    'mencion_serie_490_formset': {
        'subcampos': ['titulo', 'volumen'],
        'handler_titulo': '_save_titulos_490',
        'handler_volumen': '_save_volumenes_490',
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
