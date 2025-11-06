"""
Módulo de modelos Django para catalogación MARC21
==================================================

Importa todos los modelos organizados por bloques MARC bibliográficos.

Estructura:
- autoridades.py: Vocabularios controlados (personas, títulos, formas, materias)
- bloque_0xx.py: Campos de control y códigos (020, 024, 028, 031, 041, 044)
- bloque_1xx.py: Puntos de acceso principales (100, 130, 240)
- bloque_2xx.py: Títulos y publicación (246, 250, 264)
- bloque_3xx.py: Descripción física (300, 340, 348, 382, 383)
- bloque_4xx.py: Series (490)
- bloque_5xx.py: Notas y contenido (500, 505, 520, 545)
- bloque_6xx.py: Materias y género/forma (650, 655)
- bloque_7xx.py: Accesos adicionales y relaciones (700, 710, 773, 774, 787)
- bloque_8xx.py: Ubicación y disponibilidad (852, 856)
- obra_general.py: Modelo principal ObraGeneral
"""

# =====================================================
# Importar autoridades
# =====================================================
from .autoridades import (
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadMateria,
)

# =====================================================
# Importar constantes de obra_general
# =====================================================
from .obra_general import TONALIDADES

# =====================================================
# Importar modelos bloque 0XX
# =====================================================
from .bloque_0xx import (
    CODIGOS_LENGUAJE,
    ISBN,
    ISMN,
    NumeroEditor,
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
)

# =====================================================
# Importar modelos bloque 1XX
# =====================================================
from .bloque_1xx import (
    FORMAS_MUSICALES,
    FuncionCompositor,
    AtribucionCompositor,
    Forma130,
    MedioInterpretacion130,
    NumeroParteSección130,
    NombreParteSección130,
    Forma240,
    MedioInterpretacion240,
    NumeroParteSección240,
    NombreParteSección240,
)

# =====================================================
# Importar modelos bloque 2XX
# =====================================================
from .bloque_2xx import (
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
)

# =====================================================
# Importar modelos bloque 3XX
# =====================================================
from .bloque_3xx import (
    DescripcionFisica,
    Extension300,
    Dimension300,
    MedioFisico,
    Tecnica340,
    CaracteristicaMusicaNotada,
    Formato348,
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    Solista382,
    NumeroInterpretes382,
    DesignacionNumericaObra,
    NumeroObra383,
    Opus383,
)

# =====================================================
# Importar modelos bloque 4XX
# =====================================================
from .bloque_4xx import (
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
)

# =====================================================
# Importar modelos bloque 5XX - Notas y contenido
# =====================================================
from .bloque_5xx import (
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
)

# =====================================================
# Importar modelos bloque 6XX - Materias y género/forma
# =====================================================
from .bloque_6xx import (
    Materia650,
    SubdivisionMateria650,
    MateriaGenero655,
    SubdivisionGeneral655,
)

# =====================================================
# Importar modelos bloque 7XX - Accesos adicionales y relaciones
# =====================================================
from .bloque_7xx import (
    FUNCIONES_PERSONA,
    AUTORIAS_CHOICES,
    FUNCIONES_ENTIDAD,
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    Relacion700,
    Autoria700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    EnlaceUnidadConstituyente774,
    OtrasRelaciones787,
)

# =====================================================
# Importar modelos bloque 8XX - Ubicación y disponibilidad
# =====================================================
from .bloque_8xx import (
    Ubicacion852, Estanteria852, Disponible856
)

# =====================================================
# Importar modelo principal
# =====================================================
from .obra_general import ObraGeneral


# =====================================================
# Exportar todos los modelos
# =====================================================
__all__ = [
    # Constantes
    'TONALIDADES',
    'CODIGOS_LENGUAJE',
    'FORMAS_MUSICALES',
    
    # Autoridades
    'AutoridadPersona',
    'AutoridadTituloUniforme',
    'AutoridadFormaMusical',
    'AutoridadMateria',
    
    # Bloque 0XX - Control y códigos
    'ISBN',
    'ISMN',
    'NumeroEditor',
    'IncipitMusical',
    'IncipitURL',
    'CodigoLengua',
    'IdiomaObra',
    'CodigoPaisEntidad',
    
    # Bloque 1XX - Puntos de acceso principales
    'FuncionCompositor',
    'AtribucionCompositor',
    'Forma130',
    'MedioInterpretacion130',
    'NumeroParteSección130',
    'NombreParteSección130',
    'Forma240',
    'MedioInterpretacion240',
    'NumeroParteSección240',
    'NombreParteSección240',
    
    # Bloque 2XX - Títulos y publicación
    'TituloAlternativo',
    'Edicion',
    'ProduccionPublicacion',
    
    # Bloque 3XX - Descripción física
    'DescripcionFisica',
    'Extension300',
    'Dimension300',
    'MedioFisico',
    'Tecnica340',
    'CaracteristicaMusicaNotada',
    'Formato348',
    'MedioInterpretacion382',
    'MedioInterpretacion382_a',
    'Solista382',
    'NumeroInterpretes382',
    'DesignacionNumericaObra',
    'NumeroObra383',
    'Opus383',
    
    # Bloque 4XX - Series
    'MencionSerie490',
    'TituloSerie490',
    'VolumenSerie490',

    # Bloque 5XX - Notas y contenido
    'NotaGeneral500',
    'Contenido505',
    'Sumario520',
    'DatosBiograficos545',

    # Bloque 6XX - Materias y género/forma
    'Materia650',
    'SubdivisionMateria650',
    'MateriaGenero655',
    'SubdivisionGeneral655',

   # Bloque 7XX
    'FUNCIONES_PERSONA', 
    'AUTORIAS_CHOICES', 
    'FUNCIONES_ENTIDAD',
    'NombreRelacionado700', 
    'TerminoAsociado700', 
    'Funcion700',
    'Relacion700', 
    'Autoria700', 
    'EntidadRelacionada710',
    'EnlaceDocumentoFuente773', 
    'EnlaceUnidadConstituyente774', 
    'OtrasRelaciones787',
    

    # Bloque 8XX - Ubicación y disponibilidad
    'Ubicacion852', 
    'Estanteria852',
    'Disponible856',

    
    # Modelo principal
    'ObraGeneral',
]
