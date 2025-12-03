from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    # Ruta para el Login
    path('login/', CustomLoginView.as_view(), name='login'),
    
    # Ruta para el Logout
    # Usamos la vista nativa directa, no requiere template (redirige)
    path('logout/', LogoutView.as_view(), name='logout'),
]
