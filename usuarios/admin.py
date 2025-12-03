# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ['email']
    list_display = ['email', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('email', 'pa:sword')}),
        ('Información Personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
