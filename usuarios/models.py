from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager personalizado porque el de defecto espera un username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("rol", CustomUser.ROL_ADMIN)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Modelo de usuario personalizado con roles"""

    # Tipos de roles
    ROL_CATALOGADOR = "catalogador"
    ROL_ADMIN = "admin"

    ROL_CHOICES = [
        (ROL_CATALOGADOR, "Catalogador"),
        (ROL_ADMIN, "Administrador"),
    ]

    # Tipos de catalogador
    TIPO_INVESTIGADOR_UNL = "investigador_unl"
    TIPO_INVESTIGADOR_EXTERNO = "investigador_externo"
    TIPO_COLABORADOR = "colaborador"
    TIPO_PASANTE = "pasante"
    TIPO_OTROS = "otros"

    TIPO_CATALOGADOR_CHOICES = [
        (TIPO_INVESTIGADOR_UNL, "Investigador UNL"),
        (TIPO_INVESTIGADOR_EXTERNO, "Investigador Externo"),
        (TIPO_COLABORADOR, "Colaborador"),
        (TIPO_PASANTE, "Pasante"),
        (TIPO_OTROS, "Otros"),
    ]

    username = None  # Eliminamos el campo username
    email = models.EmailField("email address", unique=True)

    # Nuevo campo para el rol
    rol = models.CharField(
        "Rol",
        max_length=20,
        choices=ROL_CHOICES,
        default=ROL_CATALOGADOR,
        help_text="Define los permisos del usuario en el sistema",
    )

    # Tipo de catalogador
    tipo_catalogador = models.CharField(
        "Tipo de Catalogador",
        max_length=30,
        choices=TIPO_CATALOGADOR_CHOICES,
        default=TIPO_OTROS,
        help_text="Clasificación del catalogador según su rol en la institución",
    )

    # Campos adicionales útiles
    nombre_completo = models.CharField(
        "Nombre completo",
        max_length=200,
        blank=True,
        help_text="Nombre completo del usuario",
    )
    activo = models.BooleanField(
        "Activo",
        default=True,
        help_text="Indica si el usuario puede acceder al sistema",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.nombre_completo or self.email

    @property
    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.rol == self.ROL_ADMIN or self.is_superuser

    @property
    def es_catalogador(self):
        """Verifica si el usuario es catalogador"""
        return self.rol == self.ROL_CATALOGADOR

    @property
    def puede_catalogar(self):
        """Verifica si el usuario puede catalogar (admin o catalogador)"""
        return self.es_admin or self.es_catalogador


class SolicitudUsuario(models.Model):
    """Modelo para almacenar solicitudes de creación de cuenta por usuarios externos."""

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_RECHAZADO = 'rechazado'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
    ]

    TIPO_CATALOGADOR = 'Catalogador'
    TIPO_ADMIN = 'Administrador'
    TIPO_CONSULTA = 'Consulta'
    TIPO_OTRO = 'Otro'

    TIPO_USUARIO_CHOICES = [
        (TIPO_CATALOGADOR, 'Catalogador'),
        (TIPO_ADMIN, 'Administrador'),
        (TIPO_CONSULTA, 'Consulta'),
        (TIPO_OTRO, 'Otro'),
    ]

    nombres = models.CharField('Nombres completos', max_length=250)
    cedula = models.CharField('Cédula', max_length=50)
    correo = models.EmailField('Correo', max_length=254)
    telefono = models.CharField('Teléfono', max_length=50, blank=True)
    tipo_usuario = models.CharField('Tipo solicitado', max_length=30, choices=TIPO_USUARIO_CHOICES)
    motivo = models.TextField('Motivo', help_text='Razón para solicitar acceso')
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    fecha_respuesta = models.DateTimeField('Fecha de respuesta', null=True, blank=True)
    respondido_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='solicitudes_respondidas')

    class Meta:
        verbose_name = 'Solicitud de Cuenta'
        verbose_name_plural = 'Solicitudes de Cuenta'
        ordering = ['-fecha_creacion']
        indexes = [models.Index(fields=['correo']), models.Index(fields=['cedula']),]

    def __str__(self):
        return f"{self.nombres} <{self.correo}> ({self.estado})"

    def marcar_aprobada(self, respondido_por=None):
        self.estado = self.ESTADO_APROBADO
        self.fecha_respuesta = timezone.now()
        self.respondido_por = respondido_por
        self.save()

    def marcar_rechazada(self, respondido_por=None):
        self.estado = self.ESTADO_RECHAZADO
        self.fecha_respuesta = timezone.now()
        self.respondido_por = respondido_por
        self.save()


class Notification(models.Model):
    """Notificación interna para administradores relacionada a solicitudes."""

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    solicitud = models.ForeignKey(SolicitudUsuario, on_delete=models.CASCADE, related_name='notifications')
    mensaje = models.CharField(max_length=300)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Notificación para {self.usuario}: {self.mensaje[:50]}"
