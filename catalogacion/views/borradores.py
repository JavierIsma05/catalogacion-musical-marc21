"""
Vistas AJAX para gestión de borradores de obras MARC21
"""

import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from catalogacion.models import BorradorObra


@require_http_methods(["POST"])
def guardar_borrador_ajax(request):
    """
    Guarda o actualiza un borrador vía AJAX.

    POST data esperado:
    {
        "tipo_obra": "manuscrito_independiente",
        "datos_formulario": {...},
        "pestana_actual": 0,
        "borrador_id": 123  // opcional, si existe actualiza
    }
    """
    try:
        data = json.loads(request.body)

        tipo_obra = data.get("tipo_obra")
        datos_formulario = data.get("datos_formulario")
        pestana_actual = data.get("pestana_actual", 0)
        borrador_id = data.get("borrador_id")
        obra_objetivo_id = data.get("obra_objetivo_id")

        if not datos_formulario or (not tipo_obra and not obra_objetivo_id):
            return JsonResponse(
                {
                    "success": False,
                    "error": "Faltan datos requeridos (datos_formulario y tipo_obra u obra_objetivo_id)",
                },
                status=400,
            )

        # Actualizar o crear borrador
        if borrador_id:
            try:
                borrador = BorradorObra.objects.get(id=borrador_id)
                if tipo_obra:
                    borrador.tipo_obra = tipo_obra
                if obra_objetivo_id:
                    borrador.obra_objetivo_id = obra_objetivo_id
                borrador.datos_formulario = datos_formulario
                borrador.pestana_actual = pestana_actual
                borrador.save()
                mensaje = "Borrador actualizado exitosamente"
            except BorradorObra.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Borrador no encontrado"}, status=404
                )
        else:
            # Crear nuevo borrador
            borrador = BorradorObra.objects.create(
                tipo_obra=tipo_obra or "edicion",
                obra_objetivo_id=obra_objetivo_id,
                datos_formulario=datos_formulario,
                pestana_actual=pestana_actual,
                usuario=request.user if request.user.is_authenticated else None,
            )
            mensaje = "Borrador guardado exitosamente"

        return JsonResponse(
            {
                "success": True,
                "message": mensaje,
                "borrador_id": borrador.id,
                "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                "titulo_temporal": borrador.titulo_temporal,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse(
            {"success": False, "error": f"Error del servidor: {str(e)}"}, status=500
        )


@require_http_methods(["GET"])
def obtener_borrador_ajax(request, borrador_id):
    """
    Obtiene un borrador específico por ID.

    Response:
    {
        "success": true,
        "borrador": {
            "id": 123,
            "tipo_obra": "manuscrito_independiente",
            "datos_formulario": {...},
            "pestana_actual": 2,
            "titulo_temporal": "Sinfonía...",
            "fecha_modificacion": "2024-11-17T10:30:00"
        }
    }
    """
    try:
        borrador = get_object_or_404(BorradorObra, id=borrador_id)

        return JsonResponse(
            {
                "success": True,
                "borrador": {
                    "id": borrador.id,
                    "tipo_obra": borrador.tipo_obra,
                    "datos_formulario": borrador.datos_formulario,
                    "pestana_actual": borrador.pestana_actual,
                    "titulo_temporal": borrador.titulo_temporal,
                    "num_control_temporal": borrador.num_control_temporal,
                    "tipo_registro": borrador.tipo_registro,
                    "nivel_bibliografico": borrador.nivel_bibliografico,
                    "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                    "fecha_creacion": borrador.fecha_creacion.isoformat(),
                },
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=404)


@require_http_methods(["GET"])
def verificar_borrador_ajax(request):
    """
    Verifica si existe un borrador para un tipo de obra específico.

    Query params:
    - tipo_obra: tipo de obra a verificar

    Response:
    {
        "success": true,
        "tiene_borrador": true,
        "borrador": {...}  // último borrador encontrado
    }
    """
    try:
        tipo_obra = request.GET.get("tipo_obra")

        if not tipo_obra:
            return JsonResponse(
                {"success": False, "error": "Tipo de obra no especificado"}, status=400
            )

        # Buscar el borrador más reciente activo para este tipo de obra.
        # En modo creación, solo aplican borradores SIN obra_objetivo.
        borrador = (
            BorradorObra.objects.filter(
                tipo_obra=tipo_obra,
                estado="activo",
                obra_objetivo__isnull=True,
            )
            .order_by("-fecha_modificacion")
            .first()
        )

        if borrador:
            return JsonResponse(
                {
                    "success": True,
                    "tiene_borrador": True,
                    "borrador": {
                        "id": borrador.id,
                        "titulo_temporal": borrador.titulo_temporal,
                        "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                        "dias_antiguedad": borrador.dias_desde_modificacion,
                        "pestana_actual": borrador.pestana_actual,
                    },
                }
            )
        else:
            return JsonResponse({"success": True, "tiene_borrador": False})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["GET"])
def obtener_ultimo_borrador_obra_ajax(request, obra_id):
    """Obtiene el último borrador activo asociado a una obra existente (edición)."""
    try:
        borrador = (
            BorradorObra.objects.filter(
                obra_objetivo_id=obra_id,
                estado="activo",
            )
            .order_by("-fecha_modificacion")
            .first()
        )

        if not borrador:
            return JsonResponse({"success": True, "tiene_borrador": False})

        return JsonResponse(
            {
                "success": True,
                "tiene_borrador": True,
                "borrador": {
                    "id": borrador.id,
                    "tipo_obra": borrador.tipo_obra,
                    "datos_formulario": borrador.datos_formulario,
                    "pestana_actual": borrador.pestana_actual,
                    "titulo_temporal": borrador.titulo_temporal,
                    "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                    "fecha_creacion": borrador.fecha_creacion.isoformat(),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["DELETE", "POST"])
def eliminar_borrador_ajax(request, borrador_id):
    """
    Marca un borrador como descartado (soft delete).
    Acepta DELETE o POST (para compatibilidad con navegadores antiguos)
    """
    try:
        borrador = get_object_or_404(BorradorObra, id=borrador_id)
        titulo = borrador.titulo_temporal

        # Soft delete: marcar como descartado
        borrador.estado = "descartado"
        borrador.save()

        return JsonResponse(
            {"success": True, "message": f'Borrador "{titulo}" descartado exitosamente'}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["GET"])
def listar_borradores_ajax(request):
    """
    Lista todos los borradores ordenados por fecha de modificación.

    Query params opcionales:
    - tipo_obra: filtrar por tipo de obra
    - limit: límite de resultados (default: 20)

    Response:
    {
        "success": true,
        "borradores": [
            {
                "id": 123,
                "tipo_obra": "manuscrito_independiente",
                "titulo_temporal": "Sinfonía...",
                "fecha_modificacion": "2024-11-17T10:30:00",
                "dias_antiguedad": 0
            },
            ...
        ],
        "total": 5
    }
    """
    try:
        tipo_obra = request.GET.get("tipo_obra")
        limit = int(request.GET.get("limit", 20))

        # Solo mostrar borradores activos
        queryset = BorradorObra.objects.filter(estado="activo")

        if tipo_obra:
            queryset = queryset.filter(tipo_obra=tipo_obra)

        borradores = queryset[:limit]

        lista_borradores = []
        for borrador in borradores:
            lista_borradores.append(
                {
                    "id": borrador.id,
                    "tipo_obra": borrador.tipo_obra,
                    "tipo_obra_descripcion": borrador.get_descripcion_tipo(),
                    "titulo_temporal": borrador.titulo_temporal,
                    "num_control_temporal": borrador.num_control_temporal,
                    "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                    "fecha_creacion": borrador.fecha_creacion.isoformat(),
                    "pestana_actual": borrador.pestana_actual,
                    "dias_antiguedad": borrador.dias_desde_modificacion(),
                }
            )

        return JsonResponse(
            {"success": True, "borradores": lista_borradores, "total": queryset.count()}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["POST"])
def autoguardar_borrador_ajax(request):
    """
    Versión simplificada de guardar_borrador para autoguardado automático.
    Actualiza si ya existe un borrador_id, o crea uno nuevo si no existe.
    """
    try:
        data = json.loads(request.body)

        borrador_id = data.get("borrador_id")
        tipo_obra = data.get("tipo_obra")
        datos_formulario = data.get("datos_formulario")
        pestana_actual = data.get("pestana_actual", 0)
        obra_objetivo_id = data.get("obra_objetivo_id")

        if not datos_formulario:
            return JsonResponse(
                {"success": False, "error": "Se requiere datos_formulario"}, status=400
            )

        # Si hay borrador_id, actualizar
        if borrador_id:
            try:
                borrador = BorradorObra.objects.get(id=borrador_id)
                borrador.datos_formulario = datos_formulario
                borrador.pestana_actual = pestana_actual
                if tipo_obra:
                    borrador.tipo_obra = tipo_obra
                if obra_objetivo_id:
                    borrador.obra_objetivo_id = obra_objetivo_id
                borrador.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Autoguardado",
                        "borrador_id": borrador.id,
                        "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                    }
                )
            except BorradorObra.DoesNotExist:
                # Si no existe, crear uno nuevo
                pass

        # Si no hay borrador_id o no existe, crear nuevo
        if not tipo_obra and not obra_objetivo_id:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Se requiere tipo_obra u obra_objetivo_id para crear nuevo borrador",
                },
                status=400,
            )

        borrador = BorradorObra.objects.create(
            tipo_obra=tipo_obra or "edicion",
            obra_objetivo_id=obra_objetivo_id,
            datos_formulario=datos_formulario,
            pestana_actual=pestana_actual,
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Borrador creado",
                "borrador_id": borrador.id,
                "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                "titulo_temporal": borrador.titulo_temporal,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ============================================================================
# Vistas de Interfaz Web para Gestión de Borradores
# ============================================================================

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from usuarios.mixins import CatalogadorRequiredMixin


class ListaBorradoresView(CatalogadorRequiredMixin, ListView):
    """Vista para listar borradores activos del usuario actual"""

    model = BorradorObra
    template_name = "catalogacion/lista_borradores.html"
    context_object_name = "borradores"
    paginate_by = 20

    def get_queryset(self):
        """Obtener solo borradores activos del usuario, ordenados por fecha de modificación"""
        queryset = BorradorObra.objects.filter(estado="activo").order_by(
            "-fecha_modificacion"
        )

        # Filtrar por el usuario autenticado (solo sus borradores)
        # Los administradores ven todos los borradores
        if self.request.user.is_authenticated:
            if not self.request.user.es_admin:
                queryset = queryset.filter(usuario=self.request.user)

        # Filtrar por búsqueda si hay query
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(titulo_temporal__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_borradores"] = self.get_queryset().count()
        # Labels de pestañas para mostrar dónde quedó el usuario.
        # Deben mantenerse en sync con el orden definido en crear_obra.html (tabs).
        context["tab_labels"] = [
            "Nombres y títulos",
            "Producción / edición",
            "Datos musicales",
            "Materias / serie",
            "Notas",
            "Relaciones",
            "Existencias",
            "Administración",
        ]
        return context


class DescartarBorradorView(DeleteView):
    """Vista para descartar un borrador (soft delete)"""

    model = BorradorObra
    success_url = reverse_lazy("catalogacion:lista_borradores")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        titulo = self.object.titulo_temporal

        # Soft delete: marcar como descartado
        self.object.estado = "descartado"
        self.object.save()

        messages.success(request, f'Borrador "{titulo}" descartado exitosamente')
        return redirect(self.success_url)


def recuperar_borrador_view(request, pk):
    """
    Vista para recuperar un borrador y redirigir al formulario de creación
    """
    borrador = get_object_or_404(BorradorObra, pk=pk, estado="activo")

    # Mapeo de valores antiguos del JavaScript a los valores correctos de TIPO_OBRA_CONFIG
    mapeo_tipos = {
        "manuscrito_coleccion": "coleccion_manuscrita",
        "manuscrito_independiente": "obra_manuscrita_individual",
        "impreso_coleccion": "coleccion_impresa",
        "impreso_independiente": "obra_impresa_individual",
    }

    # Convertir el tipo_obra si viene en formato antiguo
    tipo_obra_correcto = mapeo_tipos.get(borrador.tipo_obra, borrador.tipo_obra)

    # Guardar el ID del borrador en la sesión para que lo use el formulario
    request.session["borrador_id"] = borrador.id
    request.session["tipo_obra"] = tipo_obra_correcto

    # Redirigir al formulario de creación con el tipo de obra correcto
    messages.info(request, f"Recuperando borrador: {borrador.titulo_temporal}")

    return redirect("catalogacion:crear_obra", tipo=tipo_obra_correcto)


@require_http_methods(["POST"])
def limpiar_sesion_borrador_ajax(request):
    """
    Limpia las variables de sesión relacionadas con borradores.
    Se llama después de cargar exitosamente un borrador para evitar recargas automáticas.
    """
    try:
        # Limpiar variables de sesión de borrador
        if "borrador_id" in request.session:
            del request.session["borrador_id"]
        if "tipo_obra" in request.session:
            del request.session["tipo_obra"]

        request.session.modified = True

        return JsonResponse(
            {"success": True, "message": "Sesión limpiada exitosamente"}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["GET"])
def obtener_borrador_activo_ajax(request):
    """
    Obtiene el borrador activo para un tipo de obra específico.
    Este endpoint es usado para restaurar el borrador al recargar la página.

    Query params:
    - tipo_obra: tipo de obra (requerido)
    - obra_id: ID de obra si es modo edición (opcional)

    Response:
    {
        "success": true,
        "tiene_borrador": true,
        "borrador": {...}
    }
    """
    try:
        tipo_obra = request.GET.get("tipo_obra")
        obra_id = request.GET.get("obra_id")

        if not tipo_obra and not obra_id:
            return JsonResponse(
                {"success": False, "error": "Se requiere tipo_obra u obra_id"},
                status=400,
            )

        # Modo edición: buscar por obra_id
        if obra_id:
            borrador = (
                BorradorObra.objects.filter(
                    obra_objetivo_id=obra_id,
                    estado="activo",
                )
                .order_by("-fecha_modificacion")
                .first()
            )
        else:
            # Modo creación: buscar por tipo_obra (sin obra_objetivo)
            borrador = (
                BorradorObra.objects.filter(
                    tipo_obra=tipo_obra,
                    estado="activo",
                    obra_objetivo__isnull=True,
                )
                .order_by("-fecha_modificacion")
                .first()
            )

        if not borrador:
            return JsonResponse({"success": True, "tiene_borrador": False})

        return JsonResponse(
            {
                "success": True,
                "tiene_borrador": True,
                "borrador": {
                    "id": borrador.id,
                    "tipo_obra": borrador.tipo_obra,
                    "datos_formulario": borrador.datos_formulario,
                    "pestana_actual": borrador.pestana_actual,
                    "titulo_temporal": borrador.titulo_temporal,
                    "fecha_modificacion": borrador.fecha_modificacion.isoformat(),
                },
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["POST"])
def limpiar_borrador_tipo_ajax(request):
    """
    Descarta todos los borradores activos de un tipo de obra específico.
    Se usa cuando el usuario hace clic en "Nueva obra" para empezar desde cero.

    POST data:
    {
        "tipo_obra": "coleccion_manuscrita"
    }
    """
    try:
        data = json.loads(request.body)
        tipo_obra = data.get("tipo_obra")

        if not tipo_obra:
            return JsonResponse(
                {"success": False, "error": "Se requiere tipo_obra"}, status=400
            )

        # Marcar como descartados todos los borradores de este tipo (sin obra_objetivo)
        count = BorradorObra.objects.filter(
            tipo_obra=tipo_obra,
            estado="activo",
            obra_objetivo__isnull=True,
        ).update(estado="descartado")

        return JsonResponse(
            {
                "success": True,
                "message": f"{count} borrador(es) descartado(s)",
                "count": count,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
