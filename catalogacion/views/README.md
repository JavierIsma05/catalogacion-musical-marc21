# 📁 Organización de Vistas - Sistema MARC21

## 🎯 Estructura de Carpeta `views/`

Las vistas se han reorganizado por **bloques MARC21 bibliográficos** para mejor mantenimiento y escalabilidad.

```
catalogacion/
├── views/
│   ├── __init__.py                  # Exporta todas las vistas
│   ├── views_base.py                # Vistas generales de navegación
│   ├── views_autoridades.py         # Endpoints JSON para Select2
│   ├── views_0xx.py                 # Campos de control (ISBN, ISMN, etc.)
│   ├── views_1xx.py                 # Puntos de acceso (Compositor, Títulos)
│   ├── views_2xx.py                 # Títulos y publicación
│   ├── views_3xx.py                 # Descripción física ⭐
│   ├── views_4xx.py                 # Series
│   └── views_pruebas.py             # Testing y desarrollo
├── urls.py                          # Rutas URL
├── models/                          # Modelos organizados por bloques
└── forms.py                         # Formularios
```

## 📋 Descripción de Archivos

### `__init__.py`

**Propósito**: Exportar todas las vistas para uso en `urls.py`

**Permite**:

```python
from catalogacion.views import index, prueba_campo_300
```

### `views_base.py`

**Bloque**: No MARC (navegación general)

**Vistas**:

-   `index()` - Página principal
-   `plantillas()` - Lista de plantillas
-   `crear_obra()` - Inicio de creación
-   `coleccion_manuscrita()` - Lista manuscritas
-   `obra_individual_manuscrita()` - Detalle manuscrita
-   `coleccion_impresa()` - Lista impresas
-   `obra_individual_impresa()` - Detalle impresa

### `views_autoridades.py`

**Bloque**: API/Utilidades

**Vistas**:

-   `get_autoridades_json()` - Endpoint para Select2
    -   Compositores
    -   Títulos uniformes
    -   Formas musicales

**Ejemplo de uso**:

```javascript
$("#compositor").select2({
    ajax: {
        url: "/api/autoridades/?model=compositor",
        dataType: "json",
    },
});
```

### `views_0xx.py`

**Bloque MARC**: 0XX - Campos de Control

**Campos manejados**:

-   `020` - ISBN
-   `024` - ISMN
-   `028` - Número de editor
-   `031` - Íncipit musical (con URLs anidadas)
-   `041` - Código de lengua (con idiomas anidados)
-   `044` - Código de país

**Vistas**:

-   `crear_isbn(request, obra_id)`
-   `crear_ismn(request, obra_id)`
-   `crear_numero_editor(request, obra_id)`
-   `crear_incipit_musical(request, obra_id)`
-   `crear_codigo_lengua(request, obra_id)`
-   `listar_campos_0xx(request, obra_id)` - Vista resumen

**Patrón**: Campos repetibles, algunos con subcampos anidados

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
