# 📁 Organización de Vistas - Sistema MARC21 Musical

## 🎯 Estructura de Carpeta `views/`

Las vistas se han reorganizado por **bloques MARC21 bibliográficos** para mejor mantenimiento y escalabilidad.

```
catalogacion/
├── views/
│   ├── __init__.py                  # Exporta todas las vistas
│   ├── README.md                    # Este archivo (documentación)
│   ├── views_base.py                # Vistas generales de navegación
│   ├── views_autoridades.py         # Endpoints JSON para autocompletado
│   ├── views_0xx.py                 # Bloque 0XX - Campos de control
│   ├── views_1xx.py                 # Bloque 1XX - Puntos de acceso principal
│   ├── views_2xx.py                 # Bloque 2XX - Títulos y publicación
│   ├── views_3xx.py                 # Bloque 3XX - Descripción física
│   ├── views_4xx.py                 # Bloque 4XX - Series
│   └── views_pruebas.py             # Testing y desarrollo
├── urls.py                          # Rutas URL
├── models/                          # Modelos organizados por bloques
└── forms.py                         # Formularios
```

## � Reorganización Reciente

### **Cambio principal:** Separación de responsabilidades por bloques

**Antes:**

-   ❌ Todas las funciones de procesamiento en `views_base.py` (608 líneas)
-   ❌ Difícil mantenimiento y escalabilidad
-   ❌ Violación del principio de responsabilidad única

**Después:**

-   ✅ `views_base.py`: Solo navegación general (158 líneas, 74% reducción)
-   ✅ `views_0xx.py`: Procesamiento completo del bloque 0XX (~490 líneas)
-   ✅ `views_1xx.py`: Procesamiento completo del bloque 1XX (~490 líneas)
-   ✅ Patrón claro para agregar bloques 2XX, 3XX, 4XX

## �📋 Descripción de Archivos

### `__init__.py`

**Propósito:** Exportar todas las vistas públicas

**Exporta:**

```python
# Vistas de navegación
from .views_base import index, plantillas, crear_obra, listar_obras

# Funciones de procesamiento 0XX
from .views_0xx import (
    procesar_isbn,
    procesar_ismn,
    procesar_numero_editor,
    procesar_incipit,
    procesar_codigo_lengua,
    procesar_codigo_pais,
)

# Funciones de procesamiento 1XX
from .views_1xx import (
    procesar_compositor,
    procesar_titulo_uniforme_130,
    procesar_subcampos_130,
    procesar_titulo_uniforme_240,
    procesar_subcampos_240,
)
```

### `views_base.py`

**Responsabilidad:** Navegación general del sistema

**Vistas principales:**

-   `index()` - Página principal
-   `plantillas()` - Plantillas de catalogación
-   `crear_obra()` - Formulario principal (orquesta el guardado)
-   `listar_obras()` - Listado de obras catalogadas
-   `coleccion_manuscrita()`, `coleccion_impresa()` - Gestión de colecciones

**Flujo de crear_obra():**

```python
def crear_obra(request):
    with transaction.atomic():
        # 1. Crear obra con cabecera
        obra = ObraGeneral()
        obra.save()

        # 2. Procesar bloque 0XX
        procesar_isbn(request, obra)
        procesar_ismn(request, obra)
        procesar_numero_editor(request, obra)
        procesar_incipit(request, obra)
        procesar_codigo_lengua(request, obra)
        procesar_codigo_pais(request, obra)

        # 3. Procesar bloque 1XX
        procesar_compositor(request, obra)
        procesar_titulo_uniforme_130(request, obra)
        procesar_titulo_uniforme_240(request, obra)

        # 4. Generar clasificación automática
        obra.generar_clasificacion_092()
        obra.save()
```

### `views_autoridades.py`

**Responsabilidad:** Endpoints JSON para autocompletado

**Función principal:**

```python
def get_autoridades_json(request, tipo):
    """
    Endpoint para Select2/autocompletado

    Tipos soportados:
    - 'compositor' -> AutoridadPersona
    - 'titulo' -> AutoridadTituloUniforme
    - 'forma' -> AutoridadFormaMusical
    """
```

**Uso en JavaScript:**

```javascript
$("#compositor").select2({
    ajax: {
        url: "/api/autoridades/?tipo=compositor",
        dataType: "json",
    },
});
```

### `views_0xx.py`

**Responsabilidad:** Bloque 0XX - Campos de Control

**Campos manejados:**

-   020 - ISBN (repetible)
-   024 - ISMN (repetible)
-   028 - Número de Editor (repetible, con indicadores)
-   031 - Incipit Musical (repetible, con URLs anidadas)
-   040 - Fuente de Catalogación (no repetible)
-   041 - Código de Lengua (repetible, con idiomas anidados)
-   044 - Código de País (repetible)
-   092 - Clasificación Local (autogenerada)

**Funciones de procesamiento masivo (6):**

```python
def procesar_isbn(request, obra):
    """Procesa múltiples ISBN desde formulario principal"""

def procesar_ismn(request, obra):
    """Procesa múltiples ISMN desde formulario principal"""

def procesar_numero_editor(request, obra):
    """Procesa múltiples números de editor con indicadores"""

def procesar_incipit(request, obra):
    """Procesa incipits musicales con URLs anidadas
    Estructura: incipit_a_0, incipit_b_0, incipit_u_0_0, incipit_u_0_1"""

def procesar_codigo_lengua(request, obra):
    """Procesa códigos de lengua con idiomas anidados
    Estructura: codigo_lengua_ind1_0, codigo_lengua_a_0_0, codigo_lengua_a_0_1"""

def procesar_codigo_pais(request, obra):
    """Procesa múltiples códigos de país"""
```

**Vistas individuales:**

-   `crear_isbn(request, obra_id)` - Crear un ISBN individual
-   `crear_ismn(request, obra_id)` - Crear un ISMN individual
-   `crear_numero_editor(request, obra_id)` - Crear número de editor
-   `crear_incipit_musical(request, obra_id)` - Crear incipit con URLs
-   `crear_codigo_lengua(request, obra_id)` - Crear código de lengua con idiomas
-   `listar_campos_0xx(request, obra_id)` - Vista resumen del bloque

**Modelos procesados:**

-   `ISBN`, `ISMN`, `NumeroEditor`
-   `IncipitMusical`, `IncipitURL` (relación 1-N)
-   `CodigoLengua`, `IdiomaObra` (relación 1-N)
-   `CodigoPaisEntidad`

### `views_1xx.py`

**Responsabilidad:** Bloque 1XX - Puntos de Acceso Principal

**Campos manejados:**

-   100 - Compositor ($e funciones, $j atribuciones) - repetibles
-   130 - Título Uniforme ($k forma, $m medio, $n número, $p nombre) - solo si NO hay compositor
-   240 - Título Uniforme con Compositor (mismos subcampos que 130) - solo si HAY compositor

**Funciones de procesamiento masivo (5):**

```python
def procesar_compositor(request, obra):
    """
    Procesa compositor (100) con funciones y atribuciones

    Maneja:
    - AutoridadPersona (get_or_create)
    - FuncionCompositor (repetible)
    - AtribucionCompositor (repetible)
    """

def procesar_titulo_uniforme_130(request, obra):
    """
    Procesa título uniforme 130 (solo si NO hay compositor)

    Maneja:
    - AutoridadTituloUniforme (get_or_create)
    - Llamada a procesar_subcampos_130()
    """

def procesar_subcampos_130(request, obra):
    """
    Procesa subcampos repetibles del 130

    Maneja:
    - $k Forma130 -> ForeignKey a AutoridadFormaMusical
    - $m MedioInterpretacion130
    - $n NumeroParteSección130
    - $p NombreParteSección130
    """

def procesar_titulo_uniforme_240(request, obra):
    """
    Procesa título uniforme 240 (solo si HAY compositor)

    Maneja:
    - AutoridadTituloUniforme (get_or_create)
    - Llamada a procesar_subcampos_240()
    """

def procesar_subcampos_240(request, obra):
    """
    Procesa subcampos repetibles del 240

    Maneja:
    - $k Forma240 -> CharField con choices (FORMAS_MUSICALES)
    - $m MedioInterpretacion240
    - $n NumeroParteSección240
    - $p NombreParteSección240
    """
```

**Vistas individuales:**

-   `crear_compositor(request, obra_id)` - Crear compositor con funciones
-   `crear_titulo_uniforme_130(request, obra_id)` - Crear título uniforme 130
-   `crear_titulo_uniforme_240(request, obra_id)` - Crear título uniforme 240
-   `listar_campos_1xx(request, obra_id)` - Vista resumen del bloque

**Modelos procesados:**

-   `FuncionCompositor`, `AtribucionCompositor`
-   `Forma130`, `MedioInterpretacion130`, `NumeroParteSección130`, `NombreParteSección130`
-   `Forma240`, `MedioInterpretacion240`, `NumeroParteSección240`, `NombreParteSección240`

**Autoridades utilizadas:**

-   `AutoridadPersona` (compositor)
-   `AutoridadTituloUniforme` (títulos uniformes 130/240)
-   `AutoridadFormaMusical` (formas musicales en 130)

**Diferencia 130 vs 240:**

-   **130:** Se usa cuando NO hay compositor (punto de acceso principal)
-   **240:** Se usa cuando HAY compositor (punto de acceso secundario)
-   **Forma $k:** En 130 usa AutoridadFormaMusical (FK), en 240 usa choices directas

**Patrón**: Campos no repetibles con subcampos repetibles

### `views_1xx.py`

**Bloque MARC**: 1XX - Puntos de Acceso Principal

**Campos manejados**:

-   `100 $e` - Función del compositor
-   `100 $j` - Atribución del compositor
-   `130` - Título uniforme principal (con $r, $m, $n, $p)
-   `240` - Título uniforme (con $r, $m, $n, $p)

**Vistas**:

-   `gestionar_funciones_compositor(request, obra_id)`
-   `gestionar_atribuciones_compositor(request, obra_id)`
-   `gestionar_titulo_uniforme_130(request, obra_id)`
-   `gestionar_titulo_uniforme_240(request, obra_id)`
-   `listar_campos_1xx(request, obra_id)`

**Patrón**: Campos repetibles con múltiples subcampos repetibles

### `views_2xx.py`

**Bloque MARC**: 2XX - Títulos y Publicación

**Campos manejados**:

-   `245` - Título principal (en modelo ObraGeneral)
-   `246` - Título alternativo
-   `250` - Mención de edición
-   `264` - Producción/publicación

**Vistas**:

-   `gestionar_titulos_alternativos(request, obra_id)`
-   `gestionar_ediciones(request, obra_id)`
-   `gestionar_produccion_publicacion(request, obra_id)`
-   `listar_campos_2xx(request, obra_id)`

**Patrón**: Campos repetibles simples

### `views_3xx.py` ⭐

**Bloque MARC**: 3XX - Descripción Física

**Campos manejados**:

-   `300` - Descripción física (con $a, $b, $c, $e)
-   `340` - Medio físico
-   `348` - Características de música notada
-   `382` - Medio de interpretación
-   `383` - Designación numérica
-   `384` - Tonalidad

**Vistas**:

-   `gestionar_descripcion_fisica(request, obra_id)` ⭐ **PATRÓN DE REFERENCIA**
-   `gestionar_medio_fisico(request, obra_id)`
-   `gestionar_caracteristicas_musica_notada(request, obra_id)`
-   `gestionar_medio_interpretacion_382(request, obra_id)`
-   `gestionar_designacion_numerica_383(request, obra_id)`
-   `listar_campos_3xx(request, obra_id)`

**⭐ Patrón Especial**: Campos repetibles con subcampos repetibles anidados

**Estructura del Campo 300**:

```
Campo 300 (R)
├── $a Extensión (R)
├── $b Características (NR)
├── $c Dimensión (R)
└── $e Material acompañante (NR)
```

### `views_4xx.py`

**Bloque MARC**: 4XX - Series

**Campos manejados**:

-   `490` - Mención de serie (con títulos y volúmenes)

**Vistas**:

-   `gestionar_mencion_serie_490(request, obra_id)`
-   `listar_campos_4xx(request, obra_id)`

**Patrón**: Campos repetibles con subcampos anidados

### `views_pruebas.py`

**Bloque**: Testing y Desarrollo

**Vistas**:

-   `prueba_campo_300(request, obra_id=None)` - Prueba de campo 300
-   `limpiar_prueba_300(request)` - Limpieza de datos de prueba

**Propósito**:

-   Demostrar patrones de implementación
-   Testing de funcionalidades
-   Datos de ejemplo

## 🎨 Patrón de Implementación

### Patrón Base (Campos Repetibles Simples)

```python
def gestionar_campo_xxx(request, obra_id):
    """
    Gestionar Campo XXX

    Campo XXX - Descripción (Repetible)
    """
    obra = get_object_or_404(ObraGeneral, pk=obra_id)

    if request.method == 'POST':
        formset = CampoXXXFormSet(request.POST, instance=obra)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    formset.save()
                    messages.success(request, '✅ Guardado correctamente')
                    return redirect('detalle_obra', obra_id=obra_id)
            except Exception as e:
                messages.error(request, f'❌ Error: {str(e)}')
    else:
        formset = CampoXXXFormSet(instance=obra)

    contexto = {
        'obra': obra,
        'formset': formset,
    }
    return render(request, 'catalogacion/xxx/template.html', contexto)
```

### Patrón Avanzado (Campos Repetibles con Subcampos Repetibles)

Ver `views_3xx.py` → `gestionar_descripcion_fisica()`

**Características**:

-   ✅ Procesamiento manual de POST
-   ✅ Campos anidados múltiples niveles
-   ✅ Manejo de DELETE para eliminación
-   ✅ Transaction.atomic() para integridad
-   ✅ Preparación de datos estructurados para template
-   ✅ Mensajes de éxito/error

**Aplicable a**:

-   Campo 300 (Descripción física)
-   Campo 031 (Íncipit con URLs)
-   Campo 041 (Lengua con idiomas)
-   Campo 382 (Medio de interpretación)
-   Campo 383 (Designación numérica)
-   Campo 490 (Series)

## 🔄 Migración desde Archivos Anteriores

### Archivos Deprecados

-   ❌ `views.py` (raíz) → Dividido en `views/*.py`
-   ❌ `views_prueba_300.py` → Movido a `views/views_pruebas.py`

### Cambios en Imports

**Antes**:

```python
from catalogacion import views
views.index(request)
```

**Ahora**:

```python
from catalogacion.views import index
index(request)
```

O seguir usando:

```python
from catalogacion import views
views.index(request)  # Sigue funcionando gracias a __init__.py
```

## 📊 Estadísticas

-   **Total de archivos**: 9
-   **Total de vistas**: 35+
-   **Bloques MARC cubiertos**: 0XX, 1XX, 2XX, 3XX, 4XX
-   **Patrón de referencia**: `views_3xx.py::gestionar_descripcion_fisica()`

## 🚀 Próximos Pasos

1. **Implementar vistas faltantes**:

    - Completar TODOs en `views_3xx.py`
    - Completar TODOs en `views_4xx.py`

2. **Crear templates correspondientes**:

    - `catalogacion/0xx/*.html`
    - `catalogacion/1xx/*.html`
    - `catalogacion/2xx/*.html`
    - `catalogacion/3xx/*.html`
    - `catalogacion/4xx/*.html`

3. **Agregar vistas de detalle**:

    - `detalle_obra(request, obra_id)` en `views_base.py`
    - Vista completa con todos los campos MARC

4. **Testing**:
    - Crear tests unitarios para cada vista
    - Validar patrón de campos anidados

## 📚 Referencias

-   **Documentación MARC21**: https://www.loc.gov/marc/bibliographic/
-   **Patrón de referencia**: `views/views_3xx.py` líneas 36-200
-   **Ejemplo funcional**: http://127.0.0.1:8000/prueba/campo-300/

## ✅ Ventajas de la Nueva Organización

1. ✅ **Modularidad**: Cada bloque MARC en su archivo
2. ✅ **Mantenibilidad**: Fácil encontrar y modificar vistas
3. ✅ **Escalabilidad**: Agregar nuevos bloques sin saturar archivos
4. ✅ **Consistencia**: Patrón claro para campos repetibles
5. ✅ **Documentación**: Cada archivo con docstrings claros
6. ✅ **Testing**: Vistas de prueba separadas de producción
7. ✅ **Compatibilidad**: Imports siguen funcionando
8. ✅ **Claridad**: Estructura similar a `models/`
