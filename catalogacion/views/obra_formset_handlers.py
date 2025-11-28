"""
Handlers para procesamiento de formsets con subcampos dinámicos en MARC21.
Cada subcampo repetible que llega vía JavaScript se agrupa por índice de
formset y se guarda de forma encadenada en la base de datos.
"""


class FormsetSubcampoHandler:
    """Procesa los subcampos repetibles enviados desde inputs dinámicos."""

    def __init__(self, request_post):
        self.request_post = request_post

    def _agrupar_subcampos_por_indice(self, prefijo_input, indice_posicion=3):
        """Agrupa los valores por índice de formset (0, 1, 2, ...)."""
        agrupados = {}

        for key, value in self.request_post.items():
            if key.startswith(prefijo_input) and value.strip():
                try:
                    parts = key.split('_')
                    indice = int(parts[indice_posicion])
                except (ValueError, IndexError):
                    continue

                agrupados.setdefault(indice, []).append(value.strip())

        return agrupados

    def procesar_subcampo_simple(
        self,
        formset,
        prefijo_input,
        modelo_subcampo,
        campo_fk,
        campo_valor,
        indice_posicion=3,
    ):
        """Reemplaza los subcampos asociados a cada formulario guardado."""

        valores = self._agrupar_subcampos_por_indice(prefijo_input, indice_posicion)

        for index, form in enumerate(formset):
            if not form.instance.pk:
                continue

            if index not in valores:
                continue

            relacionado = getattr(
                form.instance,
                modelo_subcampo._meta.get_field(campo_fk).related_query_name(),
            )
            relacionado.all().delete()

            for valor in valores[index]:
                modelo_subcampo.objects.create(
                    **{
                        campo_fk: form.instance,
                        campo_valor: valor,
                    }
                )


# ================================================================
# HANDLERS ESPECÍFICOS
# ================================================================

def save_subdivisiones_650(request_post, formset):
    from catalogacion.models import SubdivisionMateria650

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input="subdivision_materia_650_",
        modelo_subcampo=SubdivisionMateria650,
        campo_fk="materia",
        campo_valor="subdivision",
    )


def save_subdivisiones_655(request_post, formset):
    from catalogacion.models import SubdivisionGeneral655

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input="subdivision_genero_655_",
        modelo_subcampo=SubdivisionGeneral655,
        campo_fk="materia655",
        campo_valor="subdivision",
    )


def save_estanterias_852(request_post, formset):
    from catalogacion.models import Estanteria852

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "estanteria_ubicacion_852_",
        Estanteria852,
        "ubicacion",
        "estanteria",
    )


def save_urls_856(request_post, formset):
    from catalogacion.models import URL856

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "url_disponible_856_",
        URL856,
        "disponible",
        "url",
    )


def save_textos_enlace_856(request_post, formset):
    from catalogacion.models import TextoEnlace856

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "texto_disponible_856_",
        TextoEnlace856,
        "disponible",
        "texto_enlace",
    )


def save_lugares_264(request_post, formset):
    from catalogacion.models import Lugar264

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "lugar_produccion_264_",
        Lugar264,
        "produccion_publicacion",
        "lugar",
    )


def save_entidades_264(request_post, formset):
    from catalogacion.models import NombreEntidad264

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "entidad_produccion_264_",
        NombreEntidad264,
        "produccion_publicacion",
        "nombre",
    )


def save_fechas_264(request_post, formset):
    from catalogacion.models import Fecha264

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "fecha_produccion_264_",
        Fecha264,
        "produccion_publicacion",
        "fecha",
    )


def save_medios_382(request_post, formset):
    from catalogacion.models import MedioInterpretacion382_a

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "medio_interpretacion_382_",
        MedioInterpretacion382_a,
        "medio_interpretacion",
        "medio",
    )


def save_titulos_490(request_post, formset):
    from catalogacion.models import TituloSerie490

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "titulo_mencion_490_",
        TituloSerie490,
        "serie",
        "titulo_serie",
    )


def save_volumenes_490(request_post, formset):
    from catalogacion.models import VolumenSerie490

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset,
        "volumen_mencion_490_",
        VolumenSerie490,
        "serie",
        "volumen",
    )


# ================================================================
# MAPEO DE HANDLERS REGISTRADOS
# ================================================================

SUBCAMPO_HANDLERS = {
    "_save_subdivisiones_650": save_subdivisiones_650,
    "_save_subdivisiones_655": save_subdivisiones_655,
    "_save_estanterias_852": save_estanterias_852,
    "_save_urls_856": save_urls_856,
    "_save_textos_enlace_856": save_textos_enlace_856,
    "_save_lugares_264": save_lugares_264,
    "_save_entidades_264": save_entidades_264,
    "_save_fechas_264": save_fechas_264,
    "_save_medios_382": save_medios_382,
    "_save_titulos_490": save_titulos_490,
    "_save_volumenes_490": save_volumenes_490,
}
