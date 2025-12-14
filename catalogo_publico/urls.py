from django.urls import path
from .views import (
    HomePublicoView,
    ListaObrasPublicaView,
    DetalleObraPublicaView,
    VistaDetalladaObraView,
)

app_name = 'catalogo_publico'

urlpatterns = [
    path('', HomePublicoView.as_view(), name='home'),
    path('obras/', ListaObrasPublicaView.as_view(), name='lista_obras'),
    path('obras/<int:pk>/', DetalleObraPublicaView.as_view(), name='detalle'),
    path('obras/<int:pk>/detalle/', VistaDetalladaObraView.as_view(), name='detalle_obra'),
]
