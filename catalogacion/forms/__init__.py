"""
Exportación centralizada de formularios MARC21
"""

# Formulario principal
from .obra_base import ObraGeneralForm
from .autoridades import (
    AutoridadPersonaForm,
    AutoridadEntidadForm,
    AutoridadFormaMusicalForm,
    AutoridadMateriaForm,
    AutoridadTituloUniformeForm,
)

# Forms por bloque
from .forms_0xx import (
    IncipitMusicalForm,
    IncipitURLForm,
    CodigoLenguaForm,
    IdiomaObraForm,
    CodigoPaisEntidadForm,
)

from .forms_1xx import FuncionCompositorForm

from .forms_2xx import (
    TituloAlternativoForm,
    EdicionForm,
    ProduccionPublicacionForm,
    Lugar264Form,
    NombreEntidad264Form,
    Fecha264Form,
)

from .forms_3xx import (
    MedioInterpretacion382Form,
    MedioInterpretacion382_aForm,
)

from .forms_4xx import (
    MencionSerie490Form,
)

from .forms_5xx import (
    NotaGeneral500Form,
    Contenido505Form,
    Sumario520Form,
    DatosBiograficos545Form,
)

from .forms_6xx import (
    Materia650Form,
    MateriaGenero655Form,
)

from .forms_7xx import (
    NombreRelacionado700Form,
    TerminoAsociado700Form,
    Funcion700Form,
    EntidadRelacionada710Form,
    EnlaceDocumentoFuente773Form,
    NumeroControl773Form,
    EnlaceUnidadConstituyente774Form,
    NumeroControl774Form,
    OtrasRelaciones787Form,
    NumeroControl787Form,
)

from .forms_8xx import (
    Ubicacion852Form,
    Estanteria852Form,
    Disponible856Form,
)

# ----------------------------
# FORMSETS (CORREGIDOS)
# ----------------------------

from .formsets import (
    # Bloque 0XX
    IncipitMusicalFormSet,
    IncipitURLFormSet,
    CodigoLenguaFormSet,
    IdiomaObraFormSet,
    CodigoPaisEntidadFormSet,

    # Bloque 1XX
    FuncionCompositorFormSet,

    # Bloque 2XX
    TituloAlternativoFormSet,
    EdicionFormSet,
    ProduccionPublicacionFormSet,
    Lugar264FormSet,
    NombreEntidad264FormSet,
    Fecha264FormSet,

    # Bloque 3XX
    MedioInterpretacion382FormSet,
    MedioInterpretacion382_aFormSet,

    # Bloque 4XX
    MencionSerie490FormSet,

    # Bloque 5XX
    NotaGeneral500FormSet,
    Contenido505FormSet,
    Sumario520FormSet,
    DatosBiograficos545FormSet,

    # Bloque 6XX
    Materia650FormSet,
    MateriaGenero655FormSet,

    # Bloque 7XX
    NombreRelacionado700FormSet,
    TerminoAsociado700FormSet,
    Funcion700FormSet,
    EntidadRelacionada710FormSet,
    EnlaceDocumentoFuente773FormSet,
    NumeroControl773FormSet,
    EnlaceUnidadConstituyente774FormSet,
    NumeroControl774FormSet,
    OtrasRelaciones787FormSet,
    NumeroControl787FormSet,

    # Bloque 8XX
    Ubicacion852FormSet,
    Estanteria852FormSet,
    Disponible856FormSet,
)

# Widgets personalizados
from .widgets import (
    Select2Widget,
    DatePickerWidget,
    TextAreaAutosize,
)

__all__ = [
    # Form principal
    'ObraGeneralForm',

    # Autoridades
    'AutoridadPersonaForm',
    'AutoridadEntidadForm',
    'AutoridadFormaMusicalForm',
    'AutoridadMateriaForm',
    'AutoridadTituloUniformeForm',

    # Forms bloque 0XX
    'IncipitMusicalForm',
    'IncipitURLForm',
    'CodigoLenguaForm',
    'IdiomaObraForm',
    'CodigoPaisEntidadForm',

    # Forms bloque 1XX
    'FuncionCompositorForm',

    # Forms bloque 2XX
    'TituloAlternativoForm',
    'EdicionForm',
    'ProduccionPublicacionForm',
    'Lugar264Form',
    'NombreEntidad264Form',
    'Fecha264Form',

    # Forms bloque 3XX
    'MedioInterpretacion382Form',
    'MedioInterpretacion382_aForm',

    # Forms bloque 4XX
    'MencionSerie490Form',

    # Forms bloque 5XX
    'NotaGeneral500Form',
    'Contenido505Form',
    'Sumario520Form',
    'DatosBiograficos545Form',

    # Forms bloque 6XX
    'Materia650Form',
    'MateriaGenero655Form',

    # Forms bloque 7XX
    'NombreRelacionado700Form',
    'TerminoAsociado700Form',
    'Funcion700Form',
    'EntidadRelacionada710Form',
    'EnlaceDocumentoFuente773Form',
    'NumeroControl773Form',
    'EnlaceUnidadConstituyente774Form',
    'NumeroControl774Form',
    'OtrasRelaciones787Form',
    'NumeroControl787Form',

    # Forms bloque 8XX
    'Ubicacion852Form',
    'Estanteria852Form',
    'Disponible856Form',

    # Formsets 0XX
    'IncipitMusicalFormSet',
    'IncipitURLFormSet',
    'CodigoLenguaFormSet',
    'IdiomaObraFormSet',
    'CodigoPaisEntidadFormSet',

    # Formsets 1XX
    'FuncionCompositorFormSet',

    # Formsets 2XX
    'TituloAlternativoFormSet',
    'EdicionFormSet',
    'ProduccionPublicacionFormSet',
    'Lugar264FormSet',
    'NombreEntidad264FormSet',
    'Fecha264FormSet',

    # Formsets 3XX
    'MedioInterpretacion382FormSet',
    'MedioInterpretacion382_aFormSet',

    # Formsets 4XX
    'MencionSerie490FormSet',

    # Formsets 5XX
    'NotaGeneral500FormSet',
    'Contenido505FormSet',
    'Sumario520FormSet',
    'DatosBiograficos545FormSet',

    # Formsets 6XX
    'Materia650FormSet',
    'MateriaGenero655FormSet',

    # Formsets 7XX
    'NombreRelacionado700FormSet',
    'TerminoAsociado700FormSet',
    'Funcion700FormSet',
    'EntidadRelacionada710FormSet',
    'EnlaceDocumentoFuente773FormSet',
    'NumeroControl773FormSet',
    'EnlaceUnidadConstituyente774FormSet',
    'NumeroControl774FormSet',
    'OtrasRelaciones787FormSet',
    'NumeroControl787FormSet',

    # Formsets 8XX
    'Ubicacion852FormSet',
    'Estanteria852FormSet',
    'Disponible856FormSet',

    # Widgets
    'Select2Widget',
    'DatePickerWidget',
    'TextAreaAutosize',
]
