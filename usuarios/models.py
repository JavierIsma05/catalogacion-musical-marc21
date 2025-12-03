from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Primero, necesitamos un Manager personalizado porque el de defecto espera un username
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Ahora sí, el modelo de usuario
class CustomUser(AbstractUser):
    username = None  # Eliminamos el campo username
    email = models.EmailField('email address', unique=True) # Hacemos el email único y obligatorio

    USERNAME_FIELD = 'email' # Le decimos a Django que use email para autenticar
    REQUIRED_FIELDS = [] # Email ya es requerido por USERNAME_FIELD, así que dejamos esto vacío

    objects = CustomUserManager() # Asignamos el manager nuevo

    def __str__(self):
        return self.email
