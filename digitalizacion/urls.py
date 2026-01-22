from django.urls import path
from . import views

app_name = "digitalizacion"

urlpatterns = [
    path("", views.DigitalizacionDashboardView.as_view(), name="dashboard"),
    path(
        "coleccion/<int:pk>/",
        views.ColeccionDigitalizacionHomeView.as_view(),
        name="coleccion_home",
    ),
    path(
        "coleccion/<int:pk>/importar/",
        views.ImportarColeccionView.as_view(),
        name="importar",
    ),
    path(
        "coleccion/<int:pk>/segmentar/",
        views.SegmentarColeccionView.as_view(),
        name="segmentar",
    ),
    path(
        "segmento/<int:segment_id>/eliminar/",
        views.eliminar_segmento,
        name="segmento_eliminar",
    ),
    path("api/buscar-obras/", views.api_buscar_obras, name="api_buscar_obras"),
    path(
        "coleccion/<int:pk>/visor/",
        views.VisorColeccionView.as_view(),
        name="visor_coleccion",
    ),
    path(
        "coleccion/<int:pk>/subir-pdf/",
        views.SubirPdfColeccionView.as_view(),
        name="subir_pdf",
    ),
    path("obra/<int:obra_id>/visor/", views.VisorObraView.as_view(), name="visor_obra"),
]
