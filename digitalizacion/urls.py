from django.urls import path
from . import views

app_name = "digitalizacion"

urlpatterns = [
    # Dashboard principal
    path("", views.DigitalizacionDashboardView.as_view(), name="dashboard"),

    # Home de digitalización para cualquier obra (colección u obra suelta)
    path(
        "obra/<int:pk>/",
        views.ObraDigitalizacionHomeView.as_view(),
        name="obra_home",
    ),
    # Alias para compatibilidad (coleccion_home -> obra_home)
    path(
        "coleccion/<int:pk>/",
        views.ObraDigitalizacionHomeView.as_view(),
        name="coleccion_home",
    ),

    # Importar TIFF
    path(
        "obra/<int:pk>/importar/",
        views.ImportarObraView.as_view(),
        name="importar",
    ),

    # Segmentar (solo para colecciones)
    path(
        "obra/<int:pk>/segmentar/",
        views.SegmentarObraView.as_view(),
        name="segmentar",
    ),

    # Eliminar segmento
    path(
        "segmento/<int:segment_id>/eliminar/",
        views.eliminar_segmento,
        name="segmento_eliminar",
    ),

    # API búsqueda de obras
    path("api/buscar-obras/", views.api_buscar_obras, name="api_buscar_obras"),

    # Visor del documento digitalizado (para colecciones y obras sueltas)
    path(
        "obra/<int:pk>/visor/",
        views.VisorObraDigitalView.as_view(),
        name="visor_digital",
    ),
    # Alias para compatibilidad (visor_coleccion -> visor_digital)
    path(
        "coleccion/<int:pk>/visor/",
        views.VisorObraDigitalView.as_view(),
        name="visor_coleccion",
    ),

    # Subir PDF
    path(
        "obra/<int:pk>/subir-pdf/",
        views.SubirPdfObraView.as_view(),
        name="subir_pdf",
    ),

    # Eliminar PDF (solo el PDF, mantiene TIFF/JPG)
    path(
        "obra/<int:pk>/eliminar-pdf/",
        views.EliminarPdfObraView.as_view(),
        name="eliminar_pdf",
    ),

    # Eliminar todo el DigitalSet (PDF + TIFF + JPG + registros)
    path(
        "obra/<int:pk>/eliminar-digitalset/",
        views.EliminarDigitalSetView.as_view(),
        name="eliminar_digitalset",
    ),

    # Visor de obra dentro de colección (segmento)
    path(
        "obra/<int:obra_id>/visor-segmento/",
        views.VisorObraSegmentoView.as_view(),
        name="visor_obra",
    ),
]
