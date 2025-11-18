"""
Handlers para procesamiento de formsets con subcampos dinámicos.
Estos handlers procesan inputs generados por JavaScript que siguen el patrón:
{subcampo}_{contenedor}_{index}_{timestamp}
"""


class FormsetSubcampoHandler:
    """
    Handler genérico para procesar subcampos dinámicos de formsets.
    Los subcampos son campos relacionados que se crean dinámicamente con JavaScript.
    """
    
    def __init__(self, request_post):
        """
        Args:
            request_post: request.POST con los datos del formulario
        """
        self.request_post = request_post
    
    def _agrupar_subcampos_por_indice(self, prefijo_input, indice_posicion=3):
        """
        Agrupa valores de inputs por su índice de contenedor.
        
        Args:
            prefijo_input: Prefijo del input (ej: 'numero_enlace_773_')
            indice_posicion: Posición del índice en el nombre separado por '_'
        
        Returns:
            dict: {indice_contenedor: [valores]}
        
        Ejemplo:
            Input: numero_enlace_773_0_1234567890 = "Valor1"
                   numero_enlace_773_0_9876543210 = "Valor2"
                   numero_enlace_773_1_1111111111 = "Valor3"
            Output: {0: ["Valor1", "Valor2"], 1: ["Valor3"]}
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
                except (IndexError, ValueError):
                    continue
        
        return agrupados
    
    def procesar_subcampo_simple(self, formset, prefijo_input, modelo_subcampo, 
                                  campo_fk, campo_valor, indice_posicion=3):
        """
        Procesa subcampos simples (un solo campo por relación).
        
        Args:
            formset: Formset del contenedor
            prefijo_input: Prefijo del nombre del input
            modelo_subcampo: Clase del modelo de subcampo
            campo_fk: Nombre del campo ForeignKey en el modelo de subcampo
            campo_valor: Nombre del campo de valor en el modelo de subcampo
            indice_posicion: Posición del índice en el nombre del input
        
        Ejemplo:
            procesar_subcampo_simple(
                formset=enlace_773_formset,
                prefijo_input='numero_enlace_773_',
                modelo_subcampo=NumeroObraRelacionada773,
                campo_fk='enlace_773',
                campo_valor='numero'
            )
        """
        valores_agrupados = self._agrupar_subcampos_por_indice(
            prefijo_input, indice_posicion
        )
        
        for index, form in enumerate(formset):
            if form.instance.pk and index in valores_agrupados:
                # Eliminar subcampos existentes
                relacionados = getattr(form.instance, 
                                      modelo_subcampo._meta.get_field(campo_fk).related_query_name())
                relacionados.all().delete()
                
                # Crear nuevos subcampos
                for valor in valores_agrupados[index]:
                    kwargs = {
                        campo_fk: form.instance,
                        campo_valor: valor
                    }
                    modelo_subcampo.objects.create(**kwargs)


# Handlers específicos por campo MARC21

def save_numeros_obra_773(request_post, formset):
    """Procesa números de obra relacionada del campo 773."""
    from catalogacion.models import NumeroObraRelacionada773
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='numero_enlace_773_',
        modelo_subcampo=NumeroObraRelacionada773,
        campo_fk='enlace_773',
        campo_valor='numero'
    )


def save_numeros_obra_774(request_post, formset):
    """Procesa números de obra relacionada del campo 774."""
    from catalogacion.models import NumeroObraRelacionada774
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='numero_enlace_774_',
        modelo_subcampo=NumeroObraRelacionada774,
        campo_fk='enlace_774',
        campo_valor='numero'
    )


def save_numeros_obra_787(request_post, formset):
    """Procesa números de obra de otras relaciones del campo 787."""
    from catalogacion.models import NumeroObra787
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='numero_relacion_787_',
        modelo_subcampo=NumeroObra787,
        campo_fk='relacion',
        campo_valor='numero'
    )


def save_estanterias_852(request_post, formset):
    """Procesa estanterías del campo 852."""
    from catalogacion.models import Estanteria852
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='estanteria_ubicacion_852_',
        modelo_subcampo=Estanteria852,
        campo_fk='ubicacion',
        campo_valor='estanteria'
    )


def save_urls_856(request_post, formset):
    """Procesa URLs del campo 856."""
    from catalogacion.models import URL856
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='url_disponible_856_',
        modelo_subcampo=URL856,
        campo_fk='disponible',
        campo_valor='url'
    )


def save_textos_enlace_856(request_post, formset):
    """Procesa textos de enlace del campo 856."""
    from catalogacion.models import TextoEnlace856
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='texto_disponible_856_',
        modelo_subcampo=TextoEnlace856,
        campo_fk='disponible',
        campo_valor='texto_enlace'
    )


def save_lugares_264(request_post, formset):
    """Procesa lugares ($a) del campo 264."""
    from catalogacion.models import Lugar264
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='lugar_produccion_264_',
        modelo_subcampo=Lugar264,
        campo_fk='produccion_publicacion',
        campo_valor='lugar'
    )


def save_entidades_264(request_post, formset):
    """Procesa entidades ($b) del campo 264."""
    from catalogacion.models import NombreEntidad264
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='entidad_produccion_264_',
        modelo_subcampo=NombreEntidad264,
        campo_fk='produccion_publicacion',
        campo_valor='nombre'
    )


def save_fechas_264(request_post, formset):
    """Procesa fechas ($c) del campo 264."""
    from catalogacion.models import Fecha264
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='fecha_produccion_264_',
        modelo_subcampo=Fecha264,
        campo_fk='produccion_publicacion',
        campo_valor='fecha'
    )


def save_medios_382(request_post, formset):
    """Procesa medios ($a) del campo 382."""
    from catalogacion.models import MedioInterpretacion382_a
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='medio_interpretacion_382_',
        modelo_subcampo=MedioInterpretacion382_a,
        campo_fk='medio_interpretacion',
        campo_valor='medio'
    )


def save_titulos_490(request_post, formset):
    """Procesa títulos de serie del campo 490."""
    from catalogacion.models import TituloSerie490
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='titulo_mencion_490_',
        modelo_subcampo=TituloSerie490,
        campo_fk='serie',
        campo_valor='titulo_serie'
    )


def save_volumenes_490(request_post, formset):
    """Procesa volúmenes de serie del campo 490."""
    from catalogacion.models import VolumenSerie490
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='volumen_mencion_490_',
        modelo_subcampo=VolumenSerie490,
        campo_fk='serie',
        campo_valor='volumen'
    )


def save_textos_biograficos_545(request_post, formset):
    """Procesa textos biográficos del campo 545."""
    from catalogacion.models import TextoBiografico545
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='texto_biografico_545_',
        modelo_subcampo=TextoBiografico545,
        campo_fk='dato_biografico',
        campo_valor='texto'
    )


def save_uris_545(request_post, formset):
    """Procesa URIs del campo 545."""
    from catalogacion.models import URI545
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='uri_545_',
        modelo_subcampo=URI545,
        campo_fk='dato_biografico',
        campo_valor='uri'
    )


def save_subdivisiones_650(request_post, formset):
    """Procesa subdivisiones de materia del campo 650."""
    from catalogacion.models import SubdivisionMateria650
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='subdivision_materia_650_',
        modelo_subcampo=SubdivisionMateria650,
        campo_fk='materia',
        campo_valor='subdivision'
    )


def save_subdivisiones_655(request_post, formset):
    """Procesa subdivisiones de género del campo 655."""
    from catalogacion.models import SubdivisionGeneral655
    
    handler = FormsetSubcampoHandler(request_post)
    handler.procesar_subcampo_simple(
        formset=formset,
        prefijo_input='subdivision_genero_655_',
        modelo_subcampo=SubdivisionGeneral655,
        campo_fk='genero',
        campo_valor='subdivision'
    )


# Mapeo de handlers para fácil acceso
SUBCAMPO_HANDLERS = {
    '_save_numeros_obra_773': save_numeros_obra_773,
    '_save_numeros_obra_774': save_numeros_obra_774,
    '_save_numeros_obra_787': save_numeros_obra_787,
    '_save_estanterias_852': save_estanterias_852,
    '_save_urls_856': save_urls_856,
    '_save_textos_enlace_856': save_textos_enlace_856,
    '_save_lugares_264': save_lugares_264,
    '_save_entidades_264': save_entidades_264,
    '_save_fechas_264': save_fechas_264,
    '_save_medios_382': save_medios_382,
    '_save_titulos_490': save_titulos_490,
    '_save_volumenes_490': save_volumenes_490,
    '_save_textos_biograficos_545': save_textos_biograficos_545,
    '_save_uris_545': save_uris_545,
    '_save_subdivisiones_650': save_subdivisiones_650,
    '_save_subdivisiones_655': save_subdivisiones_655,
}
