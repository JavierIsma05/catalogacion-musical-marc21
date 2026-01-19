from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from catalogacion.models import ObraGeneral
import json

@require_GET
def buscar_obras(request):
    obra_id = (request.GET.get("id") or "").strip()
    if obra_id:
        try:
            o = (
                ObraGeneral.objects
                .select_related("compositor", "titulo_uniforme")
                .get(id=obra_id)
            )
        except (ObraGeneral.DoesNotExist, ValueError):
            return JsonResponse({"results": []})

        return JsonResponse(
            {
                "results": [
                    {
                        "id": o.id,
                        "num_control": o.num_control,
                        "titulo": o.titulo_principal or "",
                        "compositor": (
                            o.compositor.apellidos_nombres
                            if o.compositor else ""
                        ),
                        "tipo": o.get_nivel_bibliografico_display(),
                    }
                ]
            }
        )

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
            "compositor_id": (o.compositor.id if o.compositor else None),
            "titulo_id": (o.titulo_uniforme.id if getattr(o, 'titulo_uniforme', None) else None),
            "tipo": o.get_nivel_bibliografico_display(),
        })

    return JsonResponse({"results": results})


@method_decorator(csrf_exempt, name='dispatch')
class Autocompletado773View(View):
    """
    API para obtener campos heredables de una obra padre via 773 $w
    """
    
    def get(self, request):
        """
        Busca obras para selección en campo 773 $w
        """
        q = (request.GET.get("q") or "").strip()
        if len(q) < 2:
            return JsonResponse({"results": []})
        
        # Buscar obras que puedan ser padre (colecciones u obras independientes)
        qs = (
            ObraGeneral.objects
            .select_related("compositor", "titulo_uniforme")
            .filter(
                num_control__icontains=q
            )
            .filter(
                nivel_bibliografico__in=['c', 'm']  # Solo colecciones o obras independientes
            )
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
                "tipo_registro": o.get_tipo_registro_display(),
                "nivel_bibliografico": o.get_nivel_bibliografico_display(),
            })
        
        return JsonResponse({"results": results})
    
    def post(self, request):
        """
        Obtiene campos heredables de una obra específica
        """
        try:
            data = json.loads(request.body)
            obra_id = data.get("obra_id")
            
            if not obra_id:
                return JsonResponse({
                    "error": "Se requiere obra_id"
                }, status=400)
            
            # Obtener la obra padre con todos los campos relacionados
            obra = (
                ObraGeneral.objects
                .select_related(
                    "compositor", 
                    "titulo_uniforme"
                )
                .prefetch_related(
                    "producciones_publicaciones__lugares",
                    "producciones_publicaciones__entidades", 
                    "producciones_publicaciones__fechas",
                    "medios_interpretacion_382__medios",
                    "ubicaciones_852__estanterias",
                    "disponibles_856__urls_856",
                    "disponibles_856__textos_enlace_856"
                )
                .get(id=obra_id)
            )
            
            # Obtener campos heredables usando el método del modelo
            campos_heredables = obra.obtener_campos_para_heredar_773()
            
            return JsonResponse({
                "success": True,
                "obra": {
                    "id": obra.id,
                    "num_control": obra.num_control,
                    "titulo": obra.titulo_principal,
                    "compositor": str(obra.compositor) if obra.compositor else None,
                },
                "campos_heredables": campos_heredables
            })
            
        except ObraGeneral.DoesNotExist:
            return JsonResponse({
                "error": "Obra no encontrada"
            }, status=404)
            
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "JSON inválido"
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                "error": f"Error del servidor: {str(e)}"
            }, status=500)
