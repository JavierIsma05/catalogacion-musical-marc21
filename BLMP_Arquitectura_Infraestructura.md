
# Biblioteca Latinoamericana de Música para Piano (BLMP)
## Propuesta Técnica de Arquitectura e Infraestructura

---

# 1. Descripción General del Proyecto

BLMP es una plataforma especializada de catalogación musical basada en MARC 21 para música manuscrita e impresa.

Permite:

- Catalogación completa MARC21 (0XX–8XX)
- Gestión de autoridades
- Borradores de obras
- Validación de incipit musical
- Gestión de digitalizaciones (PDF, JPG, TIFF)
- API REST para servicios internos

---

# 2. Stack Tecnológico

- Framework: Django 5.2.x
- Lenguaje: Python 3.x
- Base de datos: PostgreSQL (producción)
- Frontend: Vanilla JS + Bootstrap
- API REST: Django REST Framework
- Procesamiento de imágenes: Pillow
- Driver PostgreSQL: psycopg

---

# 3. Arquitectura de Despliegue

## Modelo recomendado: 2 Máquinas Virtuales

### Esquema general

Internet (Usuarios)
        |
        | 443 (HTTPS)
        v
[Nginx - Reverse Proxy | VM-APP]
        |
        | proxy_pass -> 127.0.0.1:8001
        v
[Gunicorn + Django BLMP | VM-APP]
        |
        | 5432 (Red interna únicamente)
        v
[PostgreSQL | VM-DB]

---

# 4. Componentes

## VM-APP

- Linux (Ubuntu Server / Debian recomendado)
- Nginx (reverse proxy)
- Gunicorn (application server)
- Django BLMP
- Entorno virtual Python
- Staticfiles y media derivados

## VM-DB

- PostgreSQL
- Acceso restringido solo desde VM-APP

---

# 5. Rutas en VM-APP

STATIC_ROOT = /var/www/blmp/staticfiles
MEDIA_ROOT  = /var/www/blmp/media

---

# 6. Exposición a Internet

Se expone:
- Puerto 443 (HTTPS)
- Puerto 80 (opcional para redirección o Let's Encrypt)

No se expone:
- Gunicorn (127.0.0.1)
- PostgreSQL (solo red interna)
- Puerto 8000

---

# 7. Certificados y Dominio

## Opción 1 (Institucional - recomendada)

- DNS: blmp.<dominio_universidad>
- Certificado wildcard institucional
- Operación detrás del proxy oficial

## Opción 2 (Autogestionado)

- Nginx en VM-APP
- Let's Encrypt + Certbot

---

# 8. Requisitos de Infraestructura

## VM-APP
- 2 vCPU mínimo (ideal 4)
- 4 GB RAM mínimo (ideal 8)
- 70 GB SSD

## VM-DB
- 2 vCPU mínimo (ideal 4)
- 8 GB RAM
- 100 GB SSD inicial

---

# 9. Almacenamiento Digital

Recomendado:

- Derivados en /var/www/blmp/media
- TIFF master en NAS institucional montado como:

/mnt/blmp_master_tiff

---

# 10. Matriz de Puertos

## VM-APP
- 443 TCP (Internet o proxy)
- 80 TCP (opcional)
- 22 TCP (red TI/VPN)
- 5432 salida hacia VM-DB

## VM-DB
- 5432 TCP solo desde VM-APP
- 22 TCP red TI/VPN

---

# 11. Runbook de Despliegue

git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart blmp-gunicorn

---

# 12. Política Inicial de Backups

Base de datos:
- Diario (7 días)
- Semanal (4 semanas)
- Mensual (6 meses)
- Prueba de restauración mensual

Archivos:
- Snapshot o rsync diario
- Retención similar

---

# 13. Seguridad

- DEBUG=0
- SECRET_KEY fuera del repositorio
- DB no expuesta públicamente
- Firewall activo
- SSH restringido

---

# 14. Preguntas para TI

1. ¿Se utilizará proxy institucional?
2. ¿Certificado institucional o Let's Encrypt?
3. ¿Existe NAS institucional para TIFF master?
4. ¿Cuál es la política de backups institucional?
5. ¿Se dispone de monitoreo centralizado?

---

Documento preparado para reunión técnica con Departamento de TI.
