"""Comando para probar el formulario completo de creacion de obras."""
import itertools
from urllib.parse import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client, override_settings
from django.urls import reverse

from catalogacion.models import (
    AutoridadEntidad,
    AutoridadFormaMusical,
    AutoridadMateria,
    AutoridadPersona,
    AutoridadTituloUniforme,
    ObraGeneral,
)
from catalogacion.views.obra_config import TIPO_OBRA_CONFIG, get_campos_visibles


class SampleAuthorityFactory:
    """Crea o reutiliza autoridades minimas para poblar los formularios."""

    def build(self):
        compositor, _ = AutoridadPersona.objects.get_or_create(
            apellidos_nombres="Test, Composer",
            defaults={"coordenadas_biograficas": "1900-1980"},
        )

        personas = [compositor]
        for nombre in [
            "Perez, Ana",
            "Lopez, Marta",
            "Gonzalez, Luis",
            "Ramirez, Sofia",
        ]:
            persona, _ = AutoridadPersona.objects.get_or_create(
                apellidos_nombres=nombre,
                defaults={"coordenadas_biograficas": "1890-1970"},
            )
            personas.append(persona)

        titulos = []
        for titulo in ["Sinfonia test", "Concierto test", "Suite test"]:
            titulo_uniforme, _ = AutoridadTituloUniforme.objects.get_or_create(titulo=titulo)
            titulos.append(titulo_uniforme)

        formas = []
        for forma in ["Sinfonia", "Concierto", "Pasillo", "Vals"]:
            forma_obj, _ = AutoridadFormaMusical.objects.get_or_create(forma=forma)
            formas.append(forma_obj)

        materias = []
        for termino in ["Musica andina", "Musica barroca", "Musica colonial"]:
            materia, _ = AutoridadMateria.objects.get_or_create(termino=termino)
            materias.append(materia)

        entidades = []
        for nombre in ["Conservatorio Nacional", "Archivo General", "Biblioteca Central"]:
            entidad, _ = AutoridadEntidad.objects.get_or_create(nombre=nombre)
            entidades.append(entidad)

        return {
            "compositor": compositor,
            "personas": personas,
            "titulos": titulos,
            "formas": formas,
            "materias": materias,
            "entidades": entidades,
        }


class CrearObraPayloadBuilder:
    """Genera el diccionario POST que simula el formulario completo."""

    def __init__(self, tipo_obra, sample_data):
        if tipo_obra not in TIPO_OBRA_CONFIG:
            raise CommandError(f"Tipo de obra desconocido: {tipo_obra}")
        self.tipo = tipo_obra
        self.sample = sample_data
        self.config = TIPO_OBRA_CONFIG[tipo_obra]
        campos = get_campos_visibles(tipo_obra)
        self.formsets_visibles = campos.get("formsets_visibles", [])
        self._seq = itertools.count(1)
        self._formset_builders = {
            "incipits_musicales": self._build_incipits,
            "codigos_lengua": self._build_codigos_lengua,
            "codigos_pais": self._build_codigos_pais,
            "funciones_compositor": self._build_funciones_compositor,
            "titulos_alternativos": self._build_titulos_alternativos,
            "ediciones": self._build_ediciones,
            "produccion_publicacion": self._build_produccion_publicacion,
            "medios_interpretacion": self._build_medios_interpretacion,
            "menciones_serie_490": self._build_menciones_serie,
            "notas_generales": self._build_notas_generales,
            "contenidos": self._build_contenidos,
            "sumarios": self._build_sumarios,
            "datos_biograficos": self._build_datos_biograficos,
            "materias_650": self._build_materias_650,
            "materias_genero_655": self._build_materias_655,
            "nombres_relacionados_700": self._build_nombres_relacionados,
            "entidades_relacionadas_710": self._build_entidades_relacionadas,
            "enlaces_documento_fuente_773": self._build_enlaces_773,
            "enlaces_unidad_constituyente_774": self._build_enlaces_774,
            "otras_relaciones_787": self._build_enlaces_787,
            "ubicaciones_852": self._build_ubicaciones_852,
            "disponibles_856": self._build_disponibles_856,
        }

    def build(self):
        data = self._build_main_form()
        for name in self.formsets_visibles:
            builder = self._formset_builders.get(name)
            if builder:
                data.update(builder())
        return data

    def _build_main_form(self):
        impresos = self.config["tipo_registro"] == "c"
        campos = {
            "tipo_registro": self.config["tipo_registro"],
            "nivel_bibliografico": self.config["nivel_bibliografico"],
            "centro_catalogador": "UNL",
            "isbn": "9781234567897" if impresos else "",
            "ismn": "9790000123456" if impresos else "",
            "tipo_numero_028": "0",
            "control_nota_028": "1",
            "numero_editor": "ED-2025-001",
            "compositor": str(self.sample["compositor"].pk),
            "compositor_texto": "",
            "compositor_coordenadas": "1900-1980",
            "termino_asociado": "Titulo nobiliario",
            "autoria": "certificada",
            "titulo_uniforme": str(self.sample["titulos"][0].pk),
            "titulo_uniforme_texto": "",
            "forma_130": str(self.sample["formas"][0].pk),
            "forma_130_texto": "",
            "medio_interpretacion_130": "piano",
            "numero_parte_130": "1",
            "nombre_parte_130": "Introduccion",
            "arreglo_130": "arreglo",
            "tonalidad_130": "Do mayor",
            "titulo_240": str(self.sample["titulos"][1].pk),
            "titulo_240_texto": "",
            "forma_240": str(self.sample["formas"][1].pk),
            "forma_240_texto": "",
            "medio_interpretacion_240": "piano con acompa\u00f1amiento",
            "numero_parte_240": "2",
            "nombre_parte_240": "Finale",
            "arreglo_240": "arreglo",
            "tonalidad_240": "Sol menor",
            "titulo_principal": f"Obra de prueba {self.tipo}",
            "subtitulo": "Subtitulo de prueba",
            "mencion_responsabilidad": "Autor Ficticio",
            "extension": "123 paginas",
            "otras_caracteristicas": "ilustraciones",
            "dimension": "30 cm",
            "material_acompanante": "1 folleto",
            "ms_imp": "impreso" if impresos else "manuscrito",
            "formato": "partitura",
            "numero_obra": "Op. 10",
            "opus": "Opus 10",
            "tonalidad_384": "La menor",
        }
        return campos

    @staticmethod
    def _formset(prefix, entries):
        data = {
            f"{prefix}-TOTAL_FORMS": str(len(entries)),
            f"{prefix}-INITIAL_FORMS": "0",
            f"{prefix}-MIN_NUM_FORMS": "0",
            f"{prefix}-MAX_NUM_FORMS": "1000",
        }
        for index, fields in enumerate(entries):
            data[f"{prefix}-{index}-id"] = ""
            data[f"{prefix}-{index}-DELETE"] = ""
            for field_name, value in fields.items():
                data[f"{prefix}-{index}-{field_name}"] = "" if value is None else str(value)
        return data

    def _subfields(self, prefix, values_by_form):
        data = {}
        for index, values in enumerate(values_by_form):
            for value in values:
                suffix = next(self._seq)
                data[f"{prefix}{index}_{suffix}"] = value
        return data

    def _build_incipits(self):
        entries = [
            {
                "numero_obra": 1,
                "numero_movimiento": 1,
                "numero_pasaje": 1,
                "titulo_encabezamiento": "Allegro",
                "personaje": "Solista",
                "clave": "G-2",
                "voz_instrumento": "Violin",
                "armadura": "xFC",
                "tiempo": "4/4",
                "notacion_musical": "c4 e4 g4 c5",
            },
            {
                "numero_obra": 2,
                "numero_movimiento": 1,
                "numero_pasaje": 2,
                "titulo_encabezamiento": "Andante",
                "personaje": "Coro",
                "clave": "F-4",
                "voz_instrumento": "Cello",
                "armadura": "bBE",
                "tiempo": "3/4",
                "notacion_musical": "g3 bb3 d4",
            },
        ]
        return self._formset("incipits", entries)

    def _build_codigos_lengua(self):
        entries = [
            {"indicacion_traduccion": "1", "fuente_codigo": "#"},
            {"indicacion_traduccion": "0", "fuente_codigo": "7"},
        ]
        return self._formset("lenguas", entries)

    def _build_codigos_pais(self):
        entries = [
            {"codigo_pais": "ec"},
            {"codigo_pais": "ar"},
        ]
        return self._formset("paises", entries)

    def _build_funciones_compositor(self):
        entries = [
            {"funcion": "compositor"},
            {"funcion": "arreglista"},
        ]
        return self._formset("funciones", entries)

    def _build_titulos_alternativos(self):
        entries = [
            {
                "titulo": "Titulo alternativo A",
                "subtitulo": "Parte 1",
                "texto_visualizacion": "En portada",
            },
            {
                "titulo": "Titulo alternativo B",
                "subtitulo": "Parte 2",
                "texto_visualizacion": "En lomo",
            },
        ]
        return self._formset("titulos_alt", entries)

    def _build_ediciones(self):
        entries = [
            {"edicion": "Primera edicion"},
            {"edicion": "Segunda edicion revisada"},
        ]
        return self._formset("ediciones", entries)

    def _build_produccion_publicacion(self):
        entries = [
            {"funcion": "0"},
            {"funcion": "1"},
        ]
        data = self._formset("produccion", entries)
        data.update(
            self._subfields(
                "lugar_produccion_264_",
                [["Quito", "Guayaquil"], ["Bogota", "Lima"]],
            )
        )
        data.update(
            self._subfields(
                "entidad_produccion_264_",
                [["Editorial Uno", "Editorial Dos"], ["Imprenta Uno", "Imprenta Dos"]],
            )
        )
        data.update(
            self._subfields(
                "fecha_produccion_264_",
                [["2020", "2021"], ["2022", "2023"]],
            )
        )
        return data

    def _build_medios_interpretacion(self):
        entries = [
            {"solista": "Soprano"},
            {"solista": "Baritono"},
        ]
        data = self._formset("medios_382", entries)
        data.update(
            self._subfields(
                "medio_interpretacion_382_",
                [["piano", "dos pianos"], ["piano a cuatro manos", "piano"]],
            )
        )
        return data

    def _build_menciones_serie(self):
        entries = [{}, {}]
        data = self._formset("menciones_490", entries)
        data.update(
            self._subfields(
                "titulo_mencion_490_",
                [["Serie Andina", "Serie Clasica"], ["Coleccion Uno", "Coleccion Dos"]],
            )
        )
        data.update(
            self._subfields(
                "volumen_mencion_490_",
                [["v.1", "v.2"], ["v.3", "v.4"]],
            )
        )
        return data

    def _build_notas_generales(self):
        entries = [
            {"nota_general": "Nota general A"},
            {"nota_general": "Nota general B"},
        ]
        return self._formset("notas_500", entries)

    def _build_contenidos(self):
        entries = [
            {"contenido": "Movimiento I; Movimiento II"},
            {"contenido": "Pieza A; Pieza B"},
        ]
        return self._formset("contenidos_505", entries)

    def _build_sumarios(self):
        entries = [
            {"sumario": "Resumen detallado A"},
            {"sumario": "Resumen detallado B"},
        ]
        return self._formset("sumarios_520", entries)

    def _build_datos_biograficos(self):
        entries = [
            {
                "texto_biografico": "Datos biograficos del autor",
                "uri": "https://example.com/autor",
            }
        ]
        return self._formset("biograficos_545", entries)

    def _build_materias_650(self):
        entries = [
            {"materia": str(self.sample["materias"][0].pk)},
            {"materia": str(self.sample["materias"][1].pk)},
        ]
        data = self._formset("materias_650", entries)
        data.update(
            self._subfields(
                "subdivision_materia_650_",
                [["Historia", "Critica"], ["Interpretacion", "Catalogos"]],
            )
        )
        return data

    def _build_materias_655(self):
        entries = [
            {
                "materia": str(self.sample["formas"][2].pk),
                "materia_texto": self.sample["formas"][2].forma,
            },
            {
                "materia": str(self.sample["formas"][3].pk),
                "materia_texto": self.sample["formas"][3].forma,
            },
        ]
        data = self._formset("generos_655", entries)
        data.update(
            self._subfields(
                "subdivision_genero_655_",
                [["Partituras", "Manuscritos"], ["Fuentes", "Temas"]],
            )
        )
        return data

    def _build_nombres_relacionados(self):
        entries = [
            {
                "persona": str(self.sample["personas"][1].pk),
                "persona_texto": "",
                "persona_coordenadas": "",
                "coordenadas_biograficas": "1901-1975",
                "relacion": "Profesor",
                "autoria": "atribuida",
                "titulo_obra": "Obra relacionada A",
            },
            {
                "persona": str(self.sample["personas"][2].pk),
                "persona_texto": self.sample["personas"][2].apellidos_nombres,
                "persona_coordenadas": "1880-1940",
                "coordenadas_biograficas": "1880-1940",
                "relacion": "Disciple",
                "autoria": "erronea",
                "titulo_obra": "Obra relacionada B",
            },
        ]
        return self._formset("nombres_700", entries)

    def _build_entidades_relacionadas(self):
        entries = [
            {
                "entidad": str(self.sample["entidades"][0].pk),
                "funcion": "editor",
            },
            {
                "entidad": str(self.sample["entidades"][1].pk),
                "funcion": "patrocinante",
            },
        ]
        return self._formset("entidades_710", entries)

    def _build_enlaces_773(self):
        entries = [
            {

                "encabezamiento_principal": str(self.sample["personas"][2].pk),
                "encabezamiento_principal_texto": "",
                "titulo": "Documento fuente A",
            },
            {

                "encabezamiento_principal": str(self.sample["personas"][3].pk),
                "encabezamiento_principal_texto": self.sample["personas"][3].apellidos_nombres,
                "titulo": "Documento fuente B",
            },
        ]
        return self._formset("enlaces_773", entries)

    def _build_enlaces_774(self):
        entries = [
            {
                "encabezamiento_principal": str(self.sample["personas"][3].pk),
                "encabezamiento_principal_texto": "",
                "titulo": "Unidad constituyente A",
            },
            {

                "encabezamiento_principal": str(self.sample["personas"][4].pk),
                "encabezamiento_principal_texto": self.sample["personas"][4].apellidos_nombres,
                "titulo": "Unidad constituyente B",
            },
        ]
        return self._formset("enlaces_774", entries)

    def _build_enlaces_787(self):
        entries = [
            {
                "encabezamiento_principal": str(self.sample["personas"][4].pk),
                "encabezamiento_principal_texto": "",
                "titulo": "Relacionada A",
            },
            {
                "encabezamiento_principal": str(self.sample["personas"][0].pk),
                "encabezamiento_principal_texto": self.sample["personas"][0].apellidos_nombres,
                "titulo": "Relacionada B",
            },
        ]
        return self._formset("relaciones_787", entries)

    def _build_ubicaciones_852(self):
        entries = [
            {
                "codigo_o_nombre ": "EC-UNL",
                "signatura_original": "Caja 1-23",
            },
            {
                "codigo_o_nombre ": "Archivo José Pérez",
                "signatura_original": "Caja 2-11",
            },
        ]
        data = self._formset("ubicaciones_852", entries)
        data.update(
            self._subfields(
                "estanteria_ubicacion_852_",
                [["Estante A", "Estante B"], ["Estante C", "Estante D"]],
            )
        )
        return data

    def _build_disponibles_856(self):
        entries = [{}, {}]
        data = self._formset("disponibles_856", entries)
        data.update(
            self._subfields(
                "url_disponible_856_",
                [
                    ["https://example.com/partitura.pdf", "https://example.com/audio.mp3"],
                    ["https://example.com/video.mp4", "https://example.com/info"],
                ],
            )
        )
        data.update(
            self._subfields(
                "texto_disponible_856_",
                [["PDF", "Audio"], ["Video", "Informacion"]],
            )
        )
        return data


class Command(BaseCommand):
    help = (
        "Envia un POST masivo al formulario de crear obra para cada tipo y verifica que todos los"
        " formsets se guarden sin errores."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--tipo",
            choices=sorted(TIPO_OBRA_CONFIG.keys()),
            help="Clave del tipo de obra a probar (por defecto se prueban todos)",
        )
        parser.add_argument(
            "--keep-records",
            action="store_true",
            help="Si se indica, no elimina las obras creadas durante la prueba",
        )

    def handle(self, *args, **options):
        tipos = [options["tipo"]] if options.get("tipo") else list(TIPO_OBRA_CONFIG.keys())
        sample_data = SampleAuthorityFactory().build()
        resultados = []

        allowed_hosts = list(getattr(settings, "ALLOWED_HOSTS", []))
        if "testserver" not in allowed_hosts:
            allowed_hosts.append("testserver")

        with override_settings(ALLOWED_HOSTS=allowed_hosts):
            for tipo in tipos:
                builder = CrearObraPayloadBuilder(tipo, sample_data)
                payload = builder.build()
                client = Client()
                url = reverse("catalogacion:crear_obra", kwargs={"tipo": tipo})
                response = client.post(url, data=payload, follow=False)

                if response.status_code == 302:
                    location = response.headers.get("Location") or response.get("Location")
                    pk = self._extraer_pk(location)
                    resultados.append({"tipo": tipo, "ok": True, "pk": pk})
                    self.stdout.write(self.style.SUCCESS(f"[OK] {tipo}: guardado (pk={pk})"))
                    if pk and not options.get("keep_records"):
                        ObraGeneral.objects.filter(pk=pk).delete()
                    continue

                errores = self._extraer_errores(response, builder.formsets_visibles)
                resultados.append({"tipo": tipo, "ok": False, "errores": errores})
                self.stdout.write(self.style.ERROR(f"[FAIL] {tipo}: fallo"))
                if errores:
                    for origen, detalle in errores.items():
                        self.stdout.write(f"    - {origen}: {detalle}")

        if not all(r["ok"] for r in resultados):
            raise CommandError("Alguno de los tipos de obra no se pudo guardar. Consulte los detalles arriba.")

        self.stdout.write(self.style.SUCCESS("Todas las variantes de obra se guardaron correctamente."))

    @staticmethod
    def _extraer_pk(location):
        if not location:
            return None
        path = urlparse(location).path
        partes = [segmento for segmento in path.split("/") if segmento]
        if not partes:
            return None
        try:
            return int(partes[-1])
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extraer_errores(response, formsets_visibles):
        ctx = None
        if hasattr(response, "context") and response.context:
            ctx = response.context
            if isinstance(ctx, list):
                ctx = ctx[0]
        if not ctx and hasattr(response, "context_data"):
            ctx = response.context_data
        if not ctx:
            return {"response": f"Estado {response.status_code}"}

        errores = {}
        form = ctx.get("form")
        if form and form.errors:
            errores["form"] = form.errors.get_json_data()

        for nombre in formsets_visibles:
            formset = ctx.get(nombre)
            if formset and formset.errors:
                errores[nombre] = formset.errors

        return errores or {"response": f"Estado {response.status_code}"}