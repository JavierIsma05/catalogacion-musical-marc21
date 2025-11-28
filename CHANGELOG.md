
# ------------------------------------------------------------
#    2. CHANGELOG.md COMPLETO
# ------------------------------------------------------------

Copia y pega esto:

```markdown
# 📜 CHANGELOG – Catalogación Musical MARC21

Este documento registra los cambios realizados en el sistema.

---

## [1.1.0] – 2025-02
### ✨ Cambios principales
- Se implementó **formset 655 completo** con:
  - Subdivisión dinámica `$x`
  - Botón X corregido
  - Estilo visual igual al 650
  - Template modular

- Se agregó soporte total en handlers:
  - `_save_subdivisiones_655()`

- Se corrigió la estructura del formulario 650.

---

## [1.0.9] – 2025-02
### 🎵 Migración de 773–774–787 a `AutoridadPersona`
- Eliminado `EncabezamientoEnlace`
- Modelos ajustados:
  - `enlace_773`
  - `enlace_774`
  - `relacion_787`
- Consistencia con campos 100, 600, 700.

---

## [1.0.8] – 2025-01
### 🎛️ Mejoras en autocompletado
- Mejoras UX
- Soporte para teclado
- Opción “Crear nuevo”

---

## [1.0.7] – 2025-01
### 🧱 Handlers unificados
- Archivo `obra_formset_handlers.py` reorganizado
- Sistema universal para subcampos dinámicos

---

## [1.0.6] – 2025-01
### 🎨 Nuevos templates 650
- Autocomplete + subdivisiones
- Estilo moderno

---

## [1.0.5] – 2025-01
### 🏗️ Mejora de la estructura MARC21
- Normalización de modelos
- Limpieza del modelo de serie 490

---

## [1.0.0] – 2024-12
### 🚀 Lanzamiento inicial
- Primera versión funcional  
- CRUD completo de obras  
- Formsets para bloques 0XX–8XX  
- Sistema de borradores  
