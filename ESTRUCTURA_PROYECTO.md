# 🗂️ Estructura del Proyecto - Catalogación Musical MARC21

## 📁 Vista General

```
catologacion_musical/
│
├── 📄 manage.py                          # Django management script
├── 📄 db.sqlite3                         # Base de datos SQLite
├── 📄 README.md                          # Documentación del proyecto
│
├── 📘 REORGANIZACION_COMPLETADA.md      # ✅ Resumen ejecutivo
├── 📘 CHECKLIST_DESARROLLO.md           # ✅ Plan de desarrollo
├── 📘 PROXIMOS_PASOS.md                 # ✅ Guía de continuación
├── 📘 PRUEBA_CAMPO_300.md               # ✅ Guía de usuario campo 300
├── 📘 IMPLEMENTACION_300.md             # ✅ Detalles técnicos campo 300
├── 📘 GUIA_VISUAL_300.md                # ✅ Guía visual campo 300
├── 📘 ESTRUCTURA_PROYECTO.md            # ✅ Este archivo
│
├── 📂 marc21_project/                    # Configuración Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                       # ⚙️ Configuración principal
│   ├── urls.py                           # 🔗 URLs raíz
│   └── wsgi.py
│
├── 📂 catalogacion/                      # 🎵 App principal
│   │
│   ├── 📄 __init__.py
│   ├── 📄 admin.py                       # Admin de Django
│   ├── 📄 apps.py                        # Configuración de app
│   ├── 📄 forms.py                       # 📝 Formularios y formsets
│   ├── 📄 urls.py                        # 🔗 URLs de catalogacion
│   ├── 📄 tests.py                       # 🧪 Tests (pendiente)
│   │
│   ├── 📂 models/                        # 💾 Modelos organizados por bloques
│   │   ├── __init__.py                   # Exporta todos los modelos
│   │   ├── obra_general.py               # ✅ Modelo principal ObraGeneral
│   │   ├── autoridades.py                # ✅ Compositor, Medio físico
│   │   ├── bloque_0xx.py                 # ✅ ISBN, ISMN, Incipit, Lenguas, Países
│   │   ├── bloque_1xx.py                 # ✅ Funciones, Atribuciones, Títulos uniformes
│   │   ├── bloque_2xx.py                 # ✅ Títulos alt., Edición, Producción/Pub
│   │   ├── bloque_3xx.py                 # ✅ Descripción física, Características, Medios
│   │   └── bloque_4xx.py                 # ✅ Series
│   │
│   ├── 📂 views/                         # 👁️ Vistas organizadas por bloques MARC
│   │   ├── __init__.py                   # ✅ Exporta todas las vistas
│   │   ├── README.md                     # ✅ Documentación completa (350+ líneas)
│   │   ├── views_base.py                 # ✅ 7 funciones (navegación)
│   │   ├── views_autoridades.py          # ✅ 1 función (JSON para Select2)
│   │   ├── views_0xx.py                  # ✅ 6 funciones (campos de control)
│   │   ├── views_1xx.py                  # ✅ 5 funciones (puntos de acceso)
│   │   ├── views_2xx.py                  # ✅ 4 funciones (títulos/publicación)
│   │   ├── views_3xx.py                  # 🟡 6 funciones (4 TODOs pendientes)
│   │   ├── views_4xx.py                  # 🟡 2 funciones (1 TODO pendiente)
│   │   └── views_pruebas.py              # ✅ 2 funciones (testing campo 300)
│   │
│   ├── 📂 templates/                     # 🎨 Templates HTML
│   │   ├── base.html                     # ✅ Template base con Bootstrap 5
│   │   ├── navbar.html                   # ✅ Navegación principal
│   │   ├── index.html                    # ✅ Página de inicio
│   │   ├── plantillas.html               # ✅ Selector de plantillas
│   │   ├── crear_obra.html               # 🚧 Formulario de creación (en desarrollo)
│   │   │
│   │   └── 📂 catalogacion/
│   │       ├── 📂 partials/
│   │       │   ├── _campo_300_item.html         # ✅ Partial para item existente
│   │       │   └── _campo_300_template.html     # ✅ Partial para nuevo item
│   │       │
│   │       ├── prueba_campo_300.html     # ✅ Test campo 300 (FUNCIONAL)
│   │       │
│   │       ├── 📂 ColeccionImpresa/
│   │       │   ├── col_imp.html
│   │       │   └── obra_in_imp.html
│   │       │
│   │       ├── 📂 ColeccionManuscrita/
│   │       │   ├── col_man.html
│   │       │   └── obra_in_man.html
│   │       │
│   │       └── 📂 ObraGeneral/
│   │           └── obra_general.html
│   │
│   ├── 📂 static/catalogacion/           # 🎨 Archivos estáticos
│   │   ├── 📂 css/
│   │   │   └── styles.css                # ✅ Estilos personalizados
│   │   ├── 📂 js/
│   │   │   └── tabs.js                   # ✅ JavaScript para tabs
│   │   └── 📂 img/
│   │
│   └── 📂 migrations/                    # 🔄 Migraciones de base de datos
│       ├── __init__.py
│       ├── 0001_initial.py
│       ├── 0002_...py
│       └── ... (9 migraciones en total)
│
├── 📂 media/                             # 📸 Archivos subidos por usuarios
│   ├── 📂 documentos/
│   └── 📂 portadas/
│
└── 📂 .venv/                             # 🐍 Entorno virtual Python
    ├── bin/
    ├── lib/
    └── ...
```

---

## 📊 Estadísticas del Proyecto

### Líneas de Código

| Componente        | Archivos | Líneas Aprox. | Estado     |
| ----------------- | -------- | ------------- | ---------- |
| **Modelos**       | 7        | ~1500         | ✅ 100%    |
| **Vistas**        | 9        | ~1310         | 🟡 85%     |
| **Forms**         | 1        | ~300          | ✅ 90%     |
| **Templates**     | 15+      | ~800          | 🔴 40%     |
| **JavaScript**    | 2        | ~200          | 🔴 30%     |
| **CSS**           | 1        | ~100          | 🟡 50%     |
| **Documentación** | 7        | ~2000         | ✅ 95%     |
| **TOTAL**         | **42+**  | **~6210**     | **🟡 70%** |

### Modelos por Bloque MARC

| Bloque            | Modelos | Estado      |
| ----------------- | ------- | ----------- |
| **Obra General**  | 1       | ✅ Completo |
| **Autoridades**   | 2       | ✅ Completo |
| **0XX (Control)** | 5       | ✅ Completo |
| **1XX (Acceso)**  | 9       | ✅ Completo |
| **2XX (Títulos)** | 3       | ✅ Completo |
| **3XX (Física)**  | 4       | ✅ Completo |
| **4XX (Series)**  | 1       | ✅ Completo |
| **TOTAL**         | **25**  | **✅ 100%** |

### Vistas por Bloque MARC

| Bloque          | Vistas | Implementadas | Pendientes | %          |
| --------------- | ------ | ------------- | ---------- | ---------- |
| **Base**        | 7      | 7             | 0          | ✅ 100%    |
| **Autoridades** | 1      | 1             | 0          | ✅ 100%    |
| **0XX**         | 6      | 6             | 0          | ✅ 100%    |
| **1XX**         | 5      | 5             | 0          | ✅ 100%    |
| **2XX**         | 4      | 4             | 0          | ✅ 100%    |
| **3XX**         | 6      | 2             | 4          | 🔴 33%     |
| **4XX**         | 2      | 1             | 1          | 🟡 50%     |
| **Pruebas**     | 2      | 2             | 0          | ✅ 100%    |
| **TOTAL**       | **33** | **28**        | **5**      | **🟡 85%** |

---

## 🎯 Campos MARC21 Implementados

### ✅ Campos Completamente Funcionales

#### Bloque 0XX - Campos de Control

-   ✅ **020** - ISBN (International Standard Book Number)
-   ✅ **024** - ISMN (International Standard Music Number)
-   ✅ **031** - Incipit Musical
-   ✅ **041** - Código de Lengua
-   ✅ **044** - Código de País de Entidad Productora

#### Bloque 1XX - Puntos de Acceso Principal

-   ✅ **100** - Encabezamiento Principal - Compositor
-   ✅ **110** - Función del Compositor
-   ✅ **111** - Atribución del Compositor
-   ✅ **130** - Encabezamiento - Título Uniforme
    -   Forma musical
    -   Nombre de parte
    -   Número de parte
    -   Medio de interpretación
-   ✅ **240** - Título Uniforme
    -   Forma musical
    -   Nombre de parte
    -   Número de parte
    -   Medio de interpretación

#### Bloque 2XX - Títulos y Mención de Responsabilidad

-   ✅ **245** - Mención de Título (en ObraGeneral)
    -   Título principal
    -   Subtítulo
    -   Mención de responsabilidad
-   ✅ **246** - Forma Variante del Título / Título Alternativo
-   ✅ **250** - Mención de Edición
-   ✅ **264** - Producción, Publicación, Distribución, etc.

#### Bloque 3XX - Descripción Física

-   ✅ **300** - Descripción Física **← PATRÓN DE REFERENCIA**
    -   $a Extension (R)
    -   $b Características (NR)
    -   $c Dimensión (R)
    -   $e Material acompañante (NR)

### 🟡 Campos Parcialmente Implementados

#### Bloque 3XX - Descripción Física

-   🔴 **348** - Características de la Música Notada (TODO)
-   🔴 **382** - Medio de Interpretación (TODO)
-   🔴 **383** - Designación Numérica para Obras Musicales (TODO)
-   ✅ **384** - Tonalidad (en ObraGeneral)

#### Bloque 4XX - Mención de Serie

-   🔴 **490** - Mención de Serie (TODO)

---

## 🗺️ Mapa de Archivos Clave

### 📝 Configuración

```
marc21_project/settings.py
├── INSTALLED_APPS
│   └── 'catalogacion'
├── DATABASES
│   └── SQLite (db.sqlite3)
├── STATIC_URL
│   └── '/static/'
└── MEDIA_URL
    └── '/media/'
```

### 🔗 Routing

```
marc21_project/urls.py
└── include('catalogacion.urls')
    │
    └── catalogacion/urls.py
        ├── / → index
        ├── /plantillas/ → plantillas
        ├── /crear_obra/ → crear_obra
        ├── /coleccion_manuscrita/ → coleccion_manuscrita
        ├── /coleccion_impresa/ → coleccion_impresa
        ├── /api/autoridades/ → get_autoridades_json
        └── /prueba/campo-300/ → prueba_campo_300 ✅
```

### 💾 Modelos → Vistas → Templates

```
CAMPO 300 (Descripción Física) - FLUJO COMPLETO ✅
│
├── 📄 models/bloque_3xx.py
│   └── class DescripcionFisica(models.Model)
│       ├── obra (FK → ObraGeneral)
│       ├── extension (TextField)        # Repetible
│       ├── caracteristicas (CharField)  # No repetible
│       ├── dimension (TextField)        # Repetible
│       └── material_acompañante (CharField)  # No repetible
│
├── 📄 views/views_pruebas.py
│   └── def prueba_campo_300(request, obra_id=None):
│       ├── GET: Renderiza formulario
│       └── POST: Procesa y guarda datos
│
└── 📄 templates/catalogacion/prueba_campo_300.html
    ├── Formulario con Bootstrap 5
    ├── JavaScript para campos dinámicos
    └── Partials:
        ├── _campo_300_item.html (items existentes)
        └── _campo_300_template.html (template para nuevos)
```

---

## 🧩 Dependencias del Proyecto

### Python Packages (requirements.txt estimado)

```txt
Django==5.2.7
Pillow==10.x.x          # Para manejo de imágenes
psycopg2-binary==2.9.x  # PostgreSQL (futuro)
python-decouple==3.8    # Variables de entorno (futuro)
```

### Frontend Dependencies

```html
<!-- Desde CDN -->
Bootstrap 5.3.0 Bootstrap Icons 1.11.0
```

---

## 🔄 Flujo de Datos

### Creación de Obra con Campo 300

```
1. Usuario accede a /prueba/campo-300/
   ↓
2. Vista: prueba_campo_300() [GET]
   ├── Crea obra temporal si no existe
   ├── Obtiene campos 300 existentes
   └── Renderiza template con datos
   ↓
3. Template muestra formulario
   ├── Campos existentes (editable)
   └── Botón "Agregar Campo 300"
   ↓
4. Usuario agrega/edita campos
   ├── JavaScript maneja formulario dinámico
   ├── Agrega subcampos repetibles
   └── Marca campos para eliminar
   ↓
5. Usuario envía formulario [POST]
   ↓
6. Vista: prueba_campo_300() [POST]
   ├── Inicia Transaction.atomic()
   ├── Procesa cada campo 300
   │   ├── Elimina marcados con DELETE
   │   ├── Actualiza existentes
   │   └── Crea nuevos
   ├── Guarda todos los cambios
   └── Commit o Rollback
   ↓
7. Redirect a misma página con datos actualizados
```

---

## 📋 Convenciones del Proyecto

### Nombres de Archivos

```
Modelos:     bloque_Nxx.py (N = primer dígito del bloque MARC)
Vistas:      views_Nxx.py (N = primer dígito del bloque MARC)
Templates:   catalogacion/Nxx/nombre_campo_NNN.html
URLs:        /bloque-N/campo-NNN/
```

### Nombres de Funciones

```python
# Vistas
def gestionar_NOMBRE_CAMPO_NNN(request, obra_id=None):
    """
    Gestiona el campo MARC NNN - NOMBRE DEL CAMPO.

    Args:
        request: HttpRequest
        obra_id: ID de la obra (opcional)

    Returns:
        HttpResponse
    """
    pass

# Listar campos de un bloque
def listar_campos_Nxx(request, obra_id):
    """Lista todos los campos del bloque Nxx para una obra."""
    pass
```

### Nombres de Templates

```
Gestionar campo:     catalogacion/Nxx/gestionar_NOMBRE_NNN.html
Listar campos:       catalogacion/Nxx/listar_campos_Nxx.html
Partials (items):    catalogacion/partials/_campo_NNN_item.html
Partials (template): catalogacion/partials/_campo_NNN_template.html
```

### Nombres de URLs

```python
path('bloque-N/campo-NNN/', gestionar_campo_NNN, name='gestionar_campo_NNN')
path('bloque-N/', listar_campos_Nxx, name='listar_campos_Nxx')
```

---

## 🎨 Estructura de Templates

### Template Base Hierarchy

```
base.html (Bootstrap 5 + Bootstrap Icons)
│
├── navbar.html (Navegación)
│
├── index.html (Página inicio)
├── plantillas.html (Selector)
├── crear_obra.html (Formulario obra)
│
└── catalogacion/
    ├── prueba_campo_300.html ✅
    │   ├── extends base.html
    │   ├── include partials/_campo_300_item.html
    │   └── include partials/_campo_300_template.html
    │
    ├── 0xx/
    │   └── (pendiente)
    ├── 1xx/
    │   └── (pendiente)
    ├── 2xx/
    │   └── (pendiente)
    ├── 3xx/
    │   └── gestionar_descripcion_fisica_300.html (mover de prueba)
    └── 4xx/
        └── (pendiente)
```

---

## 🚀 Estado de Deployment

### Desarrollo ✅

```
✅ Servidor local funcionando
✅ SQLite como base de datos
✅ DEBUG = True
✅ Archivos estáticos servidos por Django
✅ Media files en /media/
```

### Producción 🔴 (Pendiente)

```
🔴 Configurar PostgreSQL
🔴 DEBUG = False
🔴 ALLOWED_HOSTS configurado
🔴 Archivos estáticos con WhiteNoise
🔴 Media files en storage externo
🔴 Variables de entorno con python-decouple
🔴 Gunicorn/uWSGI como servidor
🔴 Nginx como reverse proxy
```

---

## 📈 Progreso Visual

```
MODELOS          [████████████████████] 100%  ✅
VISTAS           [████████████████▒▒▒▒] 85%   🟡
FORMS            [██████████████████▒▒] 90%   ✅
TEMPLATES        [████████▒▒▒▒▒▒▒▒▒▒▒▒] 40%   🔴
JAVASCRIPT       [██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒] 30%   🔴
CSS              [██████████▒▒▒▒▒▒▒▒▒▒] 50%   🟡
DOCUMENTACIÓN    [███████████████████▒] 95%   ✅
TESTS            [▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒] 0%    🔴
─────────────────────────────────────────────
TOTAL PROYECTO   [██████████████▒▒▒▒▒▒] 70%   🟡
```

---

## 🎯 Siguientes Archivos a Crear

### Alta Prioridad

1. `catalogacion/views/views_3xx.py` → Completar TODOs
2. `catalogacion/views/views_4xx.py` → Completar TODO
3. `catalogacion/templates/catalogacion/obra_detalle.html`
4. `catalogacion/templates/catalogacion/3xx/gestionar_caracteristicas_348.html`
5. `catalogacion/templates/catalogacion/3xx/gestionar_medio_382.html`

### Media Prioridad

6. `catalogacion/static/catalogacion/js/campos-repetibles.js`
7. `catalogacion/static/catalogacion/js/validaciones.js`
8. `catalogacion/templates/catalogacion/partials/_campo_repetible.html`

### Baja Prioridad

9. `catalogacion/tests/test_models.py`
10. `catalogacion/tests/test_views.py`
11. `docs/manual_usuario.md`

---

## 📝 Changelog Reciente

### [01/11/2025] - Reorganización Mayor

**Agregado:**

-   ✅ Directorio `catalogacion/views/` con 9 archivos modulares
-   ✅ 7 archivos de documentación Markdown
-   ✅ Vista funcional de prueba para campo 300
-   ✅ Patrón de referencia para campos repetibles anidados

**Modificado:**

-   ✅ `catalogacion/urls.py` - Actualizado para nueva estructura
-   ✅ `catalogacion/templates/navbar.html` - Corregida URL incorrecta
-   ✅ `catalogacion/forms.py` - Corregidos errores de sintaxis

**Eliminado:**

-   ❌ `catalogacion/views.py` (archivo monolítico original)
-   ❌ `catalogacion/views_prueba_300.py` (duplicado)

**Estado:**

-   ✅ Servidor funcionando sin errores
-   ✅ Estructura escalable establecida
-   🟡 5 TODOs pendientes (menor impacto)

---

## 🏆 Logros del Proyecto

✅ **Estructura sólida** - Organización modular por bloques MARC21  
✅ **Patrón establecido** - Campo 300 como referencia funcional  
✅ **Documentación completa** - 2000+ líneas de docs técnicas y usuario  
✅ **Código limpio** - Eliminados duplicados y archivos legacy  
✅ **Base escalable** - Fácil agregar nuevos campos siguiendo patrón

---

**Última Actualización:** 01 de Noviembre de 2025  
**Versión Django:** 5.2.7  
**Versión Python:** 3.12.7  
**Estado del Servidor:** ✅ Funcionando en http://127.0.0.1:8000/
