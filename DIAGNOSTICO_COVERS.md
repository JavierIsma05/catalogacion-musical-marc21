# ANÁLISIS: Por qué no se trae el cover en el dashboard

## Resumen del Problema

El cover no aparece en `catalogo_publico/lista_obras.html` porque **no hay datos digitalizados asociados a las obras**.

---

## Diagnóstico Completo

### ✗ PROBLEMA 1: Falta de relación entre Obra y DigitalSet

```python
# En tu base de datos:
ObraGeneral (12 "Estudio para piano")
  └── digital_set: None  ❌
  └── segments: []       ❌
```

**Explicación:**
- `DigitalSet` es el modelo que representa una colección DIGITALIZADA
- Solo colecciones que han sido importadas/escaneadas tienen `DigitalSet`
- Una obra sin `DigitalSet` no tiene páginas digitalizadas
- Sin páginas, no hay `derivative_path` y por lo tanto no hay `cover_url`

---

### ✗ PROBLEMA 2: Falta de DigitalPages con derivative_path

```python
# Lo que se necesita:
DigitalSet (id=12)
  └── pages (DigitalPage)
      └── page_number: 1
          └── derivative_path: "derivatives/page_001.jpg"  ← LA IMAGEN REAL
```

Sin este archivo, `default_storage.url(derivative_path)` devuelve `None`.

---

### ✗ PROBLEMA 3: Sin datos, el template muestra placeholder

```html
<!-- En lista_obras.html -->
{% if obra.cover_url and obra.visor_url %}
    <!-- Muestra imagen y link -->
{% else %}
    <div>Sin portada</div>  ← Aquí es donde ves nada
{% endif %}
```

---

## Solución

### Paso 1: Crear datos digitalizados (para pruebas)

```bash
python manage.py shell
```

```python
from catalogacion.models import ObraGeneral
from digitalizacion.models import DigitalSet, DigitalPage

# 1. Obtener una obra existente
obra = ObraGeneral.objects.activos().first()

# 2. Crear DigitalSet para esa obra
ds = DigitalSet.objects.create(
    coleccion=obra,
    estado='IMPORTADO',
    total_pages=1,
    repository_path='/media/digitalizado/'
)

# 3. Crear DigitalPage con derivative
from django.core.files.storage import default_storage
DigitalPage.objects.create(
    digital_set=ds,
    page_number=1,
    master_path='/media/tif/page_001.tif',
    derivative_path='derivatives/page_001.jpg'  # Ruta relativa a MEDIA_ROOT
)
```

### Paso 2: Crear la imagen real

```bash
# Crear carpeta
mkdir -p media/derivatives

# Crear imagen de prueba (requiere PIL)
python -c "from PIL import Image; img = Image.new('RGB', (100, 150)); img.save('media/derivatives/page_001.jpg')"
```

### Paso 3: Verificar que funciona

Abre el catálogo público y deberías ver:
- ✓ La imagen del cover
- ✓ El cover es clickeable
- ✓ Te lleva a `/digitalizacion/coleccion/12/visor/`

---

## Para Producción/Datos Reales

En producción, los datos deben venir de:
1. **El proceso de importación**: cuando subes un PDF o ZIP con imágenes
2. **El proceso de generación de derivatives**: convertir TIF → JPG
3. **El gestor de digitalización**: que crea DigitalSet y DigitalPages

Ve a `digitalizacion/views.py` → `ImportarColeccionView` para ver cómo se importan realmente.

---

## Verificación: Todo funciona ✓

```
Obra ID: 12 - Estudio para piano
  ✓ digital_set: DigitalSet Colección 12
  ✓ pages: 1
  ✓ derivative_path: derivatives/page_001.jpg
  ✓ cover_url: /media/derivatives/page_001.jpg
  ✓ visor_url: /digitalizacion/coleccion/12/visor/
```

El código está correcto. Solo falta que subas/importes colecciones digitalizadas.
