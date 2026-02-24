from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser
from .models import SolicitudUsuario
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    """Formulario para crear usuarios (usado en admin y en gestión de catalogadores)"""

    class Meta:
        model = CustomUser
        fields = ("email", "nombre_completo", "tipo_catalogador", "activo")
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "admin-form-input", "placeholder": "correo@ejemplo.com"}
            ),
            "nombre_completo": forms.TextInput(
                attrs={
                    "class": "admin-form-input",
                    "placeholder": "Nombre completo del catalogador",
                }
            ),
            "tipo_catalogador": forms.Select(attrs={"class": "admin-form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "admin-form-checkbox"}),
        }
        error_messages = {
            "email": {
                "required": "Este campo es obligatorio.",
                "invalid": "Ingrese un correo electrónico válido.",
                "unique": "Ya existe un usuario con este correo.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases a campos de contraseña
        self.fields["password1"].widget.attrs.update(
            {"class": "admin-form-input", "placeholder": "Mínimo 8 caracteres"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "admin-form-input", "placeholder": "Repite la contraseña"}
        )
        # Mensajes de error en español para contraseñas
        self.fields["password1"].error_messages = {
            "required": "Este campo es obligatorio.",
        }
        self.fields["password2"].error_messages = {
            "required": "Este campo es obligatorio.",
        }
        # Quitar la opción vacía del select de tipo_catalogador
        self.fields["tipo_catalogador"].empty_label = None
        # El campo activo debe estar marcado por defecto
        if not self.instance.pk:
            self.fields["activo"].initial = True


class CustomUserChangeForm(UserChangeForm):
    """Formulario para editar usuarios (usado en Django Admin)"""

    class Meta:
        model = CustomUser
        fields = ("email", "nombre_completo", "tipo_catalogador", "rol", "activo")


class CustomUserUpdateForm(forms.ModelForm):
    """Formulario para actualizar catalogadores (sin cambio de contraseña)"""

    class Meta:
        model = CustomUser
        fields = ("email", "nombre_completo", "tipo_catalogador", "activo")
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "admin-form-input", "placeholder": "correo@ejemplo.com"}
            ),
            "nombre_completo": forms.TextInput(
                attrs={
                    "class": "admin-form-input",
                    "placeholder": "Nombre completo del catalogador",
                }
            ),
            "tipo_catalogador": forms.Select(attrs={"class": "admin-form-select"}),
            "activo": forms.CheckboxInput(attrs={"class": "admin-form-checkbox"}),
        }
        error_messages = {
            "email": {
                "required": "Este campo es obligatorio.",
                "invalid": "Ingrese un correo electrónico válido.",
                "unique": "Ya existe un usuario con este correo.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Quitar la opción vacía del select de tipo_catalogador
        self.fields["tipo_catalogador"].empty_label = None


class LoginForm(forms.Form):
    """Formulario de login personalizado"""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico",
                "autofocus": True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Contraseña"}
        )
    )


class SolicitudUsuarioForm(forms.ModelForm):
    class Meta:
        model = SolicitudUsuario
        fields = ("nombres", "cedula", "correo", "telefono", "tipo_usuario", "motivo")
        widgets = {
            "nombres": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombres completos"}),
            "cedula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de cédula"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "tipo_usuario": forms.Select(attrs={"class": "form-select"}),
            "motivo": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        # Verificar que no exista un usuario con dicho correo
        if CustomUser.objects.filter(email__iexact=correo).exists():
            raise ValidationError("Ya existe un usuario con este correo.")
        # Verificar que no exista una solicitud pendiente con el mismo correo
        if SolicitudUsuario.objects.filter(correo__iexact=correo, estado=SolicitudUsuario.ESTADO_PENDIENTE).exists():
            raise ValidationError("Ya existe una solicitud pendiente con este correo.")
        return correo

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if SolicitudUsuario.objects.filter(cedula__iexact=cedula, estado=SolicitudUsuario.ESTADO_PENDIENTE).exists():
            raise ValidationError("Ya existe una solicitud pendiente con esta cédula.")
        return cedula


class ProfileForm(forms.ModelForm):
    """Formulario que permite al usuario editar su propio perfil (sin contraseña)."""

    class Meta:
        model = CustomUser
        fields = ("email", "nombre_completo")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "nombre_completo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre completo"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Evitar colision con otros usuarios
        qs = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe otro usuario con ese correo.')
        return email
