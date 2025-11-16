"""
Exportación centralizada de modelos MARC21.
Basado en la estructura refactorizada con modelo único.
"""

# ============================================
# AUTORIDADES
# ============================================
from .autoridades import (
    AutoridadPersona,
    AutoridadTituloUniforme,
    AutoridadFormaMusical,
    AutoridadEntidad,
    AutoridadMateria,
)

# ============================================
# MODELO PRINCIPAL
# ============================================
from .obra_general import (
    ObraGeneral,
    NumeroControlSecuencia,
)

# ============================================
# MODELOS AUXILIARES
# ============================================
from .auxiliares import (
    SoftDeleteMixin,
    HistorialCambio,
    EncabezamientoEnlace,
    ObraLengua,
)

# ============================================
# VALIDADORES
# ============================================
from .validadores import (
    ValidadorBase,
    ValidadorColeccion,
    ValidadorObraEnColeccion,
    ValidadorObraIndependiente,
    obtener_validador,
)

# ============================================
# BLOQUE 0XX
# ============================================
from .bloque_0xx import (
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
)

# ============================================
# BLOQUE 1XX
# ============================================
from .bloque_1xx import (
    FuncionCompositor,
)

# ============================================
# BLOQUE 2XX
# ============================================
from .bloque_2xx import (
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    Lugar264,
    NombreEntidad264,
    Fecha264,
)

# ============================================
# BLOQUE 3XX
# ============================================
from .bloque_3xx import (
    MedioInterpretacion382,
    MedioInterpretacion382_a,
)

# ============================================
# BLOQUE 4XX
# ============================================
from .bloque_4xx import (
    MencionSerie490,
    TituloSerie490,
    VolumenSerie490,
)

# ============================================
# BLOQUE 5XX
# ============================================
from .bloque_5xx import (
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
)

# ============================================
# BLOQUE 6XX
# ============================================
from .bloque_6xx import (
    Materia650,
    SubdivisionMateria650,
    MateriaGenero655,
    SubdivisionGeneral655,
)

# ============================================
# BLOQUE 7XX
# ============================================
from .bloque_7xx import (
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

# ============================================
# BLOQUE 8XX
# ============================================
# BLOQUE 8XX
# ============================================
from .bloque_8xx import (
    Ubicacion852,
    Estanteria852,
    Disponible856,
    URL856,
    TextoEnlace856,
)

# ============================================
# UTILIDADES
# ============================================
from .managers import ObraGeneralManager

# ============================================
# ACTIVAR SIGNALS DE AUDITORÍA
# ============================================
from . import signals_auditoria  # noqa: F401

# ============================================
# __all__ para import *
# ============================================
__all__ = [
    # Autoridades
    'AutoridadPersona',
    'AutoridadTituloUniforme',
    'AutoridadFormaMusical',
    'AutoridadEntidad',
    'AutoridadMateria',
    
    # Modelo principal
    'ObraGeneral',
    'NumeroControlSecuencia',
    
    # Modelos auxiliares
    'SoftDeleteMixin',
    'HistorialCambio',
    'EncabezamientoEnlace',
    'ObraLengua',
    
    # Validadores
    'ValidadorBase',
    'ValidadorColeccion',
    'ValidadorObraEnColeccion',
    'ValidadorObraIndependiente',
    'obtener_validador',
    
    # Bloque 0XX
    'IncipitMusical',
    'IncipitURL',
    'CodigoLengua',
    'IdiomaObra',
    'CodigoPaisEntidad',
    
    # Bloque 1XX
    'FuncionCompositor',
    
    # Bloque 2XX
    'TituloAlternativo',
    'Edicion',
    'ProduccionPublicacion',
    'Lugar264',
    'NombreEntidad264',
    'Fecha264',
    
    # Bloque 3XX
    'MedioInterpretacion382',
    'MedioInterpretacion382_a',
    
    # Bloque 4XX
    'MencionSerie490',
    'TituloSerie490',
    'VolumenSerie490',
    
    # Bloque 5XX
    'NotaGeneral500',
    'Contenido505',
    'Sumario520',
    'DatosBiograficos545',
    
    # Bloque 6XX
    'Materia650',
    'SubdivisionMateria650',
    'MateriaGenero655',
    'SubdivisionGeneral655',
    
    # Bloque 7XX
    'NombreRelacionado700',
    'TerminoAsociado700',
    'Funcion700',
    'Relacion700',
    'Autoria700',
    'EntidadRelacionada710',
    'EnlaceDocumentoFuente773',
    'EnlaceUnidadConstituyente774',
    'OtrasRelaciones787',
    
    # Bloque 8XX
    'Ubicacion852',
    'Estanteria852',
    'Disponible856',
    'URL856',
    'TextoEnlace856',
    
    # Utilidades
    'ObraGeneralManager',
]