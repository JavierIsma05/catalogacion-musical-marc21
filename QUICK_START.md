# ⚡ QUICK START - 5 MINUTOS

## Elige tu rol y comienza

### 👤 Soy Catalogador
```bash
1. Lee MANUAL_DE_USO.md → sección "Acceso al Sistema"
2. Abre http://localhost:8000
3. Crea tu primer obra
4. ¡Listo!
```

### 👨‍💼 Soy Administrador
```bash
# Instalar
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configurar BD
python manage.py migrate
python manage.py createsuperuser

# Iniciar
python manage.py runserver

# Acceder a http://localhost:8000
# Admin en: http://localhost:8000/admin/
```

### 🚀 Soy DevOps
```bash
# Lee GUIA_PRODUCCION.md

# Elige tu opción:
# 1. Heroku → GUIA_PRODUCCION.md → "Opción 1"
# 2. DigitalOcean → GUIA_PRODUCCION.md → "Opción 2"  
# 3. VPS propio → GUIA_PRODUCCION.md → "Gunicorn + Nginx"
```

### 👨‍💻 Soy Desarrollador
```bash
# Lee GUIA_TECNICA.md → "Desarrollo"
# Lee EJEMPLOS_AVANZADOS.md → tu caso de uso

# Ejemplo: importar CSV
python manage.py importar_csv archivo.csv

# Ejemplo: crear API REST
# Ver sección "API REST Personalizada" en EJEMPLOS_AVANZADOS.md
```

---

## 📚 Documentos principales

| Documento | Para quién | Tiempo |
|-----------|-----------|--------|
| **MANUAL_DE_USO.md** | Catalogadores | 1-2 h |
| **GUIA_TECNICA.md** | Administradores | 2-3 h |
| **GUIA_PRODUCCION.md** | DevOps | 2-4 h |
| **EJEMPLOS_AVANZADOS.md** | Desarrolladores | 2-3 h |
| **INDICE_DOCUMENTACION.md** | Todos (mapa general) | 30 min |

---

## 🔗 URLs Importantes

```
Sistema: http://localhost:8000
Admin: http://localhost:8000/admin/
Crear obra: http://localhost:8000/catalogacion/crear/
Ver obras: http://localhost:8000/catalogacion/obras/
Autoridades: http://localhost:8000/catalogacion/autoridades/
```

---

## 🎯 Primeras acciones

### Crear tu primera obra (5 min)
```bash
1. Ir a http://localhost:8000/catalogacion/crear/
2. Seleccionar tipo: "Obra manuscrita individual"
3. Llenar campos:
   - Título: "Mi Primera Obra"
   - Número de Control: dejarlo vacío (genera automático)
4. Hacer click "Crear Obra"
5. ¡Hecho! Ya tienes una obra catalogada
```

### Crear una autoridad (3 min)
```bash
1. Ir a http://localhost:8000/catalogacion/autoridades/personas/
2. Click "Crear Persona"
3. Llenar:
   - Apellidos y nombres: "Beethoven, Ludwig van"
   - Coordenadas biográficas: "1770-1827"
4. Click "Guardar"
5. Ahora puedes usarla al crear obras
```

### Ver obras catalogadas (1 min)
```bash
1. Ir a http://localhost:8000/catalogacion/obras/
2. Verás lista de todas las obras
3. Click en una obra para ver detalles
4. Click "Editar" para modificar
```

---

## 🆘 Algo no funciona

### El servidor no inicia
```bash
# Solución 1
python manage.py migrate

# Solución 2
pip install -r requirements.txt --upgrade

# Solución 3 (Windows)
set DJANGO_SETTINGS_MODULE=marc21_project.settings
python manage.py runserver
```

### Error "No such table"
```bash
python manage.py migrate
```

### Puerto 8000 en uso
```bash
python manage.py runserver 8001
```

### Problema con usuario/contraseña
```bash
python manage.py changepassword username
```

---

## 📖 Si necesitas más ayuda

- **Catálogos y campos**: Ver MANUAL_DE_USO.md
- **Instalar/configurar**: Ver GUIA_TECNICA.md
- **Producción**: Ver GUIA_PRODUCCION.md
- **Extensiones**: Ver EJEMPLOS_AVANZADOS.md
- **Mapa general**: Ver INDICE_DOCUMENTACION.md

---

## ✅ Sistema listo

```
☑️ Sistema instalado
☑️ BD configurada
☑️ Server corriendo
☑️ Documentación completa
☑️ Ejemplos de prueba

👉 ¡Comienza a catalogar!
```

---

*Último step: Abre http://localhost:8000 en tu navegador* 🎵
