from django.urls import path

from .views import (
    DescargarPDFObraView,
    DetalleObraPublicaView,
    FormatoMARC21View,
    HomePublicoView,
    ListaObrasPublicaView,
    VistaDetalladaObraView,
    VistaMARCCrudoView,
)

app_name = "catalogo_publico"

urlpatterns = [
    path("", HomePublicoView.as_view(), name="home"),
    path("obras/", ListaObrasPublicaView.as_view(), name="lista_obras"),
    path("obras/<int:pk>/", DetalleObraPublicaView.as_view(), name="detalle"),
    path(
        "obras/<int:pk>/detalle/", VistaDetalladaObraView.as_view(), name="detalle_obra"
    ),
    path("obras/<int:pk>/marc21/", FormatoMARC21View.as_view(), name="formato_marc21"),
    path("obras/<int:pk>/descargar-pdf/", DescargarPDFObraView.as_view(), name="descargar_pdf"),
    path("obras/<int:pk>/marc-crudo/", VistaMARCCrudoView.as_view(), name="vista_marc_crudo"),
]
