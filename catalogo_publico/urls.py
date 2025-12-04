from django.urls import path
from .views import (
    HomePublicoView,
    ListaObrasPublicaView,
    DetalleObraPublicaView,
)

app_name = 'catalogo_publico'

urlpatterns = [
    path('', HomePublicoView.as_view(), name='home'),
    path('obras/', ListaObrasPublicaView.as_view(), name='lista_obras'),
    path('obras/<int:pk>/', DetalleObraPublicaView.as_view(), name='detalle_obra'),
]
