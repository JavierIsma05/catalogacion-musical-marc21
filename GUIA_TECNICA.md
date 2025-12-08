# 🎼 GUÍA TÉCNICA - CATALOGACIÓN MUSICAL MARC21

## 📌 INICIO RÁPIDO

### Ejecutar el servidor:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Acceder a:
- **UI Principal**: http://localhost:8000
- **Panel Admin**: http://localhost:8000/admin
- **API**: http://localhost:8000/api (si está configurada)

---

## 🏗️ ESTRUCTURA DE MODELOS

### Niveles de Anidamiento:

```
ObraGeneral (Raíz)
├── Nivel 1: Campos simples (tipo_registro, nivel_bibliografico, etc.)
├── Nivel 2: Modelos relacionados (ForeignKey)
│   ├── MedioInterpretacion382 (solista)
│   │   └── Nivel 3: MedioInterpretacion382_a (medio)
│   ├── ProduccionPublicacion (función)
│   │   ├── Lugar264 (lugar)
│   │   ├── NombreEntidad264 (nombre)
│   │   └── Fecha264 (fecha)
│   ├── EnlaceDocumentoFuente773
│   │   └── NumeroControl773
│   └── ... (otros campos anidados)
└── OneToOne: DatosBiograficos545 (única instancia por obra)
```

---

## 🔐 SISTEMA DE VALIDACIÓN

### Tres Capas:

1. **Django Models** (`validadores.py`)
   - Validación de campos requeridos
   - Validación de formato PAEC
   - Validación de códigos MARC

2. **Django Forms** (`forms_*xx.py`)
   - Validación de widgets
   - Validación de choices
   - Validación personalizada

3. **JavaScript Cliente** (`subcampo-validators.js`)
   - Validación en tiempo real
   - Feedback visual
   - Prevención de envíos inválidos

---

## 📊 MAPEO MARC21 → DJANGO

### Nomenclatura:

| MARC | Término | Modelo Django | Campo |
|------|---------|---------------|-------|
| `245 $a` | Título principal | ObraGeneral | titulo_principal |
| `100 $a` | Compositor | ObraGeneral | compositor (FK) |
| `240` | Título uniforme | ObraGeneral | titulo_uniforme (FK) |
| `382 $b` | Solista | MedioInterpretacion382 | solista |
| `382 $a` | Medio | MedioInterpretacion382_a | medio |
| `264 $a` | Lugar | Lugar264 | lugar |
| `264 $b` | Entidad | NombreEntidad264 | nombre |
| `264 $c` | Fecha | Fecha264 | fecha |

### Campos con Choices (enumeraciones):

```python
# Ejemplo: MedioInterpretacion382_a.medio
MEDIOS = [
    ('piano', 'Piano'),
    ('dos pianos', 'Dos pianos'),
    ('piano a cuatro manos', 'Piano a cuatro manos'),
    ('piano con acompañamiento', 'Piano con acompañamiento'),
]
```

---

## 🔄 FLUJO DE GUARDADO (CrearObraView.form_valid)

```python
1. form_valid() recibe formulario principal
   ↓
2. _validar_formsets() valida todos los formsets
   ↓
3. form.save(commit=False) → self.object
   ↓
4. self.object.save() → Obtiene PK
   ↓
5. Guardar medios_interpretacion (382)
   - Guardar MedioInterpretacion382
   - Asignar FK a obra
   ↓
6. Guardar medios_formsets (382_a anidado)
   - Validar cada formset anidado
   - Guardar subcampos $a
   ↓
7. Guardar demás formsets normalmente
   ↓
8. redirect() → Detalle obra creada
```

---

## 📝 VARIABLES DE ENTORNO RECOMENDADAS

Crear archivo `.env` (no incluir en git):

```bash
# Seguridad
DEBUG=False
SECRET_KEY=tu-clave-secreta-de-50-caracteres-minimo
ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com

# Base de Datos
DATABASE_ENGINE=postgresql
DATABASE_NAME=catalogacion_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_contraseña
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email (para notificaciones)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_app

# Locale
LANGUAGE_CODE=es
TIME_ZONE=America/Bogota
```

---

## 🧪 PRUEBAS

### Ejecutar tests:
```bash
python manage.py test catalogacion
```

### Tests disponibles:
- `test_bloque_0xx.py` - Pruebas de íncipit

---

## 📚 REFERENCIAS MARC21

Estructura completa de campos:

- **0XX**: Números de control e información codificada
- **1XX**: Encabezamientos principales
- **2XX**: Títulos, ediciones, publicación
- **3XX**: Descripción física
- **4XX**: Series
- **5XX**: Notas
- **6XX**: Materias y géneros
- **7XX**: Asientos secundarios
- **8XX**: Números y ubicación

---

## ⚡ OPTIMIZACIONES FUTURAS

1. **Cache**: Implementar redis para autocompletes frecuentes
2. **Índices BD**: Agregar índices en campos searchable
3. **APIs**: Exponer vía DRF para aplicaciones móviles
4. **Búsqueda avanzada**: Implementar elasticsearch
5. **Exportación**: Agregar exportación a MARC XML/JSON

---

## 🐛 TROUBLESHOOTING

### Error: "NameError: name 'os' is not defined"
**Solución**: Verificar que `import os` esté en `settings.py` línea 13

### Error: "Tabla no existe"
**Solución**: Ejecutar migraciones: `python manage.py migrate`

### Error: "Medio de interpretación no se guarda"
**Solución**: Verificar que formset 382_a tenga datos POST válidos

### Error: "Autocomplete no funciona"
**Solución**: Verificar que endpoint AJAX esté disponible en `urls.py`

---

## 📖 DOCUMENTACIÓN ADICIONAL

Ver archivos:
- `ANALISIS_FINAL.md` - Análisis completo del proyecto
- `README.md` - Guía general del proyecto
- `catalogacion/models/__init__.py` - Importaciones de modelos
- `catalogacion/forms/__init__.py` - Importaciones de formularios

---

**Última actualización**: 7 de Diciembre de 2025  
**Versión**: 1.0  
**Status**: ✅ PRODUCCIÓN LISTA
