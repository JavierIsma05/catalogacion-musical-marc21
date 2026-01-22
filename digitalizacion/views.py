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

# Path(settings.MEDIA_ROOT) es backend/media/

def repo_root_for_collection(coleccion_id: int) -> Path:
    return Path(settings.MEDIA_ROOT) / "digitalizacion" / f"coleccion_{coleccion_id}"


# relative_to(MEDIA_ROOT) produce una ruta “portable” que sirve en cualquier servidor.
def to_media_relpath(path: Path) -> str:
    """Convierte Path absoluto dentro de MEDIA_ROOT a ruta relativa (con /)."""
    rel = path.relative_to(Path(settings.MEDIA_ROOT))
    return str(rel).replace("\\", "/")


def default_inbox_for_collection(coleccion_id: int) -> Path:
    """
    MVP: carpeta INBOX local.
    Puedes mover esto a settings luego.
    """
    base = Path(getattr(settings, "DIGITALIZACION_INBOX_BASE", Path(settings.MEDIA_ROOT) / "inbox"))
    return base / f"coleccion_{coleccion_id}"


def default_repo_for_collection(coleccion_id: int) -> Path:
    base = Path(getattr(settings, "DIGITALIZACION_REPO_BASE", Path(settings.MEDIA_ROOT) / "digitalizacion"))
    return base / f"coleccion_{coleccion_id}"

class DigitalizacionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()

        qs = ObraGeneral.objects.filter(nivel_bibliografico="c").prefetch_related("digital_set").order_by("-id")
        if q:
            # Ajusta campos según tu modelo real (titulo, compositor, num_control, etc.)
            qs = qs.filter(
                Q(titulo_principal__icontains=q)
                | Q(num_control__icontains=q)
                | Q(centro_catalogador__icontains=q)
                | Q(compositor__apellidos_nombres__icontains=q)
            )

        ctx["q"] = q
        ctx["colecciones"] = qs[:50]
        return ctx


class ColeccionDigitalizacionHomeView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/coleccion_home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        coleccion = ObraGeneral.objects.get(pk=kwargs["pk"], nivel_bibliografico="c")
        ctx["coleccion"] = coleccion
        return ctx


class ImportarColeccionView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/importar.html"

    def get_coleccion(self):
        # pk viene de la URL: /coleccion/<pk>/importar/
        return get_object_or_404(
            ObraGeneral, pk=self.kwargs["pk"], nivel_bibliografico="c"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        coleccion = self.get_coleccion()
        inbox = default_inbox_for_collection(coleccion.id)
        repo = default_repo_for_collection(coleccion.id)

        digital_set = DigitalSet.objects.filter(coleccion=coleccion).first()

        ctx.update(
            {
                "coleccion": coleccion,
                "inbox_path": str(inbox),
                "repo_path": str(repo),
                "digital_set": digital_set,
                "pages_count": digital_set.pages.count() if digital_set else 0,
            }
        )
        return ctx

    def post(self, request, *args, **kwargs):
        """
        POST = ejecutar importación.
        En MVP vamos a:
        - leer archivos .tif/.tiff de la carpeta INBOX
        - ordenarlos por nombre (por ahora)
        - registrar páginas en DB
        NOTA: por ahora NO copiamos ni renombramos.
        """
        coleccion = self.get_coleccion()
        inbox = default_inbox_for_collection(coleccion.id)
        repo = default_repo_for_collection(coleccion.id)

        if not inbox.exists():
            messages.error(request, f"No existe la carpeta INBOX: {inbox}")
            return redirect("digitalizacion:importar", pk=coleccion.id)

        tiffs = sorted(
            [
                p
                for p in inbox.iterdir()
                if p.is_file() and p.suffix.lower() in [".tif", ".tiff"]
            ]
        )

        if not tiffs:
            messages.warning(request, "No se encontraron TIFF en la carpeta INBOX.")
            return redirect("digitalizacion:importar", pk=coleccion.id)

        digital_set, _ = DigitalSet.objects.get_or_create(coleccion=coleccion)
        digital_set.inbox_path = str(inbox)
        digital_set.repository_path = str(repo)

        created = 0
        # Crear carpetas destino
        master_dir = repo / "master"
        deriv_dir = repo / "derivatives"
        master_dir.mkdir(parents=True, exist_ok=True)
        deriv_dir.mkdir(parents=True, exist_ok=True)

        digital_set, _ = DigitalSet.objects.get_or_create(coleccion=coleccion)
        digital_set.inbox_path = str(inbox)
        digital_set.repository_path = str(repo)

        created = 0

        for idx, src in enumerate(tiffs, start=1):
            # nombres estándar
            master_name = f"coleccion_{coleccion.id}_p{idx:03d}.tif"
            jpg_name = f"coleccion_{coleccion.id}_p{idx:03d}.jpg"

            dst_master = master_dir / master_name
            dst_jpg = deriv_dir / jpg_name

            # 1) copiar master
            shutil.copy2(src, dst_master)

            # 2) generar jpg derivado (para visor web)
            try:
                im = Image.open(dst_master)
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                else:
                    im = im.convert("RGB")
                im.save(dst_jpg, "JPEG", quality=85, optimize=True)
            except Exception as e:
                messages.warning(request, f"No se pudo generar JPG para p{idx:03d}: {e}")
                # Aún así guardamos master. derivative_path queda vacío.
                dst_jpg = None

            # 3) guardar en DB (rutas relativas a MEDIA_ROOT)
            master_rel = to_media_relpath(dst_master)
            deriv_rel = to_media_relpath(dst_jpg) if dst_jpg else ""

            obj, was_created = DigitalPage.objects.update_or_create(
                digital_set=digital_set,
                page_number=idx,
                defaults={"master_path": master_rel, "derivative_path": deriv_rel},
            )
            if was_created:
                created += 1

        digital_set.total_pages = digital_set.pages.count()
        digital_set.estado = "IMPORTADO"
        digital_set.save()


        messages.success(
            request,
            f"Importación completa. Páginas detectadas: {len(tiffs)}. Nuevas: {created}.",
        )
        return redirect("digitalizacion:importar", pk=coleccion.id)


class SegmentarColeccionView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/segmentar.html"

    def get_coleccion_ds(self):
        coleccion = get_object_or_404(
            ObraGeneral, pk=self.kwargs["pk"], nivel_bibliografico="c"
        )
        ds = DigitalSet.objects.filter(coleccion=coleccion).first()
        return coleccion, ds

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        coleccion, ds = self.get_coleccion_ds()
        max_pages = ds.pdf_total_pages if ds and ds.pdf_path and ds.pdf_total_pages else (ds.total_pages if ds else 0)

        ctx["coleccion"] = coleccion
        ctx["digital_set"] = ds
        ctx["pages"] = ds.pages.all() if ds else []
        ctx["segments"] = ds.segments.select_related("obra").all() if ds else []
        ctx["max_pages"] = max_pages

        return ctx

    def post(self, request, *args, **kwargs):
        coleccion, ds = self.get_coleccion_ds()
        if not ds:
            messages.error(
                request, "Primero debes importar el escaneo de la colección."
            )
            return redirect("digitalizacion:importar", pk=coleccion.id)

        obra_id = request.POST.get("obra_id")
        start_page = request.POST.get("start_page")
        end_page = request.POST.get("end_page")
        tipo = request.POST.get("tipo", "OBRA")

        if not (obra_id and start_page and end_page):
            messages.error(request, "Faltan datos (obra, inicio, fin).")
            return redirect("digitalizacion:segmentar", pk=coleccion.id)

        try:
            obra_id = int(obra_id)
            start_page = int(start_page)
            end_page = int(end_page)
        except ValueError:
            messages.error(request, "Inicio/fin inválidos.")
            return redirect("digitalizacion:segmentar", pk=coleccion.id)

        if start_page > end_page:
            messages.error(request, "Inicio no puede ser mayor que fin.")
            return redirect("digitalizacion:segmentar", pk=coleccion.id)

        # Si hay PDF cargado, manda el PDF
        total = ds.pdf_total_pages if ds.pdf_path and ds.pdf_total_pages else ds.total_pages
        if start_page < 1 or end_page > total:
            messages.error(request, f"Rango fuera de límites. Total páginas: {total}.")
            return redirect("digitalizacion:segmentar", pk=coleccion.id)

        obra = get_object_or_404(ObraGeneral, pk=obra_id)
        WorkSegment.objects.create(
            obra=obra,
            digital_set=ds,
            start_page=start_page,
            end_page=end_page,
            tipo=tipo,
        )

        messages.success(
            request,
            f"Segmento creado: Obra {obra_id} ({start_page}-{end_page}) [{tipo}].",
        )
        return redirect("digitalizacion:segmentar", pk=coleccion.id)


class VisorColeccionView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/visor_coleccion.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        coleccion = get_object_or_404(
            ObraGeneral, pk=self.kwargs["pk"], nivel_bibliografico="c"
        )
        ds = DigitalSet.objects.filter(coleccion=coleccion).first()
        ctx["coleccion"] = coleccion
        ctx["digital_set"] = ds
        ctx["pages"] = ds.pages.all() if ds else []
        ctx["segments"] = ds.segments.select_related("obra").all() if ds else []
        return ctx


class SubirPdfColeccionView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/subir_pdf.html"

    def get_coleccion_ds(self):
        coleccion = get_object_or_404(
            ObraGeneral, pk=self.kwargs["pk"], nivel_bibliografico="c"
        )
        ds, _ = DigitalSet.objects.get_or_create(coleccion=coleccion)
        repo = default_repo_for_collection(coleccion.id)
        ds.repository_path = ds.repository_path or str(repo)
        ds.save()
        return coleccion, ds, repo

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        coleccion, ds, repo = self.get_coleccion_ds()
        ctx["coleccion"] = coleccion
        ctx["digital_set"] = ds
        return ctx

    def post(self, request, *args, **kwargs):
        coleccion, ds, repo = self.get_coleccion_ds()

        f = request.FILES.get("pdf")
        if not f:
            messages.error(request, "Debes seleccionar un PDF.")
            return redirect("digitalizacion:subir_pdf", pk=coleccion.id)

        if not f.name.lower().endswith(".pdf"):
            messages.error(request, "El archivo debe ser PDF.")
            return redirect("digitalizacion:subir_pdf", pk=coleccion.id)

        master_dir = repo / "master"
        master_dir.mkdir(parents=True, exist_ok=True)

        pdf_name = f"coleccion_{coleccion.id}.pdf"
        dst = master_dir / pdf_name

        with open(dst, "wb+") as out:
            for chunk in f.chunks():
                out.write(chunk)

        ds.pdf_path = to_media_relpath(dst)
        ds.save()

        reader = PdfReader(str(dst))
        ds.pdf_total_pages = len(reader.pages)
        ds.pdf_path = to_media_relpath(dst)
        ds.save()

        messages.success(request, "PDF cargado correctamente.")
        return redirect("digitalizacion:visor_coleccion", pk=coleccion.id)


class VisorObraView(LoginRequiredMixin, TemplateView):
    template_name = "digitalizacion/visor_obra.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        obra = get_object_or_404(ObraGeneral, pk=self.kwargs["obra_id"])

        # Segmentos asignados a esta obra (puede haber más de uno)
        segments = (
            WorkSegment.objects.filter(obra=obra)
            .select_related("digital_set", "digital_set__coleccion")
            .order_by("start_page")
        )

        if not segments.exists():
            ctx.update(
                {
                    "obra": obra,
                    "segments": [],
                    "digital_set": None,
                    "coleccion": None,
                    "pages": [],
                    "start_page": None,
                }
            )
            return ctx

        # MVP: asumimos que los segmentos de una obra apuntan al mismo DigitalSet (misma colección)
        first_seg = segments.first()
        ds = first_seg.digital_set
        coleccion = ds.coleccion

        # tomamos solo el primer rango como “inicio”
        start_page = first_seg.start_page
        end_page = first_seg.end_page

        pages = DigitalPage.objects.filter(
            digital_set=ds, page_number__gte=start_page, page_number__lte=end_page
        ).order_by("page_number")

        ctx.update(
            {
                "obra": obra,
                "segments": segments,
                "digital_set": ds,
                "coleccion": coleccion,
                "pages": pages,
                "start_page": start_page,
                "end_page": end_page,
            }
        )
        return ctx


def api_buscar_obras(request):
    q = (request.GET.get("q") or "").strip()
    coleccion_id = request.GET.get("coleccion_id")

    if len(q) < 2:
        return JsonResponse({"results": []})

    # Normalizar coleccion_id
    try:
        coleccion_id = int(coleccion_id) if coleccion_id else None
    except ValueError:
        coleccion_id = None

    qs = ObraGeneral.objects.exclude(nivel_bibliografico="c").filter(
        Q(num_control__icontains=q)
        | Q(centro_catalogador__icontains=q)
        | Q(titulo_principal__icontains=q)
        | Q(compositor__apellidos_nombres__icontains=q)
    )

    # Excluir obras ya segmentadas en esta colección (si hay DS)
    if coleccion_id:
        ds = DigitalSet.objects.filter(coleccion_id=coleccion_id).first()
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
            "label": f"{o.signatura_publica_display} — {o.titulo_principal}",
        }
        for o in qs
    ]

    return JsonResponse({"results": results})


@require_POST
def eliminar_segmento(request, segment_id):
    seg = get_object_or_404(WorkSegment, pk=segment_id)
    coleccion_id = seg.digital_set.coleccion_id
    seg.delete()
    messages.success(request, "Segmento eliminado.")
    return redirect("digitalizacion:segmentar", pk=coleccion_id)
