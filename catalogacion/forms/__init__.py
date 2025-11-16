"""
Exportación centralizada de formularios MARC21
"""

# Formulario principal
from .obra_base import ObraGeneralForm

# Forms por bloque
from .forms_0xx import (
    IncipitMusicalForm,
    IncipitURLForm,
    CodigoLenguaForm,
    IdiomaObraForm,
    CodigoPaisEntidadForm,
)

from .forms_1xx import (
    FuncionCompositorForm,
)

from .forms_2xx import (
    TituloAlternativoForm,
    EdicionForm,
    ProduccionPublicacionForm,
    Lugar264Form,
    NombreEntidad264Form,
    Fecha264Form,
)

from .forms_3xx import (
    DescripcionFisicaForm,
)

from .forms_5xx import (
    SumarioForm,
    NotaGeneralForm,
)

from .forms_6xx import (
    Materia650Form,
    MateriaGenero655Form,
)

from .forms_7xx import (
    NombreRelacionado700Form,
    TerminoAsociado700Form,
    Funcion700Form,
    Relacion700Form,
    Autoria700Form,
    EntidadRelacionada710Form,
    EnlaceDocumentoFuente773Form,
    EnlaceUnidadConstituyente774Form,
    OtrasRelaciones787Form,
)

from .forms_8xx import (
    SerieForm,
)

# Formsets
from .formsets import (
    # Bloque 0XX
    IncipitMusicalFormSet,
    IncipitURLFormSet,
    CodigoLenguaFormSet,
    IdiomaObraFormSet,
    CodigoPaisEntidadFormSet,
    
    # Bloque 2XX
    TituloAlternativoFormSet,
    EdicionFormSet,
    ProduccionPublicacionFormSet,
    Lugar264FormSet,
    NombreEntidad264FormSet,
    Fecha264FormSet,
    
    # Bloque 5XX
    SumarioFormSet,
    NotaGeneralFormSet,
    
    # Bloque 6XX
    Materia650FormSet,
    MateriaGenero655FormSet,
    
    # Bloque 7XX
    NombreRelacionado700FormSet,
    TerminoAsociado700FormSet,
    Funcion700FormSet,
    Relacion700FormSet,
    Autoria700FormSet,
    EntidadRelacionada710FormSet,
    EnlaceDocumentoFuente773FormSet,
    EnlaceUnidadConstituyente774FormSet,
    OtrasRelaciones787FormSet,
    
    # Bloque 8XX
    SerieFormSet,
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
    'DescripcionFisicaForm',
    
    # Forms bloque 5XX
    'SumarioForm',
    'NotaGeneralForm',
    
    # Forms bloque 6XX
    'Materia650Form',
    'MateriaGenero655Form',
    
    # Forms bloque 7XX
    'NombreRelacionado700Form',
    'TerminoAsociado700Form',
    'Funcion700Form',
    'Relacion700Form',
    'Autoria700Form',
    'EntidadRelacionada710Form',
    'EnlaceDocumentoFuente773Form',
    'EnlaceUnidadConstituyente774Form',
    'OtrasRelaciones787Form',
    
    # Forms bloque 8XX
    'SerieForm',
    
    # Formsets
    'IncipitMusicalFormSet',
    'IncipitURLFormSet',
    'CodigoLenguaFormSet',
    'IdiomaObraFormSet',
    'CodigoPaisEntidadFormSet',
    'TituloAlternativoFormSet',
    'EdicionFormSet',
    'ProduccionPublicacionFormSet',
    'Lugar264FormSet',
    'NombreEntidad264FormSet',
    'Fecha264FormSet',
    'SumarioFormSet',
    'NotaGeneralFormSet',
    'Materia650FormSet',
    'MateriaGenero655FormSet',
    'NombreRelacionado700FormSet',
    'TerminoAsociado700FormSet',
    'Funcion700FormSet',
    'Relacion700FormSet',
    'Autoria700FormSet',
    'EntidadRelacionada710FormSet',
    'EnlaceDocumentoFuente773FormSet',
    'EnlaceUnidadConstituyente774FormSet',
    'OtrasRelaciones787FormSet',
    'SerieFormSet',
    
    # Widgets
    'Select2Widget',
    'DatePickerWidget',
    'TextAreaAutosize',
]
