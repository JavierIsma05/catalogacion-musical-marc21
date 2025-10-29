from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_marc21, name='formulario_marc21'),
]
