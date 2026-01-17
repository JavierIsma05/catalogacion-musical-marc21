"""
Definición de todos los formsets para campos repetibles
"""

from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError

from catalogacion.models import (
    ObraGeneral,

    # Bloque 0XX
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,

    # Bloque 1XX
    FuncionCompositor,

    # Bloque 2XX
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    Lugar264,
    NombreEntidad264,
    Fecha264,

    # Bloque 3XX
    MedioInterpretacion382,
    MedioInterpretacion382_a,

    # Bloque 4XX
    MencionSerie490,

    # Bloque 5XX
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,

    # Bloque 6XX
    Materia650,
    MateriaGenero655,

    # Bloque 7XX
    NombreRelacionado700,
    TerminoAsociado700,
    Funcion700,
    EntidadRelacionada710,
    EnlaceDocumentoFuente773,
    NumeroControl773,
    EnlaceUnidadConstituyente774,
    NumeroControl774,
    OtrasRelaciones787,
    NumeroControl787,

    # Bloque 8XX
    Ubicacion852,
    Estanteria852,
    Disponible856,
)

# IMPORTAR FORMULARIOS
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

from .forms_4xx import MencionSerie490Form

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

# =====================================================
# FORMSETS PERSONALIZADOS
# =====================================================

class IncipitMusicalFormSet(BaseInlineFormSet):
    """Evita íncipits duplicados"""
    def clean(self):
        if any(self.errors):
            return
        
        combinaciones = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                tup = (
                    form.cleaned_data.get('numero_obra'),
                    form.cleaned_data.get('numero_movimiento'),
                    form.cleaned_data.get('numero_pasaje')
                )
                if tup in combinaciones:
                    raise ValidationError("Íncipit duplicado.")
                combinaciones.append(tup)


class Materia650FormSet(BaseInlineFormSet):
    """Evita materias duplicadas"""
    def clean(self):
        if any(self.errors):
            return
        
        materias = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                materia = form.cleaned_data.get('materia')
                if materia in materias:
                    raise ValidationError(f"La materia '{materia}' está duplicada.")
                materias.append(materia)


# =====================================================
# BLOQUE 0XX
# =====================================================

IncipitMusicalFormSet = inlineformset_factory(
    ObraGeneral,
    IncipitMusical,
    form=IncipitMusicalForm,
    formset=IncipitMusicalFormSet,
    extra=1,
    can_delete=True,
)

IncipitURLFormSet = inlineformset_factory(
    IncipitMusical,
    IncipitURL,
    form=IncipitURLForm,
    extra=1,
    can_delete=True,
)

CodigoLenguaFormSet = inlineformset_factory(
    ObraGeneral,
    CodigoLengua,
    form=CodigoLenguaForm,
    extra=1,
    can_delete=True,
)

IdiomaObraFormSet = inlineformset_factory(
    CodigoLengua,
    IdiomaObra,
    form=IdiomaObraForm,
    extra=1,
    can_delete=True,
)

CodigoPaisEntidadFormSet = inlineformset_factory(
    ObraGeneral,
    CodigoPaisEntidad,
    form=CodigoPaisEntidadForm,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 1XX
# =====================================================

FuncionCompositorFormSet = inlineformset_factory(
    ObraGeneral,
    FuncionCompositor,
    form=FuncionCompositorForm,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 2XX
# =====================================================

TituloAlternativoFormSet = inlineformset_factory(
    ObraGeneral,
    TituloAlternativo,
    form=TituloAlternativoForm,
    extra=1,
    can_delete=True,
)

EdicionFormSet = inlineformset_factory(
    ObraGeneral,
    Edicion,
    form=EdicionForm,
    extra=1,
    can_delete=True,
)

ProduccionPublicacionFormSet = inlineformset_factory(
    ObraGeneral,
    ProduccionPublicacion,
    form=ProduccionPublicacionForm,
    extra=1,
    can_delete=True,
)

Lugar264FormSet = inlineformset_factory(
    ProduccionPublicacion,
    Lugar264,
    form=Lugar264Form,
    extra=1,
    can_delete=True,
)

NombreEntidad264FormSet = inlineformset_factory(
    ProduccionPublicacion,
    NombreEntidad264,
    form=NombreEntidad264Form,
    extra=1,
    can_delete=True,
)

Fecha264FormSet = inlineformset_factory(
    ProduccionPublicacion,
    Fecha264,
    form=Fecha264Form,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 3XX
# =====================================================

MedioInterpretacion382FormSet = inlineformset_factory(
    ObraGeneral,
    MedioInterpretacion382,
    form=MedioInterpretacion382Form,
    extra=1,
    can_delete=True,
)

MedioInterpretacion382_aFormSet = inlineformset_factory(
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    form=MedioInterpretacion382_aForm,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 4XX
# =====================================================

MencionSerie490FormSet = inlineformset_factory(
    ObraGeneral,
    MencionSerie490,
    form=MencionSerie490Form,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 5XX
# =====================================================

NotaGeneral500FormSet = inlineformset_factory(
    ObraGeneral,
    NotaGeneral500,
    form=NotaGeneral500Form,
    extra=1,
    can_delete=True,
)

Contenido505FormSet = inlineformset_factory(
    ObraGeneral,
    Contenido505,
    form=Contenido505Form,
    extra=1,
    can_delete=True,
)

Sumario520FormSet = inlineformset_factory(
    ObraGeneral,
    Sumario520,
    form=Sumario520Form,
    extra=1,
    can_delete=True,
)

DatosBiograficos545FormSet = inlineformset_factory(
    ObraGeneral,
    DatosBiograficos545,
    form=DatosBiograficos545Form,
    extra=1,
    max_num=1,
    validate_max=True,
    can_delete=True,
)

# =====================================================
# BLOQUE 6XX
# =====================================================

Materia650FormSet = inlineformset_factory(
    ObraGeneral,
    Materia650,
    form=Materia650Form,
    formset=Materia650FormSet,
    extra=1,
    can_delete=True,
)

MateriaGenero655FormSet = inlineformset_factory(
    ObraGeneral,
    MateriaGenero655,
    form=MateriaGenero655Form,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 7XX
# =====================================================

NombreRelacionado700FormSet = inlineformset_factory(
    ObraGeneral,
    NombreRelacionado700,
    form=NombreRelacionado700Form,
    extra=1,
    can_delete=True,
)

TerminoAsociado700FormSet = inlineformset_factory(
    NombreRelacionado700,
    TerminoAsociado700,
    form=TerminoAsociado700Form,
    extra=1,
    can_delete=True,
)

Funcion700FormSet = inlineformset_factory(
    NombreRelacionado700,
    Funcion700,
    form=Funcion700Form,
    extra=1,
    can_delete=True,
)

EntidadRelacionada710FormSet = inlineformset_factory(
    ObraGeneral,
    EntidadRelacionada710,
    form=EntidadRelacionada710Form,
    extra=1,
    can_delete=True,
)

EnlaceDocumentoFuente773FormSet = inlineformset_factory(
    ObraGeneral,
    EnlaceDocumentoFuente773,
    form=EnlaceDocumentoFuente773Form,
    extra=1,
    can_delete=True,
)

NumeroControl773FormSet = inlineformset_factory(
    EnlaceDocumentoFuente773,
    NumeroControl773,
    form=NumeroControl773Form,
    extra=1,
    can_delete=True,
)

EnlaceUnidadConstituyente774FormSet = inlineformset_factory(
    ObraGeneral,
    EnlaceUnidadConstituyente774,
    form=EnlaceUnidadConstituyente774Form,
    extra=1,
    can_delete=True,
)

NumeroControl774FormSet = inlineformset_factory(
    EnlaceUnidadConstituyente774,
    NumeroControl774,
    form=NumeroControl774Form,
    extra=1,
    can_delete=True,
)

OtrasRelaciones787FormSet = inlineformset_factory(
    ObraGeneral,
    OtrasRelaciones787,
    form=OtrasRelaciones787Form,
    extra=1,
    can_delete=True,
)

NumeroControl787FormSet = inlineformset_factory(
    OtrasRelaciones787,
    NumeroControl787,
    form=NumeroControl787Form,
    extra=1,
    can_delete=True,
)

# =====================================================
# BLOQUE 8XX
# =====================================================

Ubicacion852FormSet = inlineformset_factory(
    ObraGeneral,
    Ubicacion852,
    form=Ubicacion852Form,
    extra=1,
    can_delete=True,
)

Estanteria852FormSet = inlineformset_factory(
    Ubicacion852,
    Estanteria852,
    form=Estanteria852Form,
    extra=1,
    can_delete=True,
)

Disponible856FormSet = inlineformset_factory(
    ObraGeneral,
    Disponible856,
    form=Disponible856Form,
    extra=1,
    can_delete=True,
)
