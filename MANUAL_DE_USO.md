# 📚 MANUAL DE USO - CATALOGACIÓN MUSICAL MARC21

## Índice
1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Crear una Obra](#crear-una-obra)
4. [Campos MARC21 Explicados](#campos-marc21-explicados)
5. [Tipos de Obra](#tipos-de-obra)
6. [Autoridades](#autoridades)
7. [Gestión de Obras](#gestión-de-obras)
8. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Este sistema permite catalogar obras musicales utilizando el estándar **MARC21** (Machine-Readable Cataloging). MARC21 es el formato internacional estándar para codificar información bibliográfica en formato legible por máquinas.

### Características principales:
- ✅ Soporte completo para MARC21 (campos 0xx-8xx)
- ✅ Campos repetibles (subcampos)
- ✅ Formsets anidados para relaciones complejas
- ✅ Sistema de autoridades integrado
- ✅ Base de datos SQLite3 (desarrollo)
- ✅ Interfaz web intuitiva

---

## Acceso al Sistema

### 1. Iniciar el servidor Django

```bash
cd d:\PYTHON\proyectoMarcactualizado\catalogacion-musical-marc21
python manage.py runserver
```

El servidor se iniciará en: **http://localhost:8000**

### 2. Acceder a la aplicación

- **Página Principal**: http://localhost:8000/
- **Listar Obras**: http://localhost:8000/catalogacion/obras/
- **Crear Obra**: http://localhost:8000/catalogacion/obras/seleccionar-tipo/

---

## Crear una Obra

### Paso 1: Seleccionar tipo de obra

Accede a: `http://localhost:8000/catalogacion/obras/seleccionar-tipo/`

Se mostrarán 6 tipos disponibles:

1. **Colección Manuscrita** - Conjunto de obras manuscritas
2. **Obra en Colección Manuscrita** - Obra individual dentro de colección
3. **Obra Manuscrita Individual** (OIM) - Obra manuscrita completa
4. **Colección Impresa** - Conjunto de obras publicadas
5. **Obra en Colección Impresa** - Obra individual publicada
6. **Obra Impresa Individual** - Obra publicada completa

**Recomendación para comenzar:** Selecciona **"Obra Manuscrita Individual"**

### Paso 2: Llenar el formulario

Una vez selecciones el tipo, verás un formulario dividido en secciones:

#### **Campos Obligatorios** (marcados con *)

1. **245 $a - Título Principal**
   - Ej: "Concierto para Piano No. 1 en Do Mayor"

2. **008 - Descripción - Tipo de Registro y Nivel Bibliográfico**
   - Se llena automáticamente según el tipo de obra

3. **040 - Centro de Catalogación**
   - Ej: "Biblioteca Nacional" o tu código de institución

4. **340 - Técnica (Manuscrito/Impreso)**
   - Selecciona: MS (Manuscrito) o PR (Impreso)

5. **041 - Códigos de Lengua**
   - Indica la lengua de la obra (Español, Italiano, Alemán, etc.)

#### **Campos Opcionales** (según tipo de obra)

Los siguientes campos se pueden agregar según sea necesario:

- **031 - Íncipit Musical**: Inicio musical en notación GUIDO
- **100 - Compositor**: Función de compositor
- **246 - Título Alternativo**: Otros títulos
- **250 - Edición**: Información de edición
- **264 - Producción/Publicación**: Lugar y fecha
- **382 - Medio de Interpretación**: Instrumentos/voces
- **500 - Nota General**: Notas adicionales
- **505 - Contenido**: Estructura de la obra (movimientos, partes)
- **650 - Materia**: Temas/materias
- **655 - Género**: Género musical
- **700 - Nombre Relacionado**: Personas relacionadas (intérpretes, editores)
- **852 - Ubicación**: Dónde se encuentra la obra
- **856 - Disponible**: URLs de acceso

### Paso 3: Agregar Autoridades

Para campos que usan autoridades (como Compositor, Materia), debes:

1. **Crear o Seleccionar una Autoridad**:
   - Si la autoridad no existe, puedes crearla
   - Ej: Para "Beethoven", primero creas: Beethoven, Ludwig van (1770-1827)

2. **Vincular a la Obra**:
   - Una vez creada, seleccionas de la lista desplegable

### Paso 4: Guardar

Haz clic en **"Guardar Obra"** en la parte inferior del formulario.

Si hay errores de validación, se mostrarán en rojo. Corrígelos y vuelve a intentar.

---

## Campos MARC21 Explicados

### 0xx - Campos de Control

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **001** | Número de Control | M000006 |
| **005** | Fecha de Última Catalogación | Automático |
| **008** | Datos Codificados | Automático |
| **031** | Íncipit Musical | Allegro con brio |
| **040** | Centro de Catalogación | TEST |

### 1xx - Puntos de Acceso Principales

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **100** | Compositor | Beethoven, Ludwig van |
| **240** | Título Uniforme | Sonatas para piano |

### 2xx - Títulos, Edición, Publicación

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **245** | Título Principal | Concierto para Piano No. 1 |
| **246** | Título Alternativo | Piano Concerto No. 1 |
| **250** | Edición | Primera edición, revisada |
| **264** | Producción/Publicación | Viena, 1803 |

### 3xx - Descripción Física

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **300** | Descripción Física | 45 páginas |
| **340** | Técnica | Manuscrito |
| **382** | Medio de Interpretación | Violín solista, orquesta |
| **383** | Designación Musica | Sonata |
| **384** | Tonalidad | Do Mayor |

### 5xx - Notas

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **500** | Nota General | Concierto compuesto entre 1802-1803 |
| **505** | Contenido | I. Allegro \| II. Largo \| III. Rondo |
| **520** | Sumario | Descripción general de la obra |
| **545** | Datos Biográficos | Historia del compositor |

### 6xx - Puntos de Acceso Adicionales - Materia

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **650** | Materia | Conciertos para piano |
| **655** | Género | Concierto |

### 7xx - Puntos de Acceso Adicionales - Personas y Entidades

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **700** | Nombre Relacionado (Persona) | Cortot, Alfred (intérprete) |
| **710** | Entidad Relacionada | Orquesta Filarmónica |

### 8xx - Enlaces y Ubicación

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **852** | Ubicación | Biblioteca Nacional - Sección Manuscritos |
| **856** | Recurso en Línea | https://ejemplo.org/obra/123 |

---

## Tipos de Obra

### 1. Colección Manuscrita

**Cuándo usarla**: Para un conjunto de obras manuscritas sin compositor único

**Características**:
- Título uniforme principal (130)
- Obras constituyentes (774)
- Sin íncipit musical

**Campos clave**:
- 245 $a - Título de la colección
- 130 - Título uniforme
- 774 - Obras en la colección

---

### 2. Obra en Colección Manuscrita

**Cuándo usarla**: Para una obra individual dentro de una colección manuscrita

**Características**:
- Incluye íncipit musical (031)
- Compositor (100)
- Enlace a obra madre (773)

**Campos clave**:
- 031 - Íncipit musical
- 100 - Compositor
- 773 - Enlace a la colección

---

### 3. Obra Manuscrita Individual (OIM) ⭐

**Cuándo usarla**: Para una obra manuscrita completa e independiente

**Características**:
- Íncipit musical completo
- Todos los campos MARC21
- Sin vínculos de colección

**Campos clave**:
- 031 - Íncipit musical
- 100 - Compositor
- 382 - Medio de interpretación
- 505 - Contenido/movimientos

---

### 4. Colección Impresa

**Cuándo usarla**: Para un conjunto de obras publicadas

**Características**:
- Información de publicación (264)
- Descripción física (300)
- Obras constituyentes (774)

---

### 5. Obra en Colección Impresa

**Cuándo usarla**: Para una obra individual dentro de una colección publicada

**Características**:
- Íncipit musical
- Compositor
- Enlace a obra madre

---

### 6. Obra Impresa Individual

**Cuándo usarla**: Para una obra publicada completa e independiente

**Características**:
- Todos los campos MARC21
- Información completa de publicación
- Sin vínculos de colección

---

## Autoridades

El sistema utiliza autoridades para garantizar la consistencia de datos.

### Autoridades Disponibles

1. **AutoridadPersona** - Compositores, intérpretes, editores
   - Formato: Apellidos, Nombres (Fechas)
   - Ej: Beethoven, Ludwig van (1770-1827)

2. **AutoridadFormaMusical** - Géneros y formas
   - Ej: Concierto, Sonata, Sinfonía

3. **AutoridadMateria** - Temas y materias
   - Ej: Conciertos para piano, Música clásica

4. **AutoridadEntidad** - Instituciones y entidades
   - Ej: Orquesta Filarmónica, Biblioteca Nacional

### Crear una Autoridad

1. Accede a **Autoridades** en el menú principal
2. Selecciona el tipo de autoridad
3. Haz clic en **"Crear Nueva"**
4. Llena los campos (nombre, coordenadas biográficas si aplica)
5. Haz clic en **"Guardar"**

### Usar una Autoridad

1. En el formulario de crear/editar obra
2. En campos que requieran autoridades, verás un campo de búsqueda
3. Empieza a escribir el nombre
4. Selecciona de las opciones sugeridas
5. Se vinculará automáticamente

---

## Gestión de Obras

### Ver una Obra

1. Ve a **Listar Obras**: http://localhost:8000/catalogacion/obras/
2. Haz clic en el título de la obra
3. Se abrirá la vista de detalle con toda la información

**Información mostrada**:
- Todos los campos MARC21
- Subcampos anidados (si existen)
- Fecha de creación y última modificación
- Botones de edición y eliminación

### Editar una Obra

1. En la vista de detalle, haz clic en **"Editar"**
2. Se abrirá el mismo formulario de creación
3. Modifica los campos que necesites
4. Haz clic en **"Guardar Cambios"**

**Nota**: Puedes agregar más subcampos en cualquier momento

### Eliminar una Obra

1. En la vista de detalle, haz clic en **"Eliminar"**
2. Confirma la eliminación
3. La obra se eliminará de la base de datos (incluidos todos sus subcampos)

### Listar Obras

En **Listar Obras** verás:
- ID de la obra
- Número de control (MARC21 001)
- Título principal (245)
- Tipo de obra
- Fecha de creación

Puedes:
- Buscar por título
- Ordenar por diferentes campos
- Ver detalles haciendo clic

---

## Ejemplos de Uso

### Ejemplo 1: Catalogar un Concierto para Piano Manuscrito

```
1. Seleccionar tipo: "Obra Manuscrita Individual"

2. Campos principales:
   - Título: "Concierto para Piano No. 1 en Do Mayor"
   - Compositor: Beethoven, Ludwig van
   - Íncipit: "Allegro con brio"
   - Clave: G-2
   - Compás: 4/4

3. Campos opcionales:
   - Edición: "Primera edición, revisada por Jörg Demus"
   - Medio: Violín solista, orquesta
   - Movimientos:
     I. Allegro con brio (Do Mayor)
     II. Largo (La bemol Mayor)
     III. Rondo (Do Mayor)
   - Materia: Conciertos para piano
   - Género: Concierto
   - Ubicación: Biblioteca Nacional - Colección Manuscritos

4. Guardar
```

### Ejemplo 2: Catalogar una Sonata para Violín Publicada

```
1. Seleccionar tipo: "Obra Impresa Individual"

2. Campos principales:
   - Título: "Sonata para Violín No. 9 en La Mayor"
   - Compositor: Mozart, Wolfgang Amadeus
   - Editorial: Breitkopf & Härtel
   - Año: 1778

3. Campos opcionales:
   - Descripción física: "150 páginas, rústica"
   - Tonalidad: La Mayor
   - Medio: Violín solista, piano
   - Materia: Sonatas para violín
   - URL: https://ejemplo.org/mozart/sonata-9

4. Guardar
```

---

## Solución de Problemas

### Error: "Este campo es obligatorio"

**Solución**: Asegúrate de haber llenado todos los campos marcados con `*`

Campos obligatorios:
- Título principal (245)
- Centro de catalogación (040)
- Tipo de registro/Nivel bibliográfico (008)
- Técnica (340)
- Códigos de lengua (041)

### Error: "Selecciona una opción válida"

**Solución**: En campos de selección (dropdowns), debes elegir de las opciones disponibles, no escribir texto libre.

### La obra no aparece después de guardar

**Solución**: 
1. Verifica que no haya errores de validación (mensaje en rojo)
2. Actualiza la página (F5)
3. Ve a "Listar Obras" para verificar si se creó

### No puedo crear una autoridad

**Solución**: 
1. Accede primero a la sección de Autoridades
2. Crea la autoridad antes de vincularla a una obra
3. O usa el formulario de obra para crearla sobre la marcha (si está disponible)

### ¿Cómo buscar una obra?

En la lista de obras, usa la barra de búsqueda superior para:
- Buscar por título
- Buscar por número de control
- Filtrar por tipo de obra

### ¿Puedo exportar datos?

Actualmente, los datos se almacenan en SQLite3. Para exportar:
1. Accede a `/admin/` para usar el admin de Django
2. O consulta la BD directamente: `db.sqlite3`

---

## Referencia Rápida - Keyboard Shortcuts

| Acción | Atajo |
|--------|-------|
| Guardar (en formulario) | Ctrl + S |
| Buscar | Ctrl + F |
| Recargar página | F5 |
| Ir a inicio | Ctrl + Home |

---

## Recursos Adicionales

### Documentación MARC21
- [Standar MARC21 Oficial](https://www.loc.gov/marc/bibliographic/)
- [MARC21 para Música](https://www.loc.gov/marc/bibliographic/bd0xx.html)

### Notación Musical (GUIDO)
Para especificar incipits, se usa notación GUIDO:
- `c d e f g` - Notas (do, re, mi, fa, sol)
- `C D E F G` - Octava superior
- `2` - Media nota
- `4` - Cuarto de nota
- `8` - Octavo de nota

**Ejemplo**: `c d e f g a b c' a b c'` - Escala ascendente

---

## Contacto y Soporte

Para reportar problemas o solicitar mejoras:
1. Revisa la sección de "Solución de Problemas"
2. Contacta al administrador del sistema
3. Documenta el error con capturas de pantalla si es posible

---

**Última actualización**: 7 de diciembre de 2025
**Versión del Sistema**: Django 5.1.2, MARC21 Completo
