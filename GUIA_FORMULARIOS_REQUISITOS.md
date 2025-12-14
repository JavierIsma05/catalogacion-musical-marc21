# Guía de Requisitos y Solución de Problemas - Formularios de Obras

## 📋 Campos OBLIGATORIOS del Formulario Principal

Para que un formulario de obra se guarde correctamente, debes llenar:

### 1. **Tipo de Registro** (campo `tipo_registro`)
- **Valores válidos**: 
  - `d` = Música manuscrita
  - `c` = Música impresa
- **Nota**: Se preestablece según el tipo de obra seleccionado

### 2. **Nivel Bibliográfico** (campo `nivel_bibliografico`)
- **Valores válidos**:
  - `a` = Parte componente
  - `c` = Colección
  - `m` = Obra independiente
- **Nota**: Se preestablece según el tipo de obra seleccionado

### 3. **Centro Catalogador** (campo `centro_catalogador`)
- **Tipo**: Texto libre
- **Ejemplo**: `MxFLC`, `BnF`, `LC`
- **Obligatorio**: SÍ
- **MARC**: 040 $a

### 4. **Título Principal** (campo `titulo_principal`)
- **Tipo**: Texto libre
- **Obligatorio**: SÍ
- **MARC**: 245 $a o 131 $a
- **Nota**: Puede ser título general o uniforme

### 5. **Técnica / Soporte** (campo `ms_imp`)
- **Valores válidos**:
  - `autógrafo`
  - `posible autógrafo`
  - `manuscrito`
  - `manuscrito de copista no identificado`
  - `impreso`
  - `fotocopia de manuscrito`
  - `fotocopia de impreso`
- **Obligatorio**: SÍ
- **MARC**: 340 $d

### 6. **Punto de Acceso Principal** (Al menos UNO obligatorio)

**Opción A: Compositor** (campo `compositor` o `compositor_texto`)
- **MARC**: 100 $a
- **Usar cuando**: La obra tiene un autor/compositor identificado

**Opción B: Título Uniforme** (campo `titulo_uniforme` o `titulo_uniforme_texto`)
- **MARC**: 130 $a
- **Usar cuando**: Es una colección sin compositor único

⚠️ **Regla importante**: Debes especificar **AL MENOS UNO** de estos dos campos. Puedes llenar ambos si aplica.

---

## 🔧 Solución de Problemas Comunes

### Error: "This field is required" en centro_catalogador, titulo_principal, ms_imp

**Causa**: No rellenaste uno o más campos obligatorios del formulario principal.

**Solución**: 
1. Verifica que todos los campos mencionados arriba estén rellenados
2. Si aparece un asterisco rojo (*) al lado del campo, es obligatorio
3. Haz clic en "Guardar" de nuevo después de completar

---

### Error: "Debe especificar al menos un punto de acceso principal..."

**Causa**: Falta información de Compositor O Título Uniforme.

**Solución**:
- **Para obras con compositor**: Llena el campo "Compositor" (100)
- **Para colecciones sin compositor**: Llena el campo "Título Uniforme" (130)
- **Para ambos casos**: Rellena ambos campos si aplica

---

### Error: "Select a valid choice" en tipo_registro, nivel_bibliografico, o ms_imp

**Causa**: Intentaste enviar un valor que no está en la lista de opciones válidas.

**Solución**:
- Verifica que el valor que enviaste esté en la lista de "Valores válidos" arriba
- En el navegador, selecciona de la lista desplegable, no escribas manualmente
- Si estás usando un cliente API, usa exactamente los valores documentados

---

### Error: "ManagementForm data is missing..."

**Causa**: Un formset no recibió correctamente los campos de control (TOTAL_FORMS, INITIAL_FORMS).

**Solución** (si usas API/cliente personalizado):
- Cada formset necesita estos campos en el POST:
  - `{PREFIX}-TOTAL_FORMS`
  - `{PREFIX}-INITIAL_FORMS`
  - `{PREFIX}-MIN_NUM_FORMS` (opcional)
  - `{PREFIX}-MAX_NUM_FORMS` (opcional)

**Prefijos de formsets válidos**:
```
incipits
lenguas
paises
funciones
medios_382
titulos_alt
ediciones
produccion
menciones_490
notas_500
contenidos_505
sumarios_520
biograficos_545
materias_650
generos_655
nombres_700
entidades_710
enlaces_773
enlaces_774
relaciones_787
ubicaciones_852
disponibles_856
```

---

## ✅ Verificación de Guardado

Cuando envíes el formulario:

1. **Si recibe un error (página roja)**: Lee el error, corrige el campo, y envía de nuevo
2. **Si se guarda correctamente**: Serás redirigido a la página de detalle de la obra
3. **La URL cambiará a** `/obras/{ID}/` donde `{ID}` es el número de la obra creada

---

## 📚 Ejemplo de Datos Válidos Mínimos

Para crear una **colección manuscrita** (tipo más restrictivo):

| Campo | Valor |
|-------|-------|
| Tipo Registro | `d` (manuscrita) |
| Nivel Bibliográfico | `c` (colección) |
| Centro Catalogador | `MxFLC` |
| Título Principal | `Mi Colección de Obras Musicales` |
| Técnica | `manuscrito` |
| Punto de Acceso | `Colección de obras musicales` (130) |

Con estos datos mínimos, la obra se guardará correctamente.

---

## 🔍 Cómo Ver los Errores Detallados

Si el formulario no se guarda y quieres ver el error exacto:

1. **Abre la consola del navegador** (F12 → Consola)
2. **Busca mensajes de ERROR** en rojo
3. **Copia el error completo**
4. **Revisa la sección "Solución de Problemas Comunes" arriba**

Si el error no aparece ahí:
- Contacta al administrador con la captura de pantalla del error
- Proporciona los datos que intentaste guardar

---

## 📝 Notas sobre Campos Opcionales

Todos los demás campos (Idioma, País, Edición, etc.) son **OPCIONALES**:
- Puedes dejar formsets vacíos (sin agregar filas)
- O agregar filas con datos según sea necesario
- El formulario se guardará correctamente sin ellos

---

**Última actualización**: 7 de diciembre de 2025
**Versión del sistema**: Django 5.1.2 con MARC21
