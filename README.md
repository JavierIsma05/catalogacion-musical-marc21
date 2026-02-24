# Biblioteca Latinoamericana de Musica para Pianos

Sistema de catalogación de obras musicales basado en el estándar MARC21, desarrollado con Django. Permite registrar, editar y administrar obras musicales con soporte para encabezamientos de materia, géneros/forma, autoridades, subcampos dinámicos y autocompletado inteligente.

---

## Requisitos previos

- Python 3.11+
- PostgreSQL 14+
- nginx
- Un servidor Linux (Ubuntu 22.04 recomendado)

---

## Instalación en desarrollo

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd catalogacion-musical-marc21

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (ver sección abajo)
cp .env.example .env
# Editar .env con los valores locales

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Correr servidor de desarrollo
python manage.py runserver
```

---

## Despliegue en producción

### 1. Preparar el servidor

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip nginx postgresql postgresql-contrib -y
```

### 2. Clonar y configurar el proyecto

```bash
# Clonar en /var/www/ o la ruta que defina TI
sudo mkdir -p /var/www/catalogacion
sudo chown $USER:$USER /var/www/catalogacion
git clone <url-del-repo> /var/www/catalogacion
cd /var/www/catalogacion

# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3. Variables de entorno

Crear el archivo `/var/www/catalogacion/.env`:

```env
SECRET_KEY=<clave-secreta-generada>
DEBUG=False
ALLOWED_HOSTS=<dominio-o-ip-del-servidor>

DB_NAME=catalogacion_db
DB_USER=catalogacion_user
DB_PASSWORD=<contraseña-segura>
DB_HOST=localhost
DB_PORT=5432

MEDIA_ROOT=/var/www/catalogacion/media/
```

> Para generar una SECRET_KEY segura:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

El archivo `settings.py` debe leer estas variables con `os.environ.get(...)`. Ver sección [Configurar settings para producción](#configurar-settings-para-producción).

### 4. Configurar PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE catalogacion_db;
CREATE USER catalogacion_user WITH PASSWORD '<contraseña-segura>';
ALTER ROLE catalogacion_user SET client_encoding TO 'utf8';
ALTER ROLE catalogacion_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE catalogacion_user SET timezone TO 'UTC';

\c catalogacion_db
GRANT CONNECT ON DATABASE catalogacion_db TO catalogacion_user;
GRANT USAGE ON SCHEMA public TO catalogacion_user;
GRANT CREATE ON SCHEMA public TO catalogacion_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO catalogacion_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO catalogacion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO catalogacion_user;
\q
```

### 5. Aplicar migraciones y archivos estáticos

```bash
cd /var/www/catalogacion
source venv/bin/activate

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Configurar Gunicorn como servicio systemd

Crear `/etc/systemd/system/catalogacion.service`:

```ini
[Unit]
Description=Gunicorn - Catalogacion Musical MARC21
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/catalogacion
EnvironmentFile=/var/www/catalogacion/.env
ExecStart=/var/www/catalogacion/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/catalogacion.sock \
    marc21_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable catalogacion
sudo systemctl start catalogacion
sudo systemctl status catalogacion
```

### 7. Configurar nginx

Crear `/etc/nginx/sites-available/catalogacion`:

```nginx
server {
    listen 80;
    server_name <dominio-o-ip>;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/catalogacion/staticfiles/;
    }

    location /media/ {
        alias /var/www/catalogacion/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/catalogacion.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/catalogacion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Configurar settings para producción

En `marc21_project/settings.py` ajustar para leer desde variables de entorno:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## Configuración de almacenamiento de medios (portadas y documentos)

### Opción A: Carpeta local / NAS montado

La opción más simple. Si TI monta un NAS en el servidor, solo se cambia `MEDIA_ROOT`:

```python
MEDIA_ROOT = "/mnt/nas/catalogacion/media/"  # ruta donde esté montado el NAS
MEDIA_URL = "/media/"
```

### Opción B: MinIO / S3 institucional

```bash
pip install django-storages boto3
```

```python
# settings.py
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET')
AWS_S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT')  # para MinIO
```

---

## Estructura del proyecto

```
catalogacion-musical-marc21/
├── catalogacion/          # App principal - Catalogación MARC21
│   ├── models/            # Modelos MARC21 (0XX-8XX)
│   ├── views/             # Vistas y lógica de negocio
│   ├── forms/             # Formularios y formsets
│   ├── templates/         # HTML templates
│   ├── static/            # JS y estilos
│   └── management/        # Comandos personalizados
├── usuarios/              # Gestión de usuarios y autenticación
├── catalogo_publico/      # Catálogo público (lectura)
├── digitalizacion/        # Gestión de digitalizaciones
├── marc21_project/        # Configuración del proyecto
├── media/                 # Archivos subidos (portadas, documentos)
└── manage.py
```

---

## Comandos útiles

```bash
# Migraciones
python manage.py makemigrations
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic

# Ver logs de gunicorn
sudo journalctl -u catalogacion -f

# Reiniciar servicio tras cambios
sudo systemctl restart catalogacion
```
