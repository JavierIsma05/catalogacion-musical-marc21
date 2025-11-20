# 🎼 Sistema de Catalogación Musical MARC21

Proyecto Django para la catalogación de obras musicales basado en el
estándar MARC21.

Este sistema permite registrar, editar y administrar obras musicales
siguiendo la estructura oficial MARC21, incluyendo encabezamientos de
materia, géneros/forma, autoridades, enlaces 7xx, y notas 5xx, con
soporte para autocompletado inteligente y subcampos dinámicos.

## 🚀 Características principales

# 🏛️ Arquitectura general del proyecto
catalogacion/
│── models/ → Modelos MARC21 (0XX–8XX)
│── views/ → Lógica de creación, edición, detalle y listado
│── forms/ → Formulario principal + formsets
│── templates/ → Plantillas HTML
│── static/ → JS dinámico y estilos
│── api/ → Endpoints de autocompletado


---

# 🎼 MODELOS MARC21 (RESUMEN COMPLETO)

### **0XX – Control**
- Incipit Musical
- Código de lengua
- Código de país

### **1XX – Encabezamiento principal**
- Función de compositor (campo 100 modificado → `AutoridadPersona`)

### **2XX – Títulos**
- Títulos alternativos
- Edición
- Producción y publicación (264)

### **3XX – Descripción física**
- Medios de interpretación (382)  
  → Con subcampo dinámico `$a` fijo desde JS

### **4XX – Mención de serie (490)**  
- Títulos de serie  
- Volúmenes de serie  

### **5XX – Notas (500, 505, 520, 545)**  
- Nota general  
- Contenido  
- Sumario  
- Datos biográficos  
- URIs biográficas

### **6XX – Materia y Género (650–655)**  
- Materias 650 con subdivisiones dinámicas `$x`  
- Género/forma 655 con subdivisiones dinámicas `$x`

### **7XX – Asientos secundarios (IMPORTANTE)**  
- Nombre relacionado 700  
- Entidad relacionada 710  
- Enlace a documento fuente 773  
- Enlace a unidad constituyente 774  
- Otras relaciones 787  

**⚠️ Nota:**  
Se reemplazó el modelo anterior `EncabezamientoEnlace` por **AutoridadPersona**, ya que los campos 700/600/100 deben ser consistentes como autoridades personales.

### **8XX – Ubicación y acceso electrónico**
- Ubicación física 852  
- Disponible/URL 856  

---

# 🧩 Funcionamiento de los Formsets

Cada bloque MARC21 funciona como un formset independiente.  
La vista usa `ObraFormsetMixin` para:

✔️ Inicializarlos  
✔️ Validarlos  
✔️ Guardarlos  
✔️ Procesar subcampos dinámicos mediante handlers

Ejemplo del formset 650:

