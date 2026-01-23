from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from catalogacion.models import ObraGeneral

from django.core.files.storage import default_storage
from django.urls import reverse

from digitalizacion.models import DigitalPage, WorkSegment


class HomePublicoView(TemplateView):
    """Página de inicio pública del catálogo"""

    template_name = "catalogo_publico/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Catálogo Musical MARC21"
        context["total_obras"] = ObraGeneral.objects.activos().count()
        # Últimas obras catalogadas
        context["ultimas_obras"] = ObraGeneral.objects.activos().order_by(
            "-fecha_creacion_sistema"
        )[:6]
        return context


class ListaObrasPublicaView(ListView):
    """Lista pública de obras catalogadas"""

    model = ObraGeneral
    template_name = "catalogo_publico/lista_obras.html"
    context_object_name = "obras"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            ObraGeneral.objects.activos()
            .select_related(
                "compositor",
                "titulo_uniforme",
                "titulo_240",
                "forma_130",
                "forma_240",
                "digital_set",
            )
            .prefetch_related(
                "medios_interpretacion_382__medios",
                "materias_650__subdivisiones",
                "materias_655__subdivisiones",
                "producciones_publicaciones__lugares",
                "producciones_publicaciones__entidades",
                "producciones_publicaciones__fechas",
                "enlaces_documento_fuente_773__titulo",
                "enlaces_documento_fuente_773__encabezamiento_principal",
                "incipits_musicales",
                # 🆕 NUEVO para mostrar 852 y 856
                "ubicaciones_852",
                "ubicaciones_852__estanterias",
                "disponibles_856",
                "disponibles_856__urls_856",
                "disponibles_856__textos_enlace_856",
            )
            .order_by("-fecha_creacion_sistema")
        )

        # Búsqueda por texto
        busqueda = self.request.GET.get("q", "")
        if busqueda:
            queryset = queryset.filter(
                Q(titulo_principal__icontains=busqueda)
                | Q(compositor__apellidos_nombres__icontains=busqueda)
            )

        # Filtro por tipo de obra
        tipo = self.request.GET.get("tipo", "")
        if tipo:
            queryset = queryset.filter(tipo_registro=tipo)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Catálogo de Obras"
        context["busqueda"] = self.request.GET.get("q", "")
        context["tipo_seleccionado"] = self.request.GET.get("tipo", "")
        context["tipos_obra"] = [
            ("d", "Manuscritos"),
            ("c", "Impresos"),
        ]

        obras = context.get("obras")
        obras_list = list(obras) if obras is not None else []
        obra_ids = [o.id for o in obras_list]
        if not obra_ids:
            return context

        # 1) Primer segmento por obra (si existe)
        segments = (
            WorkSegment.objects.filter(obra_id__in=obra_ids)
            .select_related("digital_set")
            .order_by("obra_id", "start_page")
        )
        first_segment_by_obra = {}
        for seg in segments:
            if seg.obra_id not in first_segment_by_obra:
                first_segment_by_obra[seg.obra_id] = seg

        # 2) Decide ds + página + visor_url por obra
        wanted_pairs = []
        wanted_meta = {}  # obra_id -> {ds_id, page, visor_url, pdf_path}
        for o in obras_list:
            seg = first_segment_by_obra.get(o.id)

            if seg:
                ds = seg.digital_set
                page_n = seg.start_page
                visor_url = reverse("digitalizacion:visor_obra", kwargs={"obra_id": o.id})
                pdf_path = getattr(ds, "pdf_path", "") if ds else ""
            else:
                ds = getattr(o, "digital_set", None)
                page_n = 1
                visor_url = reverse("digitalizacion:visor_coleccion", kwargs={"pk": o.id})
                pdf_path = getattr(ds, "pdf_path", "") if ds else ""

            ds_id = ds.id if ds else None
            if ds_id:
                wanted_pairs.append((ds_id, page_n))

            wanted_meta[o.id] = {
                "ds_id": ds_id,
                "page": page_n,
                "visor_url": visor_url,  # dejamos link aunque no haya cover; el template decide
                "pdf_path": pdf_path,
            }

        # 3) Buscar derivative JPG para esas páginas
        from django.db.models import Q
        q = Q()
        for ds_id, page_n in wanted_pairs:
            q |= Q(digital_set_id=ds_id, page_number=page_n)

        dp_map = {}
        if q:
            pages = DigitalPage.objects.filter(q).only("digital_set_id", "page_number", "derivative_path")
            for dp in pages:
                if dp.derivative_path:
                    dp_map[(dp.digital_set_id, dp.page_number)] = dp.derivative_path

        # 4) Inyectar cover_url + visor_url en cada obra
        for o in obras_list:
            meta = wanted_meta.get(o.id, {})
            ds_id = meta.get("ds_id")
            page_n = meta.get("page", 1)

            derivative_path = dp_map.get((ds_id, page_n)) if ds_id else None

            cover_url = None
            cover_kind = None  # "jpg" | "pdf"

            if derivative_path:
                cover_url = default_storage.url(derivative_path)
                cover_kind = "jpg"
            else:
                pdf_path = meta.get("pdf_path") or ""
                if pdf_path:
                    # Nota: esto no es una miniatura real; es fallback funcional
                    cover_url = default_storage.url(pdf_path)
                    cover_kind = "pdf"

            o.cover_url = cover_url
            o.cover_kind = cover_kind
            o.visor_url = meta.get("visor_url")

        return context



class DetalleObraPublicaView(DetailView):
    """Vista pública de detalle de una obra"""

    model = ObraGeneral
    template_name = "catalogo_publico/resumen_obra.html"
    context_object_name = "obra"

    def get_queryset(self):
        return (
            ObraGeneral.objects.activos()
            .select_related(
                "compositor",
                "titulo_uniforme",
                "titulo_240",
                "forma_130",
                "forma_240",
            )
            .prefetch_related(
                "medios_interpretacion_382__medios",
                "materias_650__subdivisiones",
                "materias_655__subdivisiones",
                "producciones_publicaciones__lugares",
                "producciones_publicaciones__entidades",
                "producciones_publicaciones__fechas",
                "enlaces_documento_fuente_773__titulo",
                "enlaces_documento_fuente_773__encabezamiento_principal",
                "incipits_musicales",
                "notas_generales_500",
                # 🆕 NUEVO para mostrar 852 y 856
                "ubicaciones_852",
                "ubicaciones_852__estanterias",
                "disponibles_856",
                "disponibles_856__urls_856",
                "disponibles_856__textos_enlace_856",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = f"Detalle: {self.object}"
        return context


class VistaDetalladaObraView(DetailView):
    """Vista pública detallada completa de una obra"""

    model = ObraGeneral
    template_name = "catalogo_publico/detalle_obra.html"
    context_object_name = "obra"

    def get_queryset(self):
        return (
            ObraGeneral.objects.activos()
            .select_related(
                "compositor",
                "titulo_uniforme",
                "titulo_240",
                "forma_130",
                "forma_240",
                "digital_set",
            )
            .prefetch_related(
                "medios_interpretacion_382__medios",
                "materias_650__subdivisiones",
                "materias_655__subdivisiones",
                "producciones_publicaciones__lugares",
                "producciones_publicaciones__entidades",
                "producciones_publicaciones__fechas",
                "enlaces_documento_fuente_773__titulo",
                "enlaces_documento_fuente_773__encabezamiento_principal",
                "incipits_musicales",
                "notas_generales_500",
                "titulos_alternativos",
                "ediciones",
                "nombres_relacionados_700__persona",
                "nombres_relacionados_700__funciones",
                "nombres_relacionados_700__terminos_asociados",
                "entidades_relacionadas_710__entidad",
                "menciones_serie__titulos",
                "menciones_serie__volumenes",
                "enlaces_unidades_774__encabezamiento_principal",
                "enlaces_unidades_774__titulo",
                "otras_relaciones_787__encabezamiento_principal",
                "contenidos_505",
                "sumarios_520",
                "ubicaciones_852",
                "ubicaciones_852__estanterias",
                "disponibles_856",
                "disponibles_856__urls_856",
                "disponibles_856__textos_enlace_856",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obra = self.object
        context["titulo"] = f"Vista detallada: {obra}"

        # Resolver PDF y start_page:
        seg = (
            WorkSegment.objects.filter(obra=obra)
            .select_related("digital_set")
            .order_by("start_page")
            .first()
        )

        if seg and seg.digital_set:
            ds = seg.digital_set
            start_page = seg.start_page or 1
        else:
            ds = getattr(obra, "digital_set", None)
            start_page = 1

        pdf_url = None
        if ds and getattr(ds, "pdf_path", ""):
            pdf_url = default_storage.url(ds.pdf_path)

        context["pdf_url"] = pdf_url
        context["pdf_start_page"] = start_page

        return context



class FormatoMARC21View(DetailView):
    """Vista pública del formato MARC21 de una obra"""

    model = ObraGeneral
    template_name = "catalogo_publico/formato_marc21.html"
    context_object_name = "obra"

    def get_queryset(self):
        return (
            ObraGeneral.objects.activos()
            .select_related(
                "compositor",
                "titulo_uniforme",
                "titulo_240",
                "forma_130",
                "forma_240",
            )
            .prefetch_related(
                # Bloque 0XX
                "incipits_musicales__urls",  # 031 con subcampo $u
                "codigos_lengua__idiomas",  # 041 con subcampo $a
                "codigos_pais_entidad",  # 044
                # Bloque 1XX
                "funciones_compositor",  # 100 $e
                # Bloque 2XX
                "titulos_alternativos",  # 246
                "ediciones",  # 250
                "producciones_publicaciones__lugares",  # 264 $a
                "producciones_publicaciones__entidades",  # 264 $b
                "producciones_publicaciones__fechas",  # 264 $c
                # Bloque 3XX
                "medios_interpretacion_382__medios",  # 382 $a
                # Bloque 4XX
                "menciones_serie__titulos",  # 490 $a
                "menciones_serie__volumenes",  # 490 $v
                # Bloque 5XX
                "notas_generales_500",  # 500
                "contenidos_505",  # 505
                "sumarios_520",  # 520
                # Bloque 6XX
                "materias_650__subdivisiones",  # 650 con $x
                "materias_655__subdivisiones",  # 655 con $x
                # Bloque 7XX
                "nombres_relacionados_700__persona",
                "nombres_relacionados_700__funciones",
                "nombres_relacionados_700__terminos_asociados",
                "entidades_relacionadas_710__entidad",
                "enlaces_documento_fuente_773__titulo",
                "enlaces_documento_fuente_773__encabezamiento_principal",
                "enlaces_documento_fuente_773__numeros_control",
                "enlaces_unidades_774__encabezamiento_principal",
                "enlaces_unidades_774__titulo",
                "enlaces_unidades_774__numeros_control",
                "otras_relaciones_787__encabezamiento_principal",
                "otras_relaciones_787__numeros_control",
                # Bloque 8XX
                "ubicaciones_852__estanterias",  # 852 con $c
                "disponibles_856__urls_856",  # 856 $u
                "disponibles_856__textos_enlace_856",  # 856 $y
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = f"Formato MARC21: {self.object}"

        # Intentar obtener datos biográficos (OneToOne puede no existir)
        try:
            context["datos_biograficos"] = self.object.datos_biograficos_545
        except:
            context["datos_biograficos"] = None

        return context
