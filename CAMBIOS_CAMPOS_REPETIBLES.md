# 📋 CAMBIOS EN CAMPOS REPETIBLES - MARC21

## Fecha: 31 de octubre de 2025

## 🎯 Resumen de Cambios

Se implementaron tres campos repetibles como modelos independientes y se ajustaron los campos del modelo `ObraGeneral` según las especificaciones MARC21.

---

## 📝 CAMPO 245: CAMBIOS EN TÍTULO PRINCIPAL

### Cambios realizados:

1. **RENOMBRADO**: `resto_titulo` → `subtitulo`
   - **Razón**: Mayor claridad semántica (245 $b es el subtítulo)
   - **Help text actualizado**: "245 $b – Subtítulo"

2. **ELIMINADOS**: Campos de parte/sección
   - ❌ `numero_parte_245` (245 $n)
   - ❌ `nombre_parte_245` (245 $p)
   - **Razón**: Estos subcampos no se utilizarán en el proyecto

### Campos finales del 245 en ObraGeneral:
```python
titulo_principal = models.CharField(...)  # 245 $a
subtitulo = models.CharField(...)         # 245 $b (antes resto_titulo)
mencion_responsabilidad = models.TextField(...)  # 245 $c
```

---

## 📚 CAMPO 246: TÍTULOS ALTERNATIVOS (Modelo separado)

### ❌ Campos eliminados de ObraGeneral:
- `titulo_variante` (246 $a)
- `resto_titulo_variante` (246 $b)

### ✅ Nueva clase: `TituloAlternativo`

```python
class TituloAlternativo(models.Model):
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='titulos_alternativos'
    )
    titulo = models.CharField(max_length=500)  # 246 $a
    resto_titulo = models.CharField(max_length=500, blank=True, null=True)  # 246 $b
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Características**:
- ✅ Repetible (múltiples títulos alternativos por obra)
- ✅ Inline en Django Admin
- ✅ Formset en templates frontales

---

## 📘 CAMPO 250: EDICIÓN (Modelo separado)

### ❌ Campo eliminado de ObraGeneral:
- `presentacion_musical` (254 $a) - **NOTA**: Este era del campo 254, no 250

### ✅ Nueva clase: `Edicion`

```python
class Edicion(models.Model):
    obra = models.ForeignKey(
        'ObraGeneral',
        on_delete=models.CASCADE,
        related_name='ediciones'
    )
    edicion = models.CharField(max_length=200)  # 250 $a
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

**Características**:
- ✅ Repetible (múltiples ediciones por obra)
- ✅ Inline en Django Admin
- ✅ Formset en templates frontales
- ✅ Ejemplos: "2a ed.", "Primera edición revisada"

---

## 📖 CAMPO 264: PRODUCCIÓN/PUBLICACIÓN

### Estado:
- ✅ **YA IMPLEMENTADO** como modelo separado (`ProduccionPublicacion`)
- ✅ No requiere cambios adicionales
- ✅ Formset funcional

---

## 🔧 ARCHIVOS MODIFICADOS

### 1. **models.py**
```python
# Cambios en ObraGeneral:
- Renombrado: resto_titulo → subtitulo
- Eliminados: numero_parte_245, nombre_parte_245
- Eliminados: titulo_variante, resto_titulo_variante, presentacion_musical

# Nuevas clases añadidas:
+ class TituloAlternativo(models.Model)
+ class Edicion(models.Model)
```

### 2. **admin.py**
```python
# Imports actualizados:
from .models import (
    TituloAlternativo,  # ✅ Nuevo
    Edicion,            # ✅ Nuevo
    ProduccionPublicacion
)

# Nuevos inlines:
+ class TituloAlternativoInline(admin.TabularInline)
+ class EdicionInline(admin.TabularInline)

# Actualizado ObraGeneralAdmin:
inlines = [TituloAlternativoInline, EdicionInline, ProduccionPublicacionInline]

# Fieldsets actualizados:
- Eliminado fieldset de "Títulos adicionales"
- Campo 245 ahora solo tiene: titulo_principal, subtitulo, mencion_responsabilidad
```

### 3. **forms.py**
```python
# Imports actualizados:
from .models import (
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion
)

# Nuevos formsets:
+ TituloAlternativoFormSet = forms.inlineformset_factory(...)
+ EdicionFormSet = forms.inlineformset_factory(...)

# Campos eliminados de ObraForm.Meta.fields:
- 'numero_parte_245'
- 'nombre_parte_245'
- 'titulo_variante'
- 'resto_titulo_variante'
- 'presentacion_musical'

# Campo renombrado:
- 'resto_titulo' → 'subtitulo'

# Widgets eliminados:
- resto_titulo → subtitulo (widget mantenido)
- Eliminados todos los widgets de campos borrados
```

### 4. **views.py**
```python
# Imports actualizados:
from .forms import (
    ObraForm,
    TituloAlternativoFormSet,
    EdicionFormSet,
    ProduccionPublicacionFormSet
)

# Vista obra_general actualizada:
- Manejo de 3 formsets (246, 250, 264)
- Guardado en cascada de registros relacionados
```

### 5. **templates/ObraGeneral/obra_general.html**
```django
# Actualizaciones pendientes:
- Cambiar form.resto_titulo → form.subtitulo
- Eliminar campos: numero_parte_245, nombre_parte_245
- Reemplazar bloque 246 estático por formset_246
- Reemplazar bloque 254 por formset_250
- Actualizar bloque 264 (ya usa formset_264)
```

---

## 🚀 PRÓXIMOS PASOS

### 1. **Crear migraciones**
```bash
.venv\Scripts\python.exe manage.py makemigrations
.venv\Scripts\python.exe manage.py migrate
```

### 2. **Actualizar templates**
- ✅ Cambiar `resto_titulo` → `subtitulo` en línea 405
- ✅ Eliminar sección de `numero_parte_245` y `nombre_parte_245`
- ✅ Reemplazar bloque 246 estático por formset dinámico
- ✅ Reemplazar bloque 254 por formset de ediciones (250)
- ✅ Verificar bloque 264 (formset ya implementado)

### 3. **Probar funcionalidad**
- Crear obra con múltiples títulos alternativos
- Agregar múltiples ediciones
- Verificar guardado y visualización

---

## 📊 RESUMEN DE RELACIONES

```
ObraGeneral (1) ──── (N) TituloAlternativo
                ├─── (N) Edicion
                └─── (N) ProduccionPublicacion
```

**Related names**:
- `obra.titulos_alternativos.all()` → Campo 246
- `obra.ediciones.all()` → Campo 250
- `obra.produccion_publicacion.all()` → Campo 264

---

## ⚠️ IMPORTANTE

1. **Migraciones**: Ejecutar antes de probar cambios
2. **Datos existentes**: Los campos eliminados (`titulo_variante`, etc.) perderán datos si existían
3. **Templates**: Actualizar TODAS las referencias a `resto_titulo` → `subtitulo`
4. **Formsets**: Incluir {{ formset_246.management_form }}, {{ formset_250.management_form }}, etc.

---

## ✅ VALIDACIÓN

- [x] Models actualizados
- [x] Admin configurado con inlines
- [x] Forms con formsets creados
- [x] Views con lógica de guardado
- [ ] Templates actualizados (PENDIENTE)
- [ ] Migraciones ejecutadas (PENDIENTE)
- [ ] Pruebas funcionales (PENDIENTE)

---

**Autor**: AI Assistant  
**Fecha**: 31/10/2025  
**Versión**: 1.0
