# 🚀 GUÍA DE PRODUCCIÓN - DEPLOYMENT Y MONITOREO

## Índice
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Configuración de Producción](#configuración-de-producción)
3. [Deployment](#deployment)
4. [Seguridad](#seguridad)
5. [Monitoreo](#monitoreo)
6. [Respaldo y Recuperación](#respaldo-y-recuperación)

---

## Pre-Deployment Checklist

### ✓ Código
- [ ] Todos los tests pasan: `python manage.py test`
- [ ] Sin warnings de linting: `pylint catalogacion/`
- [ ] Sin imports no utilizados
- [ ] Docstrings en todas las funciones
- [ ] Configuración de DEBUG = False

### ✓ Base de Datos
- [ ] Migraciones actualizadas: `python manage.py migrate`
- [ ] Datos de prueba eliminados
- [ ] Índices creados para campos principales
- [ ] Backup realizado

### ✓ Estáticos
- [ ] Archivos CSS/JS compilados: `python manage.py collectstatic`
- [ ] Sin errores 404 en assets
- [ ] Caché habilitado en navegador

### ✓ Dependencias
- [ ] requirements.txt actualizado
- [ ] Python 3.10+ instalado en servidor
- [ ] Todas las librerías verificadas

### ✓ Documentación
- [ ] README.md actualizado
- [ ] MANUAL_DE_USO.md accesible
- [ ] APIs documentadas
- [ ] Contacto de soporte definido

---

## Configuración de Producción

### settings.py - Cambios Requeridos

```python
# SEGURIDAD
DEBUG = False
ALLOWED_HOSTS = ['ejemplo.com', 'www.ejemplo.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # ¡NO hardcodear!

# BASE DE DATOS (PostgreSQL recomendado)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# CACHÉ
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}

# MEDIA STORAGE (S3 opcional)
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Variables de Entorno (.env)

```bash
# Django
SECRET_KEY=tu-clave-secreta-super-larga-aqui
DEBUG=False
ALLOWED_HOSTS=ejemplo.com,www.ejemplo.com

# Base de Datos PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=catalogacion_prod
DB_USER=catalogacion_user
DB_PASSWORD=contraseña-fuerte-aqui
DB_HOST=localhost
DB_PORT=5432

# Redis Cache
REDIS_URL=redis://localhost:6379/1

# Email (para notificaciones)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-app

# AWS S3 (opcional para archivos)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=tu-bucket
```

---

## Deployment

### Opción 1: Heroku

```bash
# 1. Instalar Heroku CLI
# 2. Login
heroku login

# 3. Crear app
heroku create mi-app-catalogacion

# 4. Configurar variables de entorno
heroku config:set DJANGO_SETTINGS_MODULE=marc21_project.settings
heroku config:set SECRET_KEY=tu-clave-secreta

# 5. Agregar Procfile
echo "web: gunicorn marc21_project.wsgi" > Procfile

# 6. Agregar requirements.txt
pip freeze > requirements.txt

# 7. Commit y deploy
git add .
git commit -m "Preparar para Heroku"
git push heroku main

# 8. Ejecutar migraciones
heroku run python manage.py migrate
```

### Opción 2: DigitalOcean App Platform

```bash
# 1. Crear droplet con Ubuntu 22.04
# 2. SSH al servidor
ssh root@tu-ip

# 3. Actualizar sistema
apt update && apt upgrade -y

# 4. Instalar dependencias
apt install -y python3.10 python3.10-venv postgresql postgresql-contrib nginx redis-server

# 5. Crear usuario Django
useradd -m -s /bin/bash catalogacion

# 6. Clonar repo
cd /home/catalogacion
sudo -u catalogacion git clone https://github.com/JavierIsma05/catalogacion-musical-marc21.git
cd catalogacion-musical-marc21

# 7. Crear venv
sudo -u catalogacion python3.10 -m venv venv

# 8. Instalar dependencias
sudo -u catalogacion venv/bin/pip install -r requirements.txt

# 9. Recolectar estáticos
sudo -u catalogacion venv/bin/python manage.py collectstatic --noinput

# 10. Configurar Gunicorn (systemd)
# Ver sección Gunicorn abajo

# 11. Configurar Nginx (ver sección Nginx)

# 12. SSL con Let's Encrypt
apt install -y certbot python3-certbot-nginx
certbot --nginx -d ejemplo.com
```

### Gunicorn (systemd service)

**Archivo: `/etc/systemd/system/catalogacion.service`**

```ini
[Unit]
Description=Catalogación Musical MARC21
After=network.target

[Service]
Type=notify
User=catalogacion
Group=www-data
WorkingDirectory=/home/catalogacion/catalogacion-musical-marc21
Environment="PATH=/home/catalogacion/catalogacion-musical-marc21/venv/bin"
EnvironmentFile=/home/catalogacion/.env
ExecStart=/home/catalogacion/catalogacion-musical-marc21/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind unix:/run/gunicorn.sock \
    marc21_project.wsgi:application

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

**Activar servicio:**
```bash
systemctl daemon-reload
systemctl enable catalogacion
systemctl start catalogacion
systemctl status catalogacion
```

### Nginx (reverse proxy)

**Archivo: `/etc/nginx/sites-available/catalogacion`**

```nginx
upstream catalogacion {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name ejemplo.com www.ejemplo.com;
    
    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ejemplo.com www.ejemplo.com;
    
    # SSL Certificate (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/ejemplo.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ejemplo.com/privkey.pem;
    
    client_max_body_size 20M;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    location /static/ {
        alias /home/catalogacion/catalogacion-musical-marc21/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/catalogacion/catalogacion-musical-marc21/media/;
    }
    
    location / {
        proxy_pass http://catalogacion;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }
}
```

**Activar:**
```bash
ln -s /etc/nginx/sites-available/catalogacion /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## Seguridad

### 1. Contraseñas Fuertes

```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### 2. Firewall

```bash
# UFW (Ubuntu)
ufw enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
```

### 3. Backup Automático

```bash
#!/bin/bash
# /home/catalogacion/backup.sh

BACKUP_DIR="/backups/catalogacion"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup BD PostgreSQL
pg_dump -U catalogacion_user catalogacion_prod | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup archivos media
tar czf $BACKUP_DIR/media_$DATE.tar.gz /home/catalogacion/catalogacion-musical-marc21/media/

# Eliminar backups antiguos (>30 días)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completado: $DATE" >> /var/log/backup.log
```

**Cron job:**
```bash
0 2 * * * /home/catalogacion/backup.sh
```

### 4. Monitoreo de Seguridad

```bash
# Verificar conexiones abiertas
netstat -tulpn | grep LISTEN

# Ver logs de acceso
tail -f /var/log/nginx/access.log

# Verificar archivos modificados
find /home/catalogacion -type f -mtime -1

# Scan de puertos abiertos
nmap -p- localhost
```

---

## Monitoreo

### Health Check

```python
# catalogacion/views/base.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection

@require_http_methods(["GET"])
def health_check(request):
    """Verificar estado del sistema"""
    try:
        # Probar BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

**En urls.py:**
```python
path('health/', health_check, name='health_check'),
```

### Métricas Básicas

```python
# catalogacion/management/commands/metricas.py
from django.core.management.base import BaseCommand
from catalogacion.models import ObraGeneral
from django.db.models import Count

class Command(BaseCommand):
    def handle(self, *args, **options):
        total_obras = ObraGeneral.objects.count()
        obras_incompletas = ObraGeneral.objects.filter(
            incipits_musicales__isnull=True
        ).count()
        
        por_tipo = ObraGeneral.objects.values('tipo_obra').annotate(
            count=Count('id')
        )
        
        print(f"Total obras: {total_obras}")
        print(f"Incompletas: {obras_incompletas}")
        print(f"\nPor tipo:")
        for item in por_tipo:
            print(f"  {item['tipo_obra']}: {item['count']}")
```

**Ejecutar diariamente:**
```bash
0 0 * * * /home/catalogacion/catalogacion-musical-marc21/venv/bin/python manage.py metricas >> /var/log/metricas.log
```

### Monitoreo con Sentry (Errores)

```bash
# 1. Crear cuenta en sentry.io
# 2. Instalar SDK
pip install sentry-sdk

# 3. Configurar settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

---

## Respaldo y Recuperación

### Backup Completo

```bash
#!/bin/bash
# Full backup script

BACKUP_DIR="/backups/catalogacion"
RETENTION_DAYS=30

mkdir -p $BACKUP_DIR

# PostgreSQL dump
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$(date +%Y%m%d).sql.gz

# Media files
tar czf $BACKUP_DIR/media_$(date +%Y%m%d).tar.gz /path/to/media/

# Código (si es necesario)
cd /home/catalogacion/catalogacion-musical-marc21
git archive --format=tar.gz --output=$BACKUP_DIR/code_$(date +%Y%m%d).tar.gz HEAD

# Limpiar backups antiguos
find $BACKUP_DIR -type f -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completado" >> /var/log/backup.log
```

### Restaurar Base de Datos

```bash
# 1. Detener aplicación
systemctl stop catalogacion

# 2. Restaurar BD
gunzip -c /backups/catalogacion/db_20251207.sql.gz | psql -U catalogacion_user catalogacion_prod

# 3. Restaurar media
cd /home/catalogacion/catalogacion-musical-marc21
tar xzf /backups/catalogacion/media_20251207.tar.gz

# 4. Iniciar aplicación
systemctl start catalogacion
```

### Verificar Integridad

```bash
# Verificar BD
python manage.py dbshell < /dev/null

# Verificar estáticos
ls -la staticfiles/

# Verificar media
du -sh media/

# Verificar permisos
ls -la | grep catalogacion
```

---

## Logs y Debugging

### Ver Logs en Tiempo Real

```bash
# Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Aplicación
journalctl -u catalogacion -f

# Sistema
dmesg | tail -20
```

### Analizar Errores

```bash
# Buscar errores en últimas 24h
journalctl -u catalogacion --since "24 hours ago" | grep ERROR

# Contar errores por tipo
journalctl -u catalogacion | grep ERROR | cut -d':' -f3 | sort | uniq -c | sort -rn

# Salvar log a archivo
journalctl -u catalogacion > /tmp/catalogacion.log
```

---

## Performance

### Optimizaciones de BD

```sql
-- Crear índices
CREATE INDEX idx_obra_titulo ON catalogacion_obrageneral(titulo_principal);
CREATE INDEX idx_obra_tipo ON catalogacion_obrageneral(tipo_obra);
CREATE INDEX idx_materia_obra ON catalogacion_materia650(obra_id);

-- Analizar tabla
ANALYZE catalogacion_obrageneral;

-- Ver tamaño de tablas
SELECT schemaname, tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Caché de Resultados

```python
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Vista cacheada
@cache_page(60*15)  # 15 minutos
def lista_obras(request):
    return render(request, 'lista_obras.html')

# Cache manual
def obtener_obras():
    obras = cache.get('todas_las_obras')
    if obras is None:
        obras = ObraGeneral.objects.all()[:100]
        cache.set('todas_las_obras', obras, 60*60)  # 1 hora
    return obras
```

---

## Checklist Post-Deployment

- [ ] Health check respondiendo correctamente
- [ ] Certificado SSL válido
- [ ] Logs sin errores en las últimas 24h
- [ ] Backup automático funcionando
- [ ] Métrica de disponibilidad > 99%
- [ ] Página de login accesible
- [ ] Creación de obra completable
- [ ] Base de datos accesible
- [ ] Email de notificaciones funcionando
- [ ] Usuarios pueden recuperar contraseña

---

**Última actualización**: 7 de diciembre de 2025
**Versión**: 1.0
**Status**: Listo para Producción ✅
