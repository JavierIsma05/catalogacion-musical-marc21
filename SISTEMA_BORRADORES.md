# Sistema de Borradores para Obras MARC21

## 📋 Descripción

Sistema completo de guardado automático y recuperación de borradores para el formulario de catalogación de obras MARC21. Permite a los usuarios guardar su progreso y recuperarlo posteriormente sin perder información.

## ✨ Características

### 🔄 Guardado Automático

-   **Autoguardado periódico**: Cada 60 segundos si hay cambios
-   **Guardado inteligente**: Espera 3 segundos de inactividad antes de guardar
-   **Indicador visual**: Muestra el estado del guardado en tiempo real

### 💾 Gestión de Borradores

-   **Verificación al inicio**: Detecta automáticamente si existe un borrador previo
-   **Recuperación de progreso**: Restaura el formulario desde la pestaña donde se quedó
-   **Eliminación automática**: Borra el borrador al publicar la obra
-   **Prevención de pérdida**: Alerta si intentas salir con cambios sin guardar

### 📊 Panel de Administración

-   **Lista completa**: Vista de todos los borradores con filtros
-   **Acciones en lote**: Eliminar borradores antiguos (>30 días)
-   **Limpieza automática**: Eliminar borradores sin título
-   **Indicadores visuales**: Antigüedad con colores (verde=hoy, naranja=<7 días, rojo=>7 días)

## 🏗️ Arquitectura

### Modelo de Base de Datos (`BorradorObra`)

```python
- id: Identificador único
- tipo_obra: Tipo de obra MARC21
- datos_formulario: JSON con todos los datos del formulario
- pestana_actual: Índice de la pestaña activa
- titulo_temporal: Título extraído del campo 245$a
- num_control_temporal: Número de control si existe
- tipo_registro: c=impreso, d=manuscrito
- nivel_bibliografico: a=parte, c=colección, m=monografía
- fecha_creacion: Timestamp de creación
- fecha_modificacion: Timestamp de última modificación
```

### API REST (Endpoints)

```
POST   /api/borradores/guardar/          - Guardar/actualizar borrador
POST   /api/borradores/autoguardar/      - Autoguardado (solo actualización)
GET    /api/borradores/verificar/        - Verificar si existe borrador
GET    /api/borradores/listar/           - Listar todos los borradores
GET    /api/borradores/<id>/             - Obtener borrador específico
DELETE /api/borradores/<id>/eliminar/    - Eliminar borrador
```

### JavaScript (`borrador-system.js`)

-   **Serialización automática**: Convierte FormData a JSON
-   **Detección de cambios**: Escucha eventos input/change
-   **Gestión de estado**: Controla hasUnsavedChanges y borradorId
-   **Notificaciones toast**: Feedback visual de todas las operaciones
-   **Atajos de teclado**: Alt+S para guardar (opcional)

## 🚀 Uso

### Para el Usuario Final

1. **Crear nueva obra**:

    - Ir a "Seleccionar Tipo de Obra"
    - Elegir tipo (manuscrito/impreso)
    - Si existe borrador previo, se mostrará diálogo de recuperación

2. **Durante la catalogación**:

    - El sistema guarda automáticamente cada 60 segundos
    - Indicador verde "✓ Guardado" aparece en esquina inferior izquierda
    - Cambios no guardados muestran "● Cambios sin guardar" en naranja

3. **Guardar manualmente**:

    - Hacer clic en botón "☁️ Guardar Borrador" (en primera pestaña)
    - O simplemente navegar entre pestañas (autoguarda)

4. **Recuperar borrador**:

    - Al volver al formulario, se ofrece automáticamente recuperar
    - Se restaura hasta la pestaña donde se quedó

5. **Finalizar**:
    - Hacer clic en "Publicar Obra" elimina el borrador automáticamente
    - "Guardar Borrador" mantiene el borrador para continuar después

### Para el Administrador

**Panel de Django Admin**:

```
/admin/catalogacion/borradorobra/
```

**Acciones disponibles**:

-   🗑️ Eliminar borradores > 30 días
-   🧹 Limpiar borradores sin título
-   Ver/editar datos de cualquier borrador
-   Filtrar por tipo de obra, fecha, etc.

## 📝 Flujo Técnico

### 1. Inicialización

```javascript
// Al cargar la página
verificarBorradorExistente()
  → API: GET /api/borradores/verificar/?tipo_obra=manuscrito_independiente
  → Si existe: mostrarDialogoRecuperarBorrador()
  → Usuario elige: recuperar o empezar nuevo
```

### 2. Guardado Manual

```javascript
// Usuario click en "Guardar Borrador"
guardarBorrador(false)
  → serializeFormData() - Convertir formulario a JSON
  → getTipoObra() - Detectar tipo
  → API: POST /api/borradores/guardar/
  → Respuesta: borradorId, fecha_modificacion
  → Actualizar UI: indicador verde
```

### 3. Autoguardado

```javascript
// Cada 60 segundos O 3 segundos después de cambio
guardarBorrador(true)
  → Verifica: hasUnsavedChanges && borradorId
  → API: POST /api/borradores/autoguardar/
  → Notificación toast pequeña
```

### 4. Recuperación

```javascript
// Usuario acepta recuperar borrador
cargarBorrador(id)
  → API: GET /api/borradores/{id}/
  → cargarDatosEnFormulario(datos)
  → switchTab(pestana_actual) - Ir a pestaña guardada
```

### 5. Publicación

```javascript
// Usuario click en "Publicar Obra"
form.submit()
  → Detectar action="publish"
  → API: DELETE /api/borradores/{id}/eliminar/
  → Enviar formulario a Django
```

## 🔧 Configuración

### Constantes Personalizables

```javascript
// En borrador-system.js
const AUTOSAVE_INTERVAL = 60000; // 60 seg (modificar si deseas)
const MIN_CHANGE_DELAY = 3000; // 3 seg después de último cambio
```

### Limpieza Automática

Por defecto, el admin ofrece eliminar borradores > 30 días. Para automatizar:

```python
# En settings.py o tarea programada
from catalogacion.models import BorradorObra
from datetime import timedelta
from django.utils import timezone

# Eliminar borradores antiguos
fecha_limite = timezone.now() - timedelta(days=30)
BorradorObra.objects.filter(fecha_modificacion__lt=fecha_limite).delete()
```

## 🎨 Personalización de UI

### Notificaciones Toast

Los colores se definen en `borrador-system.js`:

```javascript
const colores = {
    success: "#27AE60", // Verde
    error: "#E74C3C", // Rojo
    info: "#3498DB", // Azul
    warning: "#F39C12", // Naranja
};
```

### Indicador de Guardado

Posición y estilo en `actualizarIndicadorGuardado()`:

```javascript
indicador.style.cssText = `
    position: fixed;
    bottom: 20px;    // Cambiar a top: 20px si prefieres arriba
    left: 20px;      // Cambiar a right: 20px para mover a derecha
    ...
`;
```

## 🐛 Resolución de Problemas

### Borrador no se guarda

1. Verificar consola del navegador (F12) para errores
2. Verificar que CSRF token esté presente en el formulario
3. Verificar conexión a base de datos

### Borrador no se recupera

1. Verificar que `tipo_obra` coincida exactamente
2. Verificar en admin si el borrador existe
3. Ver logs de Django para errores de API

### Datos no se cargan correctamente

1. Verificar que nombres de campos coincidan entre HTML y datos guardados
2. Revisar formsets - deben usar prefijos correctos
3. Verificar campos dinámicos (autocomplete, select2)

## 📊 Estadísticas y Monitoreo

### Consultas útiles en Django Shell

```python
# Total de borradores
BorradorObra.objects.count()

# Borradores por tipo
BorradorObra.objects.values('tipo_obra').annotate(total=Count('id'))

# Borradores activos (últimas 24h)
from datetime import timedelta
from django.utils import timezone
ayer = timezone.now() - timedelta(days=1)
BorradorObra.objects.filter(fecha_modificacion__gte=ayer).count()

# Borradores más antiguos
BorradorObra.objects.order_by('fecha_modificacion')[:10]
```

## ✅ Testing

### Pruebas manuales

1. ✓ Crear borrador - completar algunos campos y guardar
2. ✓ Cerrar navegador y volver - verificar recuperación
3. ✓ Autoguardado - esperar 60 segundos con cambios
4. ✓ Navegación - cambiar pestañas sin perder datos
5. ✓ Publicar - verificar que borrador se elimina
6. ✓ Pérdida de datos - intentar salir con cambios

### Pruebas de API (con curl o Postman)

```bash
# Guardar borrador
curl -X POST http://localhost:8000/catalogacion/api/borradores/guardar/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_obra":"manuscrito_independiente","datos_formulario":{},"pestana_actual":0}'

# Listar borradores
curl http://localhost:8000/catalogacion/api/borradores/listar/

# Obtener borrador
curl http://localhost:8000/catalogacion/api/borradores/1/

# Eliminar borrador
curl -X DELETE http://localhost:8000/catalogacion/api/borradores/1/eliminar/
```

## 📚 Referencias

-   Documentación Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
-   JSONField: https://docs.djangoproject.com/en/stable/ref/models/fields/#jsonfield
-   Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
-   FormData: https://developer.mozilla.org/en-US/docs/Web/API/FormData

## 🔄 Actualizaciones Futuras

### Mejoras Planeadas

-   [ ] Versionado de borradores (múltiples versiones por obra)
-   [ ] Comparación visual de cambios
-   [ ] Exportar borrador a JSON
-   [ ] Importar borrador desde JSON
-   [ ] Historial de autoguardados
-   [ ] Sincronización multi-dispositivo
-   [ ] Compresión de datos grandes

---

**Autor**: Sistema de Catalogación MARC21  
**Versión**: 1.0.0  
**Fecha**: Noviembre 2025
