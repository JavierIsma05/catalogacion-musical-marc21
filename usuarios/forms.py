from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


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
