from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from catalogacion.models.obra_general import (
    ObraGeneral,
)
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.views import View
from django.urls import reverse
from .models import DigitalSet, DigitalPage, WorkSegment
from django.views.decorators.http import require_POST
from pypdf import PdfReader

from django.http import JsonResponse

import os
import shutil
from PIL import Image

from catalogacion.models.utils import signatura_para_archivo

# Path(settings.MEDIA_ROOT) es backend/media/


def nombre_carpeta_obra(obra) -> str:
    """
    Genera el nombre de carpeta para una obra.
    Usa la signatura si está completa, sino fallback a obra_{id}.
    """
    return signatura_para_archivo(obra) or f"obra_{obra.id}"


def repo_root_for_obra(obra) -> Path:
    """Retorna la ruta del repositorio para una obra."""
    return Path(settings.MEDIA_ROOT) / "digitalizacion" / nombre_carpeta_obra(obra)


# relative_to(MEDIA_ROOT) produce una ruta "portable" que sirve en cualquier servidor.
def to_media_relpath(path: Path) -> str:
    """Convierte Path absoluto dentro de MEDIA_ROOT a ruta relativa (con /)."""
    rel = path.relative_to(Path(settings.MEDIA_ROOT))
    return str(rel).replace("\\", "/")


def default_inbox_for_obra(obra) -> Path:
    """
    Retorna la ruta del inbox para una obra.
    Usa la signatura si está completa, sino fallback a obra_{id}.
    """
    base = Path(getattr(settings, "DIGITALIZACION_INBOX_BASE", Path(settings.MEDIA_ROOT) / "inbox"))
    return base / nombre_carpeta_obra(obra)


def default_repo_for_obra(obra) -> Path:
    """Retorna la ruta del repositorio para una obra."""
    base = Path(getattr(settings, "DIGITALIZACION_REPO_BASE", Path(settings.MEDIA_ROOT) / "digitalizacion"))
    return base / nombre_carpeta_obra(obra)


class DigitalizacionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        filtro_tipo = self.request.GET.get("tipo", "todos")

        # Base queryset
        qs = ObraGeneral.objects.prefetch_related("digital_set").order_by("-id")

        # Filtrar por tipo
        if filtro_tipo == "colecciones":
            qs = qs.filter(nivel_bibliografico="c")
        elif filtro_tipo == "obras_sueltas":
            # Obras que no son colecciones y no pertenecen a ninguna colección (sin 773)
            qs = qs.exclude(nivel_bibliografico="c").filter(
                enlaces_documento_fuente_773__isnull=True
            )
        # else: "todos" - mostrar todo lo que tiene o puede tener DigitalSet

        if q:
            qs = qs.filter(
                Q(titulo_principal__icontains=q)
                | Q(num_control__icontains=q)
                | Q(centro_catalogador__icontains=q)
                | Q(compositor__apellidos_nombres__icontains=q)
            )

        ctx["q"] = q
        ctx["filtro_tipo"] = filtro_tipo
        ctx["obras"] = qs[:50]
        return ctx


class ObraDigitalizacionHomeView(LoginRequiredMixin, TemplateView):
    """Vista home de digitalización para cualquier obra (colección u obra suelta)"""
    template_name = "digitalizacion/obra_home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obra = get_object_or_404(ObraGeneral, pk=kwargs["pk"])
        ds = DigitalSet.objects.filter(obra=obra).first()

        # Determinar si es colección o obra suelta
        es_coleccion = obra.nivel_bibliografico == "c"

        ctx["obra"] = obra
        ctx["digital_set"] = ds
        ctx["es_coleccion"] = es_coleccion
        return ctx


class ImportarObraView(LoginRequiredMixin, TemplateView):
    """Vista de importación TIFF para cualquier obra (colección u obra suelta)"""
    template_name = "digitalizacion/importar.html"

    def get_obra(self):
        return get_object_or_404(ObraGeneral, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        obra = self.get_obra()
        nombre_carpeta = nombre_carpeta_obra(obra)
        inbox = default_inbox_for_obra(obra)
        repo = default_repo_for_obra(obra)

        digital_set = DigitalSet.objects.filter(obra=obra).first()
        es_coleccion = obra.nivel_bibliografico == "c"

        ctx.update(
            {
                "obra": obra,
                "nombre_carpeta_inbox": nombre_carpeta,
                "inbox_path": str(inbox),
                "repo_path": str(repo),
                "digital_set": digital_set,
                "pages_count": digital_set.pages.count() if digital_set else 0,
                "es_coleccion": es_coleccion,
            }
        )
        return ctx

    def post(self, request, *args, **kwargs):
        """
        POST = ejecutar importación de TIFF.
        Flujo: TIFF → copiar a master/ → generar JPG derivado en iiif/jpg/
        """
        obra = self.get_obra()
        nombre_carpeta = nombre_carpeta_obra(obra)
        inbox = default_inbox_for_obra(obra)
        repo = default_repo_for_obra(obra)
        es_coleccion = obra.nivel_bibliografico == "c"

        if not inbox.exists():
            messages.error(request, f"No existe la carpeta INBOX: {inbox}")
            return redirect("digitalizacion:importar", pk=obra.id)

        # Buscar TIFF en la carpeta INBOX
        tiffs = sorted(
            [
                p
                for p in inbox.iterdir()
                if p.is_file() and p.suffix.lower() in [".tif", ".tiff"]
            ]
        )

        if not tiffs:
            messages.warning(request, "No se encontraron imágenes TIFF en la carpeta INBOX.")
            return redirect("digitalizacion:importar", pk=obra.id)

        # Crear/obtener DigitalSet
        tipo_ds = "COLECCION" if es_coleccion else "OBRA_SUELTA"
        digital_set, _ = DigitalSet.objects.get_or_create(
            obra=obra,
            defaults={"tipo": tipo_ds}
        )
        digital_set.inbox_path = str(inbox)
        digital_set.repository_path = str(repo)

        # Crear directorios
        master_dir = repo / "master"
        iiif_dir = repo / "iiif" / "jpg"
        master_dir.mkdir(parents=True, exist_ok=True)
        iiif_dir.mkdir(parents=True, exist_ok=True)

        created = 0
        for idx, src in enumerate(tiffs, start=1):
            # Nombres de archivo
            base_name = f"{nombre_carpeta}_p{idx:03d}"
            master_name = f"{base_name}.tif"
            deriv_name = f"{base_name}.jpg"

            dst_master = master_dir / master_name
            dst_deriv = iiif_dir / deriv_name

            # 1) Copiar TIFF a master/
            shutil.copy2(src, dst_master)

            # 2) Generar JPG derivado para visor (menor calidad/tamaño)
            deriv_ok = False
            try:
                im = Image.open(dst_master)
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                # Redimensionar si es muy grande (max 2000px en el lado mayor)
                max_size = 2000
                if max(im.size) > max_size:
                    im.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                im.save(dst_deriv, "JPEG", quality=85, optimize=True)
                deriv_ok = True
            except Exception as e:
                messages.warning(request, f"No se pudo generar derivado para p{idx:03d}: {e}")

            # 3) Guardar en BD (rutas relativas a MEDIA_ROOT)
            master_rel = to_media_relpath(dst_master)
            deriv_rel = to_media_relpath(dst_deriv) if deriv_ok else ""

            obj, was_created = DigitalPage.objects.update_or_create(
                digital_set=digital_set,
                page_number=idx,
                defaults={
                    "master_path": master_rel,
                    "derivative_path": deriv_rel,
                },
            )
            if was_created:
                created += 1

        digital_set.total_pages = digital_set.pages.count()
        digital_set.estado = "IMPORTADO"
        digital_set.save()

        messages.success(
            request,
            f"Importación completa. Páginas procesadas: {len(tiffs)}. Nuevas: {created}.",
        )
        return redirect("digitalizacion:importar", pk=obra.id)


class SegmentarObraView(LoginRequiredMixin, TemplateView):
    """Vista de segmentación para colecciones (asignar obras a rangos de páginas)"""
    template_name = "digitalizacion/segmentar.html"

    def get_obra_ds(self):
        # Solo colecciones pueden segmentarse
        obra = get_object_or_404(
            ObraGeneral, pk=self.kwargs["pk"], nivel_bibliografico="c"
        )
        ds = DigitalSet.objects.filter(obra=obra).first()
        return obra, ds

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obra, ds = self.get_obra_ds()
        max_pages = ds.pdf_total_pages if ds and ds.pdf_path and ds.pdf_total_pages else (ds.total_pages if ds else 0)

        ctx["obra"] = obra
        ctx["digital_set"] = ds
        ctx["pages"] = ds.pages.all() if ds else []
        ctx["segments"] = ds.segments.select_related("obra").all() if ds else []
        ctx["max_pages"] = max_pages

        return ctx

    def post(self, request, *args, **kwargs):
        obra_coleccion, ds = self.get_obra_ds()
        if not ds:
            messages.error(
                request, "Primero debes importar el escaneo."
            )
            return redirect("digitalizacion:importar", pk=obra_coleccion.id)

        obra_id = request.POST.get("obra_id")
        start_page = request.POST.get("start_page")
        end_page = request.POST.get("end_page")
        tipo = request.POST.get("tipo", "OBRA")

        if not (obra_id and start_page and end_page):
            messages.error(request, "Faltan datos (obra, inicio, fin).")
            return redirect("digitalizacion:segmentar", pk=obra_coleccion.id)

        try:
            obra_id = int(obra_id)
            start_page = int(start_page)
            end_page = int(end_page)
        except ValueError:
            messages.error(request, "Inicio/fin inválidos.")
            return redirect("digitalizacion:segmentar", pk=obra_coleccion.id)

        if start_page > end_page:
            messages.error(request, "Inicio no puede ser mayor que fin.")
            return redirect("digitalizacion:segmentar", pk=obra_coleccion.id)

        # Si hay PDF cargado, manda el PDF
        total = ds.pdf_total_pages if ds.pdf_path and ds.pdf_total_pages else ds.total_pages
        if start_page < 1 or end_page > total:
            messages.error(request, f"Rango fuera de límites. Total páginas: {total}.")
            return redirect("digitalizacion:segmentar", pk=obra_coleccion.id)

        obra_segmento = get_object_or_404(ObraGeneral, pk=obra_id)
        WorkSegment.objects.create(
            obra=obra_segmento,
            digital_set=ds,
            start_page=start_page,
            end_page=end_page,
            tipo=tipo,
        )

        messages.success(
            request,
            f"Segmento creado: Obra {obra_id} ({start_page}-{end_page}) [{tipo}].",
        )
        return redirect("digitalizacion:segmentar", pk=obra_coleccion.id)


class VisorObraDigitalView(LoginRequiredMixin, TemplateView):
    """Visor del documento digitalizado (para colecciones o obras sueltas)"""
    template_name = "digitalizacion/visor_digital.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obra = get_object_or_404(ObraGeneral, pk=self.kwargs["pk"])
        ds = DigitalSet.objects.filter(obra=obra).first()
        es_coleccion = obra.nivel_bibliografico == "c"

        ctx["obra"] = obra
        ctx["digital_set"] = ds
        ctx["pages"] = ds.pages.all() if ds else []
        ctx["segments"] = ds.segments.select_related("obra").all() if ds and es_coleccion else []
        ctx["es_coleccion"] = es_coleccion
        return ctx


class SubirPdfObraView(LoginRequiredMixin, TemplateView):
    """Vista para subir PDF a cualquier obra (colección u obra suelta)"""
    template_name = "digitalizacion/subir_pdf.html"

    def get_obra_ds(self):
        obra = get_object_or_404(ObraGeneral, pk=self.kwargs["pk"])
        es_coleccion = obra.nivel_bibliografico == "c"
        tipo_ds = "COLECCION" if es_coleccion else "OBRA_SUELTA"

        ds, _ = DigitalSet.objects.get_or_create(
            obra=obra,
            defaults={"tipo": tipo_ds}
        )
        repo = default_repo_for_obra(obra)
        ds.repository_path = ds.repository_path or str(repo)
        ds.save()
        return obra, ds, repo

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obra, ds, repo = self.get_obra_ds()
        ctx["obra"] = obra
        ctx["digital_set"] = ds
        ctx["es_coleccion"] = obra.nivel_bibliografico == "c"
        return ctx

    def post(self, request, *args, **kwargs):
        obra, ds, repo = self.get_obra_ds()

        f = request.FILES.get("pdf")
        if not f:
            messages.error(request, "Debes seleccionar un PDF.")
            return redirect("digitalizacion:subir_pdf", pk=obra.id)

        if not f.name.lower().endswith(".pdf"):
            messages.error(request, "El archivo debe ser PDF.")
            return redirect("digitalizacion:subir_pdf", pk=obra.id)

        # Guardar PDF en access/pdf/ (nueva estructura)
        access_dir = repo / "access" / "pdf"
        access_dir.mkdir(parents=True, exist_ok=True)

        # Nombre del PDF usando signatura (ej: UNL-BLMP-EC-Ms-M000001.pdf)
        nombre_carpeta = nombre_carpeta_obra(obra)
        pdf_name = f"{nombre_carpeta}.pdf"
        dst = access_dir / pdf_name

        with open(dst, "wb+") as out:
            for chunk in f.chunks():
                out.write(chunk)

        ds.pdf_path = to_media_relpath(dst)
        ds.save()

        reader = PdfReader(str(dst))
        ds.pdf_total_pages = len(reader.pages)
        ds.pdf_path = to_media_relpath(dst)
        ds.save()

        # Generar thumbnail de la primera página del PDF
        from digitalizacion.services.thumbnail_service import get_pdf_thumbnail_for_digital_set
        get_pdf_thumbnail_for_digital_set(ds)

        messages.success(request, "PDF cargado correctamente.")
        return redirect("digitalizacion:visor_digital", pk=obra.id)


class VisorObraSegmentoView(LoginRequiredMixin, TemplateView):
    """Visor de una obra (prioriza DigitalSet propio sobre segmentos de colección)"""
    template_name = "digitalizacion/visor_obra.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        obra = get_object_or_404(ObraGeneral, pk=self.kwargs["obra_id"])

        # PRIORIDAD 1: Verificar si la obra tiene su propio DigitalSet
        # Esto tiene prioridad porque si alguien subió un PDF específico para esta obra,
        # ese es el que debe mostrarse (no el de la colección)
        ds_propio = DigitalSet.objects.filter(obra=obra).first()
        if ds_propio:
            # La obra tiene su propio DigitalSet - usarlo
            ctx.update(
                {
                    "obra": obra,
                    "segments": [],
                    "digital_set": ds_propio,
                    "coleccion_padre": None,
                    "pages": ds_propio.pages.all(),
                    "start_page": 1,
                    "end_page": ds_propio.total_pages or ds_propio.pdf_total_pages,
                    "es_obra_suelta": True,
                }
            )
            return ctx

        # PRIORIDAD 2: Buscar segmentos en colecciones
        segments = (
            WorkSegment.objects.filter(obra=obra)
            .select_related("digital_set", "digital_set__obra")
            .order_by("start_page")
        )

        if not segments.exists():
            # No tiene DigitalSet propio ni segmentos
            ctx.update(
                {
                    "obra": obra,
                    "segments": [],
                    "digital_set": None,
                    "coleccion_padre": None,
                    "pages": [],
                    "start_page": None,
                    "es_obra_suelta": False,
                }
            )
            return ctx

        # Obra dentro de una colección - usar segmento
        first_seg = segments.first()
        ds = first_seg.digital_set
        coleccion_padre = ds.obra  # La colección a la que pertenece

        # tomamos solo el primer rango como "inicio"
        start_page = first_seg.start_page
        end_page = first_seg.end_page

        pages = DigitalPage.objects.filter(
            digital_set=ds, page_number__gte=start_page, page_number__lte=end_page
        ).order_by("page_number")

        # Generar PDF segmentado (prioridad: imágenes > PDF de colección)
        segment_pdf_url = None
        segment_total_pages = None
        from digitalizacion.services.pdf_service import get_segment_pdf
        segment_pdf_path = get_segment_pdf(first_seg)
        if segment_pdf_path:
            from django.core.files.storage import default_storage
            segment_pdf_url = default_storage.url(segment_pdf_path)
            segment_total_pages = end_page - start_page + 1

        ctx.update(
            {
                "obra": obra,
                "segments": segments,
                "digital_set": ds,
                "coleccion_padre": coleccion_padre,
                "pages": pages,
                "start_page": start_page,
                "end_page": end_page,
                "es_obra_suelta": False,
                "segment_pdf_url": segment_pdf_url,
                "segment_total_pages": segment_total_pages,
            }
        )
        return ctx


def api_buscar_obras(request):
    q = (request.GET.get("q") or "").strip()
    obra_id = request.GET.get("obra_id")  # ID de la colección

    if len(q) < 2:
        return JsonResponse({"results": []})

    # Normalizar obra_id
    try:
        obra_id = int(obra_id) if obra_id else None
    except ValueError:
        obra_id = None

    qs = ObraGeneral.objects.exclude(nivel_bibliografico="c").filter(
        Q(num_control__icontains=q)
        | Q(centro_catalogador__icontains=q)
        | Q(titulo_principal__icontains=q)
        | Q(compositor__apellidos_nombres__icontains=q)
    )

    # Excluir obras ya segmentadas en esta colección (si hay DS)
    if obra_id:
        ds = DigitalSet.objects.filter(obra_id=obra_id).first()
        if ds:
            segmented_ids = WorkSegment.objects.filter(digital_set=ds).values_list(
                "obra_id", flat=True
            )
            qs = qs.exclude(id__in=segmented_ids)

    qs = qs.order_by("-id")[:20]

    results = [
        {
            "id": o.id,
            "num_control": o.num_control,
            "titulo": o.titulo_principal,
            "signatura": o.signatura_publica_display,
            "label": f"{o.signatura_publica_display} — {o.titulo_principal} - {o.autor_publico_principal}",

        }
        for o in qs
    ]

    return JsonResponse({"results": results})


@require_POST
def eliminar_segmento(request, segment_id):
    seg = get_object_or_404(WorkSegment, pk=segment_id)
    obra_id = seg.digital_set.obra_id
    seg.delete()
    messages.success(request, "Segmento eliminado.")
    return redirect("digitalizacion:segmentar", pk=obra_id)


class EliminarPdfObraView(LoginRequiredMixin, View):
    """Elimina solo el PDF de una obra/colección, manteniendo TIFF/JPG"""

    def post(self, request, pk):
        obra = get_object_or_404(ObraGeneral, pk=pk)
        ds = DigitalSet.objects.filter(obra=obra).first()

        if ds and ds.pdf_path:
            # Eliminar archivo físico
            pdf_file = Path(settings.MEDIA_ROOT) / ds.pdf_path
            if pdf_file.exists():
                pdf_file.unlink()

            # Limpiar campos en BD
            ds.pdf_path = ""
            ds.pdf_total_pages = 0
            ds.save()
            messages.success(request, "PDF eliminado correctamente.")
        else:
            messages.warning(request, "No hay PDF para eliminar.")

        return redirect("digitalizacion:obra_home", pk=pk)


class EliminarDigitalSetView(LoginRequiredMixin, View):
    """Elimina todo el DigitalSet (PDF + TIFF + JPG + registros)"""

    def post(self, request, pk):
        obra = get_object_or_404(ObraGeneral, pk=pk)
        ds = DigitalSet.objects.filter(obra=obra).first()

        if not ds:
            messages.warning(request, "No hay digitalización para eliminar.")
            return redirect("digitalizacion:obra_home", pk=pk)

        # Verificar que no haya segmentos que dependan de este DigitalSet
        if ds.segments.exists():
            messages.error(
                request,
                "No se puede eliminar: hay segmentos asignados a esta colección. "
                "Elimina los segmentos primero."
            )
            return redirect("digitalizacion:obra_home", pk=pk)

        # Eliminar carpeta - usar repository_path guardado si existe, sino calcular
        if ds.repository_path:
            repo_dir = Path(ds.repository_path)
        else:
            repo_dir = repo_root_for_obra(obra)

        if repo_dir.exists():
            shutil.rmtree(repo_dir)

        # Eliminar DigitalSet (CASCADE elimina DigitalPages automáticamente)
        ds.delete()
        messages.success(request, "Digitalización eliminada completamente.")

        return redirect("digitalizacion:obra_home", pk=pk)
