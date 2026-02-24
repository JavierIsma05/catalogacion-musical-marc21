from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import SolicitudUsuario
from .models import Notification


class SolicitudUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'correo', 'cedula', 'tipo_usuario', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'tipo_usuario')
    search_fields = ('nombres', 'correo', 'cedula')



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ['email']
    list_display = ['email', 'nombre_completo', 'rol', 'activo', 'is_staff', 'fecha_creacion']
    list_filter = ['rol', 'activo', 'is_staff', 'is_superuser']
    search_fields = ['email', 'nombre_completo']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre_completo',)}),
        ('Rol y Estado', {'fields': ('rol', 'activo')}),
        ('Permisos Django', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre_completo', 'rol', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SolicitudUsuario, SolicitudUsuarioAdmin)
admin.site.register(Notification)
