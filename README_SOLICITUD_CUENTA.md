# Cambios: Sistema de Solicitud de Cuenta y Gestión de Perfil

Este README resume los cambios realizados para implementar el sistema de "Solicitud de Cuenta" (público) y las mejoras asociadas para la gestión de usuarios y claves.

Resumen funcional
- Usuarios no autenticados pueden solicitar una cuenta a través de un formulario público.
- Los administradores pueden ver las solicitudes, aprobar/rechazar, generar una contraseña temporal o generar un enlace de restablecimiento.
- Al aprobar una solicitud se crea un `CustomUser` con contraseña generada.
- El admin puede generar una contraseña temporal y verla UNA sola vez en la UI del panel administrativo.
- Los usuarios autenticados pueden editar su perfil (`email`, `nombre_completo`) y cambiar su contraseña desde su área de usuario.
- Se añadieron notificaciones internas para avisar a admins de nuevas solicitudes.

Archivos modificados / añadidos y razón de cambio

- `usuarios/models.py`
  - Añadido `SolicitudUsuario` para almacenar solicitudes públicas (campos: `nombres`, `cedula`, `correo`, `telefono`, `tipo_usuario`, `motivo`, `estado`, `fecha_respuesta`, `respondido_por`).
  - Añadido `Notification` para notificaciones internas relacionadas con solicitudes.
  - Motivo: persistir solicitudes y permitir notificaciones a administradores.

- `usuarios/forms.py`
  - Añadido `SolicitudUsuarioForm` con validaciones (correo único, no duplicar solicitudes pendientes por correo/cedula).
  - Añadido `ProfileForm` para que el usuario edite su `email` y `nombre_completo`.
  - Motivo: validación en servidor y formularios amigables para crear/editar datos.

- `usuarios/views.py`
  - Añadidas vistas públicas y admin:
    - `SolicitarCuentaView` (CreateView) — formulario público.
    - `AdminSolicitudesListView`, `DetalleSolicitudView` — lista y detalle para admins.
    - `CrearClaveTemporalView` — genera una contraseña temporal, la asigna al usuario y la muestra UNA vez.
    - `GenerarEnlaceResetView` y `AdminResetConfirmView` — opción admin para crear enlace de reset seguro.
    - `ProfileUpdateView` — permite que el usuario edite su propio perfil (se usa `ProfileForm`).
    - `UserPasswordChangeView`, `UserPasswordChangeDoneView` — cambio de contraseña para usuarios autenticados.
  - Motivo: implementar todas las interacciones necesarias (públicas y administrativas) para la gestión segura de cuentas.

- `usuarios/urls.py`
  - Nuevas rutas públicas/admin:
    - `solicitar-cuenta/` (público)
    - `admin/solicitudes/`, `admin/solicitudes/<pk>/` (admin)
    - `admin/catalogadores/<pk>/generar-clave/` (admin generar clave temporal)
    - `perfil/`, `perfil/password/`, `perfil/password/done/` (editar perfil y cambiar contraseña por el usuario)
  - Motivo: exponer endpoints necesarios.

- Plantillas añadidas/actualizadas (carpeta `usuarios/templates/usuarios/...`):
  - `solicitud/solicitar_cuenta.html` — formulario público (añadido).
  - `admin/solicitudes_list.html`, `admin/detalle_solicitud.html` — listado y detalle en admin.
  - `admin/mostrar_clave.html` — muestra la contraseña temporal UNA vez al admin.
  - `admin/mostrar_enlace_reset.html`, `admin/admin_reset_confirm.html` — flujo de reset por enlace.
  - `perfil/editar_perfil.html`, `perfil/password_change_form.html`, `perfil/password_change_done.html` — editar perfil y cambiar contraseña.
  - `admin/base_admin.html` — añadido enlace "Mi perfil" y campana de notificaciones.
  - `registration/inicio_sesion.html` — añadido enlace "Solicitar acceso".
  - `usuarios/admin/lista_catalogadores.html` — botón para "ver clave" (genera la temporal y la muestra).
  - Motivo: UI para todas las nuevas acciones.

- `marc21_project/settings.py`
  - Se añadió el context processor (si aplica) para exponer `solicitudes_pendientes_count` y notificaciones en las plantillas.
  - Motivo: mostrar contador de solicitudes pendientes y notificaciones en el sidebar/topbar.

- `usuarios/admin.py`
  - Registro de los nuevos modelos (`SolicitudUsuario`, `Notification`) y ajustes si corresponde.
  - Motivo: permitir gestión desde Django admin si se desea.

- Migraciones
  - Hay una migración relacionada con `SolicitudUsuario` (por ejemplo `usuarios/migrations/0004_solicitudusuario.py`).
  - Nota: Debes ejecutar migraciones si aun no lo hiciste: ejecutar `python manage.py migrate`.

Comportamiento de la contraseña temporal
- La contraseña temporal generada por el admin se asigna al usuario con `set_password()` (guardada en hash).
- El admin ve la contraseña temporal en pantalla UNA vez (no queda almacenada en texto claro en la base de datos).
- El usuario puede iniciar sesión con esa contraseña y luego usar "Cambiar contraseña" para establecer su propia contraseña.

Cómo probar localmente
1. Aplicar migraciones si es necesario:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Ejecutar el servidor:

```bash
python manage.py runserver
```

3. Flujo de prueba (ejemplos):
- Acceder a `/solicitar-cuenta/`, enviar una solicitud nueva.
- Como admin, ir a `/admin/solicitudes/`, abrir una solicitud y aprobarla: se creará un usuario con contraseña generada.
- En lista de catalogadores, usar el botón "Generar clave" para asignar/mostrar una contraseña temporal (el admin verá la clave en pantalla una vez).
- Como usuario, iniciar sesión con la contraseña temporal y acceder a "Mi perfil" → "Cambiar contraseña" para establecer su propia contraseña.

Notas y recomendaciones futuras
- Forzar cambio de contraseña en el primer inicio: actualmente no se fuerza; si quieres, puedo implementar un campo booleano (`must_change_password`) en `CustomUser` y una redirección en `CustomLoginView` para obligar al usuario a ir a `/perfil/password/` la primera vez.
- Envío de notificaciones por correo: ahora hay notificaciones internas; puedo añadir envío por email (SMTP) si lo deseas.
- Seguridad: la contraseña temporal se muestra UNA vez; para mayor seguridad se puede generar y enviar un enlace de restablecimiento en vez de mostrar la contraseña en pantalla.

Archivos clave para revisar rápidamente
- `usuarios/models.py`
- `usuarios/forms.py`
- `usuarios/views.py`
- `usuarios/urls.py`
- `usuarios/templates/usuarios/` (subcarpetas `solicitud/`, `admin/`, `perfil/`)
- `marc21_project/settings.py` (context processors)

Si quieres, puedo:
- Implementar la opción `must_change_password` para obligar al cambio en el primer login.
- Limpiar/remover las rutas/plantillas de restablecimiento por enlace si prefieres sólo la visualización de clave temporal.
- Añadir tests automatizados para los flujos principales.

---
Fecha: 24 de febrero de 2026
Generado por: asistente de desarrollo (cambios en el repo local)
