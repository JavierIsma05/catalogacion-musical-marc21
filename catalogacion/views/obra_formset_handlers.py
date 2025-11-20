"""
Handlers para procesamiento de formsets con subcampos dinámicos en MARC21.
Cada subcampo repetible agregando vía JavaScript se parsea aquí, agrupando
por índice de formset y guardándolo en cascada en la base de datos.

Este archivo es crítico para todos los campos repetibles del sistema.
"""

class FormsetSubcampoHandler:
    """
    Handler genérico para procesar subcampos dinámicos generados por JS.

    Formato esperado de inputs dinámicos:
        prefijo_index_timestamp → valor
        
    Ejemplo:
        subdivision_genero_655_0_93232323 = "Vocal"
        subdivision_genero_655_0_91282111 = "Litúrgica"
    """

    def __init__(self, request_post):
        self.request_post = request_post

    # ============================================================
    # Agrupar subcampos por índice del formset
    # ============================================================
    def _agrupar_subcampos_por_indice(self, prefijo_input, indice_posicion=3):
        """
        Agrupa inputs del formset por su índice.

        Ejemplo:
            subdivision_genero_655_0_123  → index 0
            subdivision_genero_655_1_888  → index 1

        Retorna:
            {0: ["valor1","valor2"], 1:["valorA"]}
        """
        agrupados = {}

        for key, value in self.request_post.items():
            if key.startswith(prefijo_input) and value.strip():
                try:
                    parts = key.split('_')
                    indice = int(parts[indice_posicion])

                    if indice not in agrupados:
                        agrupados[indice] = []

                    agrupados[indice].append(value.strip())

                except (ValueError, IndexError):
                    continue

        return agrupados

    # ============================================================
    # Guardar subcampos simples
    # ============================================================
    def procesar_subcampo_simple(
        self, formset, prefijo_input, modelo_subcampo, campo_fk, campo_valor, indice_posicion=3
    ):
        """
        Procesa un subcampo repetible (solo un valor por fila).

        - Elimina subcampos existentes
        - Crea los nuevos subcampos agrupados por índice

        Ejemplo 650:
            campo_fk    = "materia"
            campo_valor = "subdivision"
        """
        valores = self._agrupar_subcampos_por_indice(prefijo_input, indice_posicion)

        for index, form in enumerate(formset):
            # solo procesamos si el objeto existe en BD
            if not form.instance.pk:
                continue

            if index in valores:
                # eliminar subcampos viejos
                relacionado = getattr(
                    form.instance,
                    modelo_subcampo._meta.get_field(campo_fk).related_query_name()
                )
                relacionado.all().delete()

                # crear nuevos
                for valor in valores[index]:
                    modelo_subcampo.objects.create(
                        **{
                            campo_fk: form.instance,
                            campo_valor: valor
                        }
                    )

# ================================================================
# HANDLERS ESPECÍFICOS PARA CADA CAMPO MARC21
# ================================================================

def save_subdivisiones_650(request_post, formset):
    """Guardar subdivisiones del campo 650 $x"""
    from catalogacion.models import SubdivisionMateria650

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input="subdivision_materia_650_",
        modelo_subcampo=SubdivisionMateria650,
        campo_fk="materia",
        campo_valor="subdivision"
    )

def save_subdivisiones_655(request_post, formset):
    """Guardar subdivisiones del campo 655 $x"""
    from catalogacion.models import SubdivisionGeneral655

    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input="subdivision_genero_655_",
        modelo_subcampo=SubdivisionGeneral655,
        campo_fk="materia655",    # ← ESTE ERA EL ERROR ORIGINAL
        campo_valor="subdivision"
    )

# ================================================================
# OTROS HANDLERS (sin modificaciones importantes)
# ================================================================

def save_numeros_obra_773(request_post, formset):
    from catalogacion.models import NumeroObraRelacionada773
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "numero_enlace_773_", NumeroObraRelacionada773, "enlace_773", "numero")

def save_numeros_obra_774(request_post, formset):
    from catalogacion.models import NumeroObraRelacionada774
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "numero_enlace_774_", NumeroObraRelacionada774, "enlace_774", "numero")

def save_numeros_obra_787(request_post, formset):
    from catalogacion.models import NumeroObra787
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "numero_relacion_787_", NumeroObra787, "relacion", "numero")

def save_estanterias_852(request_post, formset):
    from catalogacion.models import Estanteria852
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "estanteria_ubicacion_852_", Estanteria852, "ubicacion", "estanteria")

def save_urls_856(request_post, formset):
    from catalogacion.models import URL856
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "url_disponible_856_", URL856, "disponible", "url")

def save_textos_enlace_856(request_post, formset):
    from catalogacion.models import TextoEnlace856
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "texto_disponible_856_", TextoEnlace856, "disponible", "texto_enlace")

def save_lugares_264(request_post, formset):
    from catalogacion.models import Lugar264
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "lugar_produccion_264_", Lugar264, "produccion_publicacion", "lugar")

def save_entidades_264(request_post, formset):
    from catalogacion.models import NombreEntidad264
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "entidad_produccion_264_", NombreEntidad264, "produccion_publicacion", "nombre")

def save_fechas_264(request_post, formset):
    from catalogacion.models import Fecha264
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "fecha_produccion_264_", Fecha264, "produccion_publicacion", "fecha")

def save_medios_382(request_post, formset):
    from catalogacion.models import MedioInterpretacion382_a
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "medio_interpretacion_382_", MedioInterpretacion382_a, "medio_interpretacion", "medio")

def save_titulos_490(request_post, formset):
    from catalogacion.models import TituloSerie490
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "titulo_mencion_490_", TituloSerie490, "serie", "titulo_serie")

def save_volumenes_490(request_post, formset):
    from catalogacion.models import VolumenSerie490
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "volumen_mencion_490_", VolumenSerie490, "serie", "volumen")

def save_textos_biograficos_545(request_post, formset):
    from catalogacion.models import TextoBiografico545
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "texto_biografico_545_", TextoBiografico545, "dato_biografico", "texto")

def save_uris_545(request_post, formset):
    from catalogacion.models import URI545
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(formset, "uri_545_", URI545, "dato_biografico", "uri")


# ================================================================
# MAPEADOR DE HANDLERS
# ================================================================

SUBCAMPO_HANDLERS = {
    "_save_subdivisiones_650": save_subdivisiones_650,
    "_save_subdivisiones_655": save_subdivisiones_655,
    "_save_numeros_obra_773": save_numeros_obra_773,
    "_save_numeros_obra_774": save_numeros_obra_774,
    "_save_numeros_obra_787": save_numeros_obra_787,
    "_save_estanterias_852": save_estanterias_852,
    "_save_urls_856": save_urls_856,
    "_save_textos_enlace_856": save_textos_enlace_856,
    "_save_lugares_264": save_lugares_264,
    "_save_entidades_264": save_entidades_264,
    "_save_fechas_264": save_fechas_264,
    "_save_medios_382": save_medios_382,
    "_save_titulos_490": save_titulos_490,
    "_save_volumenes_490": save_volumenes_490,
    "_save_textos_biograficos_545": save_textos_biograficos_545,
    "_save_uris_545": save_uris_545,
}
