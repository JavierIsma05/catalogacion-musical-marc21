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
        """Agrupa los valores por índice de formset (0, 1, 2, ...).

        El prefijo_input tiene formato como 'lugar_produccion_264_'
        y las keys del POST son como 'lugar_produccion_264_0_0'
        donde el primer número después del prefijo es el índice del formset.
        """
        agrupados = {}

        for key, value in self.request_post.items():
            if key.startswith(prefijo_input) and value.strip():
                try:
                    # Extraer la parte después del prefijo
                    # Ej: key='lugar_produccion_264_0_0', prefijo='lugar_produccion_264_'
                    # sufijo = '0_0' → primer número es el índice del formset
                    sufijo = key[len(prefijo_input) :]
                    partes_sufijo = sufijo.split("_")

                    # Ignorar __prefix__ (template vacío)
                    if partes_sufijo[0] == "_" or "_prefix_" in sufijo:
                        continue

                    indice_formset = int(partes_sufijo[0])
                    agrupados.setdefault(indice_formset, []).append(value.strip())
                except (ValueError, IndexError):
                    continue

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
            # 1. Asegurar que el form padre exista
            if not form.instance.pk:
                parent = form.save(commit=False)
                obra = formset.instance  # La obra que contiene este 856
                parent.obra = obra
                parent.save()

            # 2. Ahora SÍ tiene pk
            instance = form.instance

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
        campo_fk="materia650",
        campo_valor="subdivision",
    )


def save_subdivisiones_geograficas_650(request_post, formset):
    """Guarda subdivisiones geográficas (650 $z)"""
    from catalogacion.models import SubdivisionCronologica650

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input="subdivision_cronologica_650_",
        modelo_subcampo=SubdivisionCronologica650,
        campo_fk="materia650",
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


def _save_urls_856(request_post, disponibles):
    from catalogacion.models import URL856

    # 🔥 Recorremos POST en orden, no por índice
    for key, value in request_post.items():
        if not key.startswith("url_disponible_856_"):
            continue

        if not value.strip():
            continue

        try:
            _, _, _, orden = key.split("_", 3)
        except ValueError:
            continue

        # 🔐 USAR EL ORDEN REAL, NO EL ÍNDICE DEL NAME
        try:
            disponible = disponibles.pop(0)
        except IndexError:
            break  # no hay más padres

        URL856.objects.create(disponible=disponible, url=value.strip())


def _save_textos_enlace_856(request_post, disponibles):
    from catalogacion.models import TextoEnlace856

    for key, value in request_post.items():
        if not key.startswith("texto_disponible_856_"):
            continue

        if not value.strip():
            continue

        try:
            disponible = disponibles[0]
        except IndexError:
            break

        TextoEnlace856.objects.create(disponible=disponible, texto_enlace=value.strip())


def save_lugares_264(request_post, formset, obra=None):
    """
    Handler especial para guardar lugares del 264
    """
    from catalogacion.models import Lugar264

    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("lugar_produccion_264_", 2)
    print(f"[264] Lugares recibidos: {valores}")

    for index, form in enumerate(formset):
        if not form.instance.pk:
            parent = form.save(commit=False)
            parent.obra = obra
            parent.save()

        form.instance.lugares.all().delete()

        if index in valores:
            for valor in valores[index]:
                if valor.strip():
                    Lugar264.objects.create(
                        produccion_publicacion=form.instance, lugar=valor.strip()
                    )


def save_entidades_264(request_post, formset, obra=None):
    """
    Handler especial para guardar entidades del 264
    """
    from catalogacion.models import NombreEntidad264

    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("entidad_produccion_264_", 2)
    print(f"[264] Entidades recibidas: {valores}")

    for index, form in enumerate(formset):
        if not form.instance.pk:
            parent = form.save(commit=False)
            parent.obra = obra
            parent.save()

        form.instance.entidades.all().delete()

        if index in valores:
            for valor in valores[index]:
                if valor.strip():
                    NombreEntidad264.objects.create(
                        produccion_publicacion=form.instance, nombre=valor.strip()
                    )


def save_fechas_264(request_post, formset, obra=None):
    """
    Handler especial para guardar fechas del 264
    """
    from catalogacion.models import Fecha264

    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("fecha_produccion_264_", 2)
    print(f"[264] Fechas recibidas: {valores}")

    for index, form in enumerate(formset):
        if not form.instance.pk:
            parent = form.save(commit=False)
            parent.obra = obra
            parent.save()

        form.instance.fechas.all().delete()

        if index in valores:
            for valor in valores[index]:
                if valor.strip():
                    Fecha264.objects.create(
                        produccion_publicacion=form.instance, fecha=valor.strip()
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
    "_save_subdivisiones_geograficas_650": save_subdivisiones_geograficas_650,
    "_save_subdivisiones_655": save_subdivisiones_655,
    "_save_estanterias_852": save_estanterias_852,
    "_save_urls_856": _save_urls_856,
    "_save_textos_enlace_856": _save_textos_enlace_856,
    "_save_lugares_264": save_lugares_264,
    "_save_entidades_264": save_entidades_264,
    "_save_fechas_264": save_fechas_264,
    "_save_medios_382": save_medios_382,
    "_save_titulos_490": save_titulos_490,
    "_save_volumenes_490": save_volumenes_490,
}
