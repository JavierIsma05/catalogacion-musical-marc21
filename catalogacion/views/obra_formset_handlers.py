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
                    # 🔥 CORRECCIÓN: Manejar tanto creación como edición
                    if len(parts) >= 4:
                        # Formato: lugar_produccion_264_0_123 (editar) o lugar_produccion_264_0_0 (crear)
                        # El índice del formset siempre está en posición 2
                        indice_formset = int(parts[2])
                        # Ignorar el último número (puede ser PK o índice)
                    else:
                        continue

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

        URL856.objects.create(
            disponible=disponible,
            url=value.strip()
        )


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

        TextoEnlace856.objects.create(
            disponible=disponible,
            texto_enlace=value.strip()
        )


def save_lugares_264(request_post, formset, obra=None):
    """
    Handler especial para guardar lugares del 264
    """
    from catalogacion.models import Lugar264
    
    print(f"🔥 DEBUG save_lugares_264: obra={obra}, formset={formset}")
    
    # Agrupar valores por índice (ahora usa posición 2)
    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("lugar_produccion_264_", 2)
    
    print(f"🔥 DEBUG save_lugares_264: valores={valores}")
    
    for index, form in enumerate(formset):
        print(f"🔥 DEBUG save_lugares_264: procesando form {index}, pk={form.instance.pk}")
        
        # 1. Asegurar que el ProduccionPublicacion exista y tenga obra
        if not form.instance.pk:
            parent = form.save(commit=False)
            # CORRECCIÓN: Usar la obra pasada como parámetro
            parent.obra = obra
            print(f"🔥 DEBUG save_lugares_264: guardando parent con obra={obra}")
            parent.save()
            print(f"🔥 DEBUG save_lugares_264: parent guardado con pk={parent.pk}")
        
        # 2. Eliminar lugares existentes para este ProduccionPublicacion
        form.instance.lugares.all().delete()
        
        # 3. Agregar nuevos lugares si hay valores
        if index in valores:
            for valor in valores[index]:
                if valor.strip():  # Solo guardar si no está vacío
                    lugar = Lugar264.objects.create(
                        produccion_publicacion=form.instance,
                        lugar=valor.strip()
                    )
                    print(f"🔥 DEBUG save_lugares_264: lugar creado={lugar.lugar} (pk={lugar.pk})")


def save_entidades_264(request_post, formset, obra=None):
    """
    Handler especial para guardar entidades del 264
    """
    from catalogacion.models import NombreEntidad264
    
    print(f"🔥 DEBUG save_entidades_264: obra={obra}, formset={formset}")
    
    # Agrupar valores por índice (ahora usa posición 2)
    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("entidad_produccion_264_", 2)
    
    print(f"🔥 DEBUG save_entidades_264: valores={valores}")
    
    for index, form in enumerate(formset):
        print(f"🔥 DEBUG save_entidades_264: procesando form {index}, pk={form.instance.pk}")
        
        # 1. Asegurar que el ProduccionPublicacion exista y tenga obra
        if not form.instance.pk:
            parent = form.save(commit=False)
            # CORRECCIÓN: Usar la obra pasada como parámetro
            parent.obra = obra
            print(f"🔥 DEBUG save_entidades_264: guardando parent con obra={obra}")
            parent.save()
            print(f"🔥 DEBUG save_entidades_264: parent guardado con pk={parent.pk}")
        
        # 2. Eliminar entidades existentes para este ProduccionPublicacion
        form.instance.entidades.all().delete()
        
        # 3. Agregar nuevas entidades si hay valores
        if index in valores:
            for valor in valores[index]:
                if valor.strip():  # Solo guardar si no está vacío
                    entidad = NombreEntidad264.objects.create(
                        produccion_publicacion=form.instance,
                        nombre=valor.strip()
                    )
                    print(f"🔥 DEBUG save_entidades_264: entidad creada={entidad.nombre} (pk={entidad.pk})")


def save_fechas_264(request_post, formset, obra=None):
    """
    Handler especial para guardar fechas del 264
    """
    from catalogacion.models import Fecha264
    
    print(f"🔥 DEBUG save_fechas_264: obra={obra}, formset={formset}")
    
    # Agrupar valores por índice (ahora usa posición 2)
    handler = FormsetSubcampoHandler(request_post)
    valores = handler._agrupar_subcampos_por_indice("fecha_produccion_264_", 2)
    
    print(f"🔥 DEBUG save_fechas_264: valores={valores}")
    
    for index, form in enumerate(formset):
        print(f"🔥 DEBUG save_fechas_264: procesando form {index}, pk={form.instance.pk}")
        
        # 1. Asegurar que el ProduccionPublicacion exista y tenga obra
        if not form.instance.pk:
            parent = form.save(commit=False)
            # CORRECCIÓN: Usar la obra pasada como parámetro
            parent.obra = obra
            print(f"🔥 DEBUG save_fechas_264: guardando parent con obra={obra}")
            parent.save()
            print(f"🔥 DEBUG save_fechas_264: parent guardado con pk={parent.pk}")
        
        # 2. Eliminar fechas existentes para este ProduccionPublicacion
        form.instance.fechas.all().delete()
        
        # 3. Agregar nuevas fechas si hay valores
        if index in valores:
            for valor in valores[index]:
                if valor.strip():  # Solo guardar si no está vacío
                    fecha = Fecha264.objects.create(
                        produccion_publicacion=form.instance,
                        fecha=valor.strip()
                    )
                    print(f"🔥 DEBUG save_fechas_264: fecha creada={fecha.fecha} (pk={fecha.pk})")


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
    "_save_urls_856": _save_urls_856,
    "_save_textos_enlace_856": _save_textos_enlace_856,
    "_save_lugares_264": save_lugares_264,
    "_save_entidades_264": save_entidades_264,
    "_save_fechas_264": save_fechas_264,
    "_save_medios_382": save_medios_382,
    "_save_titulos_490": save_titulos_490,
    "_save_volumenes_490": save_volumenes_490,
}