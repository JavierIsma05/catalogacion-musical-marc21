from django.http import JsonResponse
from django.views.decorators.http import require_GET
from catalogacion.models import ObraGeneral

@require_GET
def buscar_obras(request):
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    qs = (
        ObraGeneral.objects
        .select_related("compositor", "titulo_uniforme")
        .filter(num_control__icontains=q)
        .order_by("num_control")[:20]
    )

    results = []
    for o in qs:
        results.append({
            "id": o.id,
            "num_control": o.num_control,
            "titulo": o.titulo_principal or "",
            "compositor": (
                o.compositor.apellidos_nombres
                if o.compositor else ""
            ),
            "tipo": o.get_nivel_bibliografico_display(),
        })

    return JsonResponse({"results": results})
