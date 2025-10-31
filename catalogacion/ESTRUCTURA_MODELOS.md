# 📁 Estructura de Modelos - Catalogación MARC21

## Organización de archivos

### `models.py` (Principal)
Contiene los modelos principales del sistema:
- **Tablas de autoridades**: `AutoridadPersona`, `AutoridadTituloUniforme`, `AutoridadFormaMusical`, `AutoridadMateria`
- **Modelo principal**: `ObraGeneral` (Registro bibliográfico MARC21)
- **Constantes**: `TONALIDADES`, `FUNCIONES_PERSONA`, `CALIFICADORES_AUTORIA`

### `models_repetibles.py` (Campos MARC21 repetibles)
Contiene modelos para campos MARC21 marcados como repetibles (R):
- **Campo 246**: `TituloAlternativo` - Títulos alternativos/variantes
- **Campo 250**: `Edicion` - Ediciones
- **Campo 264**: `ProduccionPublicacion` - Producción/Publicación/Distribución

## Relaciones

```
ObraGeneral (1) ──┬── (N) TituloAlternativo  [246]
                  ├── (N) Edicion             [250]
                  └── (N) ProduccionPublicacion [264]
```

## Importación

Todos los modelos se pueden importar desde `.models`:

```python
from catalogacion.models import (
    ObraGeneral,
    AutoridadPersona,
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion
)
```

O desde el archivo específico:

```python
from catalogacion.models_repetibles import (
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion
)
```

## Ventajas de esta estructura

✅ **Modularidad**: Campos repetibles separados del modelo principal  
✅ **Mantenibilidad**: Más fácil localizar y modificar código  
✅ **Legibilidad**: `models.py` más limpio y enfocado  
✅ **Escalabilidad**: Fácil agregar más campos repetibles en el futuro  
✅ **Documentación**: Cada archivo tiene su propósito claramente definido
