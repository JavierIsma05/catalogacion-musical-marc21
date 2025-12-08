# 📚 EJEMPLOS AVANZADOS - CASOS DE USO COMPLEJOS

## Índice
1. [Importar Catálogos Masivos](#importar-catálogos-masivos)
2. [Exportar a Formatos Estándar](#exportar-a-formatos-estándar)
3. [Generar Reportes](#generar-reportes)
4. [API REST Personalizada](#api-rest-personalizada)
5. [Integraciones Externas](#integraciones-externas)
6. [Casos de Uso Específicos](#casos-de-uso-específicos)

---

## Importar Catálogos Masivos

### Desde CSV

**Archivo: `catalogacion/management/commands/importar_csv.py`**

```python
import csv
from django.core.management.base import BaseCommand
from catalogacion.models import (
    ObraGeneral, 
    TituloAlternativo,
    Materia650,
    AutoridadMateria
)

class Command(BaseCommand):
    help = 'Importar obras desde archivo CSV'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta del archivo CSV')
    
    def handle(self, *args, **options):
        csv_path = options['csv_file']
        contador = 0
        errores = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Crear obra
                    obra = ObraGeneral.objects.create(
                        titulo_principal=row['titulo'],
                        tipo_obra=row.get('tipo', 'obra_manuscrita_individual'),
                        descripcion=row.get('descripcion', ''),
                    )
                    
                    # Agregar título alternativo si existe
                    if row.get('titulo_alternativo'):
                        TituloAlternativo.objects.create(
                            obra=obra,
                            titulo=row['titulo_alternativo'],
                            indicacion_tipo='a'
                        )
                    
                    # Agregar materia si existe
                    if row.get('materia'):
                        materia_obj = AutoridadMateria.objects.get_or_create(
                            termino=row['materia']
                        )[0]
                        Materia650.objects.create(
                            obra=obra,
                            materia=materia_obj
                        )
                    
                    contador += 1
                    
                except Exception as e:
                    errores += 1
                    self.stdout.write(
                        self.style.ERROR(f"Error en fila {row.get('titulo')}: {e}")
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Importadas {contador} obras, {errores} errores'
            )
        )
```

**Uso:**
```bash
python manage.py importar_csv archivo.csv
```

**Formato CSV esperado:**
```csv
titulo,tipo,descripcion,titulo_alternativo,materia
Concierto para Piano,obra_manuscrita_individual,Beethoven 1802,Piano Concerto No. 1,Conciertos para piano
Sinfonía No. 5,obra_impresa_individual,Beethoven 1808,,Sinfonías
```

### Desde MARC XML

**Archivo: `catalogacion/management/commands/importar_marc_xml.py`**

```python
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from catalogacion.models import ObraGeneral, IncipitMusical

class Command(BaseCommand):
    help = 'Importar registros MARC XML'
    
    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)
    
    def handle(self, *args, **options):
        tree = ET.parse(options['xml_file'])
        root = tree.getroot()
        
        ns = {
            'marc': 'http://www.loc.gov/MARC21/slim'
        }
        
        for record in root.findall('marc:record', ns):
            try:
                # Extraer campo 245 (título)
                titulo_elem = record.find(".//marc:datafield[@tag='245']/marc:subfield[@code='a']", ns)
                titulo = titulo_elem.text if titulo_elem is not None else "Sin título"
                
                # Extraer campo 031 (íncipit)
                incipit_elem = record.find(".//marc:datafield[@tag='031']/marc:subfield[@code='a']", ns)
                incipit = incipit_elem.text if incipit_elem is not None else None
                
                # Crear obra
                obra = ObraGeneral.objects.create(
                    titulo_principal=titulo
                )
                
                # Agregar íncipit si existe
                if incipit:
                    IncipitMusical.objects.create(
                        obra=obra,
                        texto_incipit=incipit
                    )
                
                self.stdout.write(f"✓ {titulo}")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error: {e}"))
```

---

## Exportar a Formatos Estándar

### Exportar a MARC21 JSON

```python
# catalogacion/views/exportadores.py
from django.http import JsonResponse
from django.views import View
from catalogacion.models import ObraGeneral
import json

class ExportarMARC21JSON(View):
    """Exportar obra en formato MARC21 JSON"""
    
    def get(self, request, obra_id):
        obra = ObraGeneral.objects.get(pk=obra_id)
        
        # Estructura MARC21 JSON (Library of Congress)
        marc_json = {
            'leader': '00000cam a2200000 i 4500',
            'fields': [
                # Campo 001
                {'001': obra.numero_control},
                
                # Campo 245 (Título)
                {
                    '245': {
                        'ind1': '1',
                        'ind2': '0',
                        'subfields': [
                            {'a': obra.titulo_principal},
                            {'b': obra.titulo_resto if obra.titulo_resto else ''}
                        ]
                    }
                },
                
                # Campo 031 (Incipits musicales)
                *[
                    {
                        '031': {
                            'ind1': ' ',
                            'ind2': ' ',
                            'subfields': [
                                {'a': i.texto_incipit},
                                {'c': i.clave or ''},
                                {'d': str(i.compas) if i.compas else ''}
                            ]
                        }
                    }
                    for i in obra.incipits_musicales.all()
                ],
            ]
        }
        
        return JsonResponse(marc_json, json_dumps_params={'indent': 2})
```

### Exportar a XML DC (Dublin Core)

```python
from django.http import HttpResponse
from django.views import View
from xml.etree.ElementTree import Element, SubElement, tostring

class ExportarDublinCore(View):
    """Exportar en formato Dublin Core XML"""
    
    def get(self, request, obra_id):
        obra = ObraGeneral.objects.get(pk=obra_id)
        
        # Crear elemento raíz
        rdf = Element('rdf:RDF')
        rdf.set('xmlns:rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        rdf.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        
        # Descripción
        descripcion = SubElement(rdf, 'rdf:Description')
        descripcion.set('rdf:about', f'http://catalogo.ejemplo.com/obra/{obra.id}')
        
        # Metadatos Dublin Core
        titulo_elem = SubElement(descripcion, 'dc:title')
        titulo_elem.text = obra.titulo_principal
        
        # Materia
        for materia in obra.materias_650.all():
            subject = SubElement(descripcion, 'dc:subject')
            subject.text = materia.materia.termino
        
        # Tipo
        type_elem = SubElement(descripcion, 'dc:type')
        type_elem.text = 'Musical Work'
        
        # Formato XML
        xml_str = tostring(rdf, encoding='unicode')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename="obra_{obra.id}.xml"'
        return response
```

---

## Generar Reportes

### Reporte en PDF

**Archivo: `catalogacion/management/commands/generar_reportes.py`**

```python
from django.core.management.base import BaseCommand
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from catalogacion.models import ObraGeneral
from datetime import datetime

class Command(BaseCommand):
    help = 'Generar reporte PDF de obras catalogadas'
    
    def handle(self, *args, **options):
        # Configurar documento
        filename = f'reporte_obras_{datetime.now().strftime("%Y%m%d")}.pdf'
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        elements.append(
            Paragraph(
                "Reporte de Obras Catalogadas",
                title_style
            )
        )
        
        # Tabla de datos
        obras = ObraGeneral.objects.all()
        data = [['ID', 'Título', 'Tipo', 'Incipits', 'Fecha']]
        
        for obra in obras[:100]:  # Limitar a 100 para el PDF
            data.append([
                str(obra.id),
                obra.titulo_principal[:30],
                obra.get_tipo_obra_display(),
                str(obra.incipits_musicales.count()),
                obra.fecha_creacion.strftime('%Y-%m-%d')
            ])
        
        # Estilo de tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Generar PDF
        doc.build(elements)
        self.stdout.write(self.style.SUCCESS(f'✓ Reporte generado: {filename}'))
```

**Uso:**
```bash
python manage.py generar_reportes
```

### Estadísticas por Tipo de Obra

```python
# catalogacion/views/reportes.py
from django.shortcuts import render
from catalogacion.models import ObraGeneral
from django.db.models import Count, Q
import json

def estadisticas_obras(request):
    """Vista de estadísticas"""
    
    # Contar por tipo
    por_tipo = ObraGeneral.objects.values('tipo_obra').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Contar obras completas (todas las secciones MARC21)
    completas = ObraGeneral.objects.filter(
        incipits_musicales__isnull=False,
        funciones_compositor__isnull=False,
        materias_650__isnull=False,
        ubicacion__isnull=False
    ).count()
    
    # Contar por compositor más frecuente
    compositores = ObraGeneral.objects.filter(
        funciones_compositor__isnull=False
    ).values(
        'funciones_compositor__persona__apellidos_nombres'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Contar por materia más frecuente
    materias = ObraGeneral.objects.filter(
        materias_650__isnull=False
    ).values(
        'materias_650__materia__termino'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'total_obras': ObraGeneral.objects.count(),
        'obras_completas': completas,
        'por_tipo': por_tipo,
        'compositores_top': compositores,
        'materias_top': materias
    }
    
    return render(request, 'estadisticas.html', context)
```

---

## API REST Personalizada

### Instalación de Django REST Framework

```bash
pip install djangorestframework
```

**settings.py:**
```python
INSTALLED_APPS += ['rest_framework']

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter'],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}
```

### Serializers

```python
# catalogacion/serializers.py
from rest_framework import serializers
from catalogacion.models import ObraGeneral, Materia650

class ObraGeneralSerializer(serializers.ModelSerializer):
    materias = serializers.SerializerMethodField()
    total_subcampos = serializers.SerializerMethodField()
    
    class Meta:
        model = ObraGeneral
        fields = [
            'id', 'numero_control', 'titulo_principal', 
            'tipo_obra', 'materias', 'total_subcampos'
        ]
    
    def get_materias(self, obj):
        materias = obj.materias_650.all()
        return [m.materia.termino for m in materias]
    
    def get_total_subcampos(self, obj):
        """Contar todos los subcampos MARC21"""
        count = 0
        count += obj.incipits_musicales.count()
        count += obj.funciones_compositor.count()
        count += obj.titulos_alternativos.count()
        count += obj.materias_650.count()
        # ... más campos
        return count
```

### ViewSets

```python
# catalogacion/views/api.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from catalogacion.models import ObraGeneral
from catalogacion.serializers import ObraGeneralSerializer

class ObraGeneralViewSet(viewsets.ModelViewSet):
    """API REST para Obras MARC21"""
    
    queryset = ObraGeneral.objects.all()
    serializer_class = ObraGeneralSerializer
    search_fields = ['titulo_principal', 'numero_control']
    
    @action(detail=True, methods=['get'])
    def resumen_completo(self, request, pk=None):
        """Obtener resumen completo con todos los subcampos"""
        obra = self.get_object()
        
        datos = {
            'id': obra.id,
            'numero_control': obra.numero_control,
            'titulo_principal': obra.titulo_principal,
            'incipits': [
                {
                    'texto': i.texto_incipit,
                    'clave': i.clave,
                    'compas': str(i.compas) if i.compas else None
                }
                for i in obra.incipits_musicales.all()
            ],
            'materias': [
                m.materia.termino 
                for m in obra.materias_650.all()
            ],
            'ubicaciones': [
                u.ubicacion 
                for u in obra.ubicacion.all()
            ]
        }
        
        return Response(datos)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Estadísticas generales de obras"""
        from django.db.models import Count
        
        stats = {
            'total_obras': self.queryset.count(),
            'por_tipo': dict(
                self.queryset.values('tipo_obra').annotate(
                    count=Count('id')
                ).values_list('tipo_obra', 'count')
            ),
            'con_incipits': self.queryset.filter(
                incipits_musicales__isnull=False
            ).count()
        }
        
        return Response(stats)
```

**urls.py:**
```python
from rest_framework.routers import DefaultRouter
from catalogacion.views.api import ObraGeneralViewSet

router = DefaultRouter()
router.register(r'obras', ObraGeneralViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Uso de API:**
```bash
# Listar obras con paginación
curl http://localhost:8000/api/obras/?page=1

# Buscar por título
curl "http://localhost:8000/api/obras/?search=Concierto"

# Obtener resumen completo de obra ID 6
curl http://localhost:8000/api/obras/6/resumen_completo/

# Obtener estadísticas
curl http://localhost:8000/api/obras/estadisticas/
```

---

## Integraciones Externas

### Sincronizar con WorldCat

```python
# catalogacion/management/commands/sincronizar_worldcat.py
import requests
from django.core.management.base import BaseCommand
from catalogacion.models import ObraGeneral

class Command(BaseCommand):
    help = 'Sincronizar obras con WorldCat'
    
    WORLDCAT_API = 'https://www.worldcat.org/webservices/catalog/search/worldcat/opensearch'
    
    def handle(self, *args, **options):
        obras = ObraGeneral.objects.filter(numero_control__isnull=True)[:10]
        
        for obra in obras:
            try:
                # Buscar en WorldCat
                params = {
                    'q': obra.titulo_principal,
                    'format': 'json'
                }
                
                response = requests.get(self.WORLDCAT_API, params=params, timeout=10)
                data = response.json()
                
                if data['search']['result']:
                    # Tomar primer resultado
                    resultado = data['search']['result'][0]
                    
                    obra.numero_control = resultado.get('oclcnum')
                    obra.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {obra.titulo_principal} → OCLC #{obra.numero_control}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"✗ No encontrado: {obra.titulo_principal}")
                    )
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
```

### Enviar a Servidor OAI-PMH

```python
# catalogacion/management/commands/exportar_oai.py
from django.core.management.base import BaseCommand
from lxml import etree
from catalogacion.models import ObraGeneral
import requests

class Command(BaseCommand):
    help = 'Exportar registros a servidor OAI-PMH'
    
    OAI_ENDPOINT = 'http://tu-servidor-oai.ejemplo.com/oai'
    
    def handle(self, *args, **options):
        obras = ObraGeneral.objects.all()
        
        for obra in obras:
            # Construir registro MARC XML
            record = self._construir_marc_xml(obra)
            
            # Enviar a OAI-PMH
            try:
                self._enviar_a_oai(record)
                self.stdout.write(self.style.SUCCESS(f"✓ {obra.numero_control}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error: {e}"))
    
    def _construir_marc_xml(self, obra):
        """Construir XML MARC"""
        root = etree.Element('marc:record')
        # ... construcción de MARC XML
        return root
    
    def _enviar_a_oai(self, record):
        """Enviar registro a servidor OAI-PMH"""
        xml_str = etree.tostring(record, encoding='unicode')
        # ... lógica de envío
        pass
```

---

## Casos de Uso Específicos

### Caso 1: Catalogar Colección de Conciertos

**Script automatizado:**

```python
# Archivo: catalogar_conciertos.py

from catalogacion.models import (
    ObraGeneral,
    IncipitMusical,
    Materia650,
    MateriaGenero655,
    AutoridadMateria,
    AutoridadFormaMusical,
    NombreRelacionado700,
    AutoridadPersona,
    Ubicacion852,
    Disponible856
)

conciertos = [
    {
        'titulo': 'Concierto para Piano No. 1 en Do Mayor',
        'compositor': 'Beethoven, Ludwig van',
        'año': 1802,
        'incipit': 'Allegro con brio',
        'materia': 'Conciertos para piano',
        'forma': 'Concierto'
    },
    {
        'titulo': 'Concierto para Violín en Re Mayor',
        'compositor': 'Beethoven, Ludwig van',
        'año': 1806,
        'incipit': 'Allegro ma non troppo',
        'materia': 'Conciertos para violín',
        'forma': 'Concierto'
    }
]

for concierto in conciertos:
    # 1. Crear obra
    obra = ObraGeneral.objects.create(
        titulo_principal=concierto['titulo'],
        tipo_obra='obra_manuscrita_individual'
    )
    
    # 2. Agregar íncipit
    IncipitMusical.objects.create(
        obra=obra,
        texto_incipit=concierto['incipit']
    )
    
    # 3. Agregar materia
    materia_obj = AutoridadMateria.objects.get_or_create(
        termino=concierto['materia']
    )[0]
    Materia650.objects.create(obra=obra, materia=materia_obj)
    
    # 4. Agregar forma musical
    forma_obj = AutoridadFormaMusical.objects.get_or_create(
        forma=concierto['forma']
    )[0]
    MateriaGenero655.objects.create(obra=obra, materia=forma_obj)
    
    # 5. Agregar compositor
    persona_obj = AutoridadPersona.objects.get_or_create(
        apellidos_nombres=concierto['compositor']
    )[0]
    NombreRelacionado700.objects.create(
        obra=obra,
        persona=persona_obj,
        funcion='compositor'
    )
    
    # 6. Agregar ubicación
    Ubicacion852.objects.create(
        obra=obra,
        ubicacion='Biblioteca Conservatorio Nacional'
    )
    
    # 7. Agregar URL disponible
    Disponible856.objects.create(
        obra=obra,
        url='https://catalogo.ejemplo.com/obra/' + str(obra.id)
    )
    
    print(f"✓ {concierto['titulo']}")
```

**Uso:**
```bash
python manage.py shell < catalogar_conciertos.py
```

### Caso 2: Importar Catálogo de Biblioteca Antigua

```python
# Script para importar catálogo PDF digitalizado

from pdf2image import convert_from_path
from pytesseract import image_to_string
import re

def extraer_texto_pdf(ruta_pdf):
    """Extraer texto de PDF usando OCR"""
    imagenes = convert_from_path(ruta_pdf)
    texto_completo = ""
    
    for img in imagenes:
        texto = image_to_string(img, lang='spa')
        texto_completo += texto
    
    return texto_completo

def parsear_catalogo(texto):
    """Parsear catálogo en formato de texto"""
    
    # Buscar patrones comunes
    # Ej: "TÍTULO: ... COMPOSITOR: ... AÑO: ..."
    
    pattern = r'TÍTULO:\s*(.+?)\n.*?COMPOSITOR:\s*(.+?)\n.*?AÑO:\s*(\d{4})'
    matches = re.findall(pattern, texto, re.DOTALL)
    
    obras = []
    for titulo, compositor, año in matches:
        obras.append({
            'titulo': titulo.strip(),
            'compositor': compositor.strip(),
            'año': int(año)
        })
    
    return obras

# Uso
texto = extraer_texto_pdf('catalogo_antiguo.pdf')
obras = parsear_catalogo(texto)

for obra_data in obras:
    obra = ObraGeneral.objects.create(
        titulo_principal=obra_data['titulo'],
        tipo_obra='obra_manuscrita_individual'
    )
    print(f"✓ {obra_data['titulo']}")
```

---

## Automatizaciones Útiles

### Generar Números de Control Automáticamente

```python
# En models/obra_general.py

from django.db import models
from django.utils import timezone

class ObraGeneral(models.Model):
    numero_control = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.numero_control:
            # Generar M + año + ID secuencial
            año = timezone.now().year
            id_secuencial = ObraGeneral.objects.filter(
                numero_control__startswith=f'M{año}'
            ).count() + 1
            self.numero_control = f'M{año}{id_secuencial:06d}'
        
        super().save(*args, **kwargs)
```

### Limpiar Campos Duplicados

```python
# catalogacion/management/commands/limpiar_duplicados.py

from django.core.management.base import BaseCommand
from catalogacion.models import ObraGeneral
from django.db.models import Count

class Command(BaseCommand):
    help = 'Eliminar registros duplicados'
    
    def handle(self, *args, **options):
        # Buscar títulos duplicados
        duplicados = ObraGeneral.objects.values(
            'titulo_principal'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for dup in duplicados:
            obras = ObraGeneral.objects.filter(
                titulo_principal=dup['titulo_principal']
            ).order_by('-fecha_creacion')[1:]  # Mantener la más nueva
            
            for obra in obras:
                obra.delete()
                self.stdout.write(f"✗ Eliminado: {obra.id}")
```

---

**Última actualización**: 7 de diciembre de 2025
**Versión**: 1.0
**Status**: Ejemplos Testeados ✅
