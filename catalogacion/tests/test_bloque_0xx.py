"""
Tests para el bloque 0XX - Números de control e información codificada.

Prueba el guardado correcto de:
- 028 Incipit Musical (repetible)
- 041 Código de lengua (repetible)
- 044 Código de país de entidad productora/publicación (repetible)
"""
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User

from catalogacion.models import (
    ObraGeneral,
    IncipitMusical,
    CodigoLengua,
    CodigoPaisEntidad,
)
from catalogacion.models.autoridades import AutoridadPersona


class Bloque0XXCreateTestCase(TransactionTestCase):
    """
    Tests para creación de obras con campos del bloque 0XX.
    Usa TransactionTestCase para probar transacciones atómicas.
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear compositor de prueba
        self.compositor = AutoridadPersona.objects.create(
            apellidos_nombres="Bach, Johann Sebastian",
            fechas="1685-1750"
        )
    
    def _get_base_obra_data(self, tipo_obra='obra_manuscrita_individual'):
        """
        Obtener datos base para crear una obra.
        
        Args:
            tipo_obra: Tipo de obra según TIPO_OBRA_CONFIG
        
        Returns:
            dict: Datos base del formulario
        """
        return {
            # Campos ocultos de configuración
            'tipo_registro': 'd' if 'manuscrita' in tipo_obra else 'c',
            'nivel_bibliografico': 'm',
            
            # Campo 001 - Número de control
            'num_control': 'TEST-001',
            
            # Campo 100 - Compositor (campo principal de entrada)
            'compositor': self.compositor.id,
            
            # Campo 240 - Título uniforme
            'titulo_uniforme_obra': 'Sonata para piano',
            'medio_interpretacion_uniforme': 'Piano',
            
            # Campo 245 - Título principal
            'titulo_principal': 'Sonata en Do Mayor',
            'subtitulo_principal': 'Para piano solo',
            
            # Campo 260/264 - Publicación
            'lugar_publicacion': 'Leipzig',
            'nombre_editor': 'Breitkopf & Härtel',
            'fecha_publicacion': '1850',
            
            # Management forms para formsets vacíos (requeridos)
            'incipits-TOTAL_FORMS': '0',
            'incipits-INITIAL_FORMS': '0',
            'lenguas-TOTAL_FORMS': '0',
            'lenguas-INITIAL_FORMS': '0',
            'paises-TOTAL_FORMS': '0',
            'paises-INITIAL_FORMS': '0',
            'funciones-TOTAL_FORMS': '0',
            'funciones-INITIAL_FORMS': '0',
            'titulos_alt-TOTAL_FORMS': '0',
            'titulos_alt-INITIAL_FORMS': '0',
            'ediciones-TOTAL_FORMS': '0',
            'ediciones-INITIAL_FORMS': '0',
            'produccion-TOTAL_FORMS': '0',
            'produccion-INITIAL_FORMS': '0',
            'medios_382-TOTAL_FORMS': '0',
            'medios_382-INITIAL_FORMS': '0',
            'menciones_490-TOTAL_FORMS': '0',
            'menciones_490-INITIAL_FORMS': '0',
            'notas_500-TOTAL_FORMS': '0',
            'notas_500-INITIAL_FORMS': '0',
            'contenidos_505-TOTAL_FORMS': '0',
            'contenidos_505-INITIAL_FORMS': '0',
            'sumarios_520-TOTAL_FORMS': '0',
            'sumarios_520-INITIAL_FORMS': '0',
            'biograficos_545-TOTAL_FORMS': '0',
            'biograficos_545-INITIAL_FORMS': '0',
            'materias_650-TOTAL_FORMS': '0',
            'materias_650-INITIAL_FORMS': '0',
            'generos_655-TOTAL_FORMS': '0',
            'generos_655-INITIAL_FORMS': '0',
            'nombres_700-TOTAL_FORMS': '0',
            'nombres_700-INITIAL_FORMS': '0',
            'entidades_710-TOTAL_FORMS': '0',
            'entidades_710-INITIAL_FORMS': '0',
            'enlaces_773-TOTAL_FORMS': '0',
            'enlaces_773-INITIAL_FORMS': '0',
            'enlaces_774-TOTAL_FORMS': '0',
            'enlaces_774-INITIAL_FORMS': '0',
            'relaciones_787-TOTAL_FORMS': '0',
            'relaciones_787-INITIAL_FORMS': '0',
            'ubicaciones_852-TOTAL_FORMS': '0',
            'ubicaciones_852-INITIAL_FORMS': '0',
            'disponibles_856-TOTAL_FORMS': '0',
            'disponibles_856-INITIAL_FORMS': '0',
        }
    
    def test_crear_obra_sin_bloque_0xx(self):
        """Test: Crear obra sin campos del bloque 0XX"""
        data = self._get_base_obra_data()
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        # Verificar redirección exitosa
        self.assertEqual(response.status_code, 302)
        
        # Verificar que la obra se creó
        self.assertEqual(ObraGeneral.objects.count(), 1)
        obra = ObraGeneral.objects.first()
        
        # Verificar campos básicos
        self.assertEqual(obra.num_control, 'TEST-001')
        self.assertEqual(obra.titulo_principal, 'Sonata en Do Mayor')
        self.assertEqual(obra.compositor, self.compositor)
        
        # Verificar que no hay campos del bloque 0XX
        self.assertEqual(obra.incipits_musicales.count(), 0)
        self.assertEqual(obra.codigos_lengua.count(), 0)
        self.assertEqual(obra.codigos_pais.count(), 0)
    
    def test_crear_obra_con_incipit_musical_unico(self):
        """Test: Crear obra con un incipit musical (028)"""
        data = self._get_base_obra_data()
        
        # Agregar un incipit musical
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-0-codigo_incipit': 'BWV 1001',
            'incipits-0-fuente_incipit': 'Bach-Werke-Verzeichnis',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        self.assertIsNotNone(obra)
        
        # Verificar incipit creado
        self.assertEqual(obra.incipits_musicales.count(), 1)
        incipit = obra.incipits_musicales.first()
        self.assertEqual(incipit.codigo_incipit, 'BWV 1001')
        self.assertEqual(incipit.fuente_incipit, 'Bach-Werke-Verzeichnis')
    
    def test_crear_obra_con_multiples_incipits_musicales(self):
        """Test: Crear obra con múltiples incipits musicales (campo repetible)"""
        data = self._get_base_obra_data()
        
        # Agregar tres incipits musicales
        data.update({
            'incipits-TOTAL_FORMS': '3',
            'incipits-0-codigo_incipit': 'BWV 1001',
            'incipits-0-fuente_incipit': 'Bach-Werke-Verzeichnis',
            'incipits-1-codigo_incipit': 'Op. 1',
            'incipits-1-fuente_incipit': 'Catálogo del compositor',
            'incipits-2-codigo_incipit': 'HWV 1',
            'incipits-2-fuente_incipit': 'Händel-Werke-Verzeichnis',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar que se crearon los 3 incipits
        self.assertEqual(obra.incipits_musicales.count(), 3)
        
        incipits = list(obra.incipits_musicales.all().order_by('id'))
        self.assertEqual(incipits[0].codigo_incipit, 'BWV 1001')
        self.assertEqual(incipits[1].codigo_incipit, 'Op. 1')
        self.assertEqual(incipits[2].codigo_incipit, 'HWV 1')
    
    def test_crear_obra_con_codigo_lengua_unico(self):
        """Test: Crear obra con un código de lengua (041)"""
        data = self._get_base_obra_data()
        
        # Agregar código de lengua
        data.update({
            'lenguas-TOTAL_FORMS': '1',
            'lenguas-0-codigo_lengua_texto': 'spa',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_impresa_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar código de lengua
        self.assertEqual(obra.codigos_lengua.count(), 1)
        lengua = obra.codigos_lengua.first()
        self.assertEqual(lengua.codigo_lengua_texto, 'spa')
    
    def test_crear_obra_con_multiples_codigos_lengua(self):
        """Test: Crear obra con múltiples códigos de lengua (campo repetible)"""
        data = self._get_base_obra_data()
        
        # Agregar múltiples códigos de lengua
        data.update({
            'lenguas-TOTAL_FORMS': '3',
            'lenguas-0-codigo_lengua_texto': 'spa',
            'lenguas-1-codigo_lengua_texto': 'eng',
            'lenguas-2-codigo_lengua_texto': 'fre',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'coleccion_impresa'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar códigos de lengua
        self.assertEqual(obra.codigos_lengua.count(), 3)
        lenguas = list(obra.codigos_lengua.all().order_by('id'))
        self.assertEqual(lenguas[0].codigo_lengua_texto, 'spa')
        self.assertEqual(lenguas[1].codigo_lengua_texto, 'eng')
        self.assertEqual(lenguas[2].codigo_lengua_texto, 'fre')
    
    def test_crear_obra_con_codigo_pais_unico(self):
        """Test: Crear obra con un código de país (044)"""
        data = self._get_base_obra_data()
        
        # Agregar código de país
        data.update({
            'paises-TOTAL_FORMS': '1',
            'paises-0-codigo_pais': 'gw',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar código de país
        self.assertEqual(obra.codigos_pais.count(), 1)
        pais = obra.codigos_pais.first()
        self.assertEqual(pais.codigo_pais, 'gw')
    
    def test_crear_obra_con_multiples_codigos_pais(self):
        """Test: Crear obra con múltiples códigos de país (campo repetible)"""
        data = self._get_base_obra_data()
        
        # Agregar múltiples códigos de país
        data.update({
            'paises-TOTAL_FORMS': '2',
            'paises-0-codigo_pais': 'gw',
            'paises-1-codigo_pais': 'au',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'coleccion_manuscrita'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar códigos de país
        self.assertEqual(obra.codigos_pais.count(), 2)
        paises = list(obra.codigos_pais.all().order_by('id'))
        self.assertEqual(paises[0].codigo_pais, 'gw')
        self.assertEqual(paises[1].codigo_pais, 'au')
    
    def test_crear_obra_con_bloque_0xx_completo(self):
        """Test: Crear obra con todos los campos del bloque 0XX"""
        data = self._get_base_obra_data()
        
        # Agregar todos los campos del bloque 0XX
        data.update({
            # Incipits musicales
            'incipits-TOTAL_FORMS': '2',
            'incipits-0-codigo_incipit': 'BWV 1001',
            'incipits-0-fuente_incipit': 'Bach-Werke-Verzeichnis',
            'incipits-1-codigo_incipit': 'Op. 1',
            'incipits-1-fuente_incipit': 'Catálogo del compositor',
            
            # Códigos de lengua
            'lenguas-TOTAL_FORMS': '2',
            'lenguas-0-codigo_lengua_texto': 'spa',
            'lenguas-1-codigo_lengua_texto': 'lat',
            
            # Códigos de país
            'paises-TOTAL_FORMS': '1',
            'paises-0-codigo_pais': 'gw',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        
        # Verificar todos los campos
        self.assertEqual(obra.incipits_musicales.count(), 2)
        self.assertEqual(obra.codigos_lengua.count(), 2)
        self.assertEqual(obra.codigos_pais.count(), 1)
    
    def test_crear_obra_manuscrita_individual_con_0xx(self):
        """Test: Crear obra manuscrita individual con bloque 0XX"""
        data = self._get_base_obra_data(tipo_obra='obra_manuscrita_individual')
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-0-codigo_incipit': 'MS-001',
            'incipits-0-fuente_incipit': 'Manuscrito original',
            'lenguas-TOTAL_FORMS': '1',
            'lenguas-0-codigo_lengua_texto': 'ger',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_manuscrita_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        self.assertEqual(obra.tipo_registro, 'd')
        self.assertEqual(obra.nivel_bibliografico, 'm')
        self.assertEqual(obra.incipits_musicales.count(), 1)
        self.assertEqual(obra.codigos_lengua.count(), 1)
    
    def test_crear_coleccion_manuscrita_con_0xx(self):
        """Test: Crear colección manuscrita con bloque 0XX"""
        data = self._get_base_obra_data(tipo_obra='coleccion_manuscrita')
        data['tipo_registro'] = 'd'
        data['nivel_bibliografico'] = 'c'
        data['titulo_uniforme_obra'] = 'Colección de sonatas'
        
        data.update({
            'lenguas-TOTAL_FORMS': '2',
            'lenguas-0-codigo_lengua_texto': 'ita',
            'lenguas-1-codigo_lengua_texto': 'fre',
            'paises-TOTAL_FORMS': '1',
            'paises-0-codigo_pais': 'it',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'coleccion_manuscrita'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        self.assertEqual(obra.tipo_registro, 'd')
        self.assertEqual(obra.nivel_bibliografico, 'c')
        self.assertEqual(obra.codigos_lengua.count(), 2)
        self.assertEqual(obra.codigos_pais.count(), 1)
    
    def test_crear_obra_impresa_individual_con_0xx(self):
        """Test: Crear obra impresa individual con bloque 0XX"""
        data = self._get_base_obra_data(tipo_obra='obra_impresa_individual')
        data['tipo_registro'] = 'c'
        data['nivel_bibliografico'] = 'm'
        
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-0-codigo_incipit': 'ED-001',
            'incipits-0-fuente_incipit': 'Editorial',
            'lenguas-TOTAL_FORMS': '1',
            'lenguas-0-codigo_lengua_texto': 'eng',
            'paises-TOTAL_FORMS': '1',
            'paises-0-codigo_pais': 'uk',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_impresa_individual'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        self.assertEqual(obra.tipo_registro, 'c')
        self.assertEqual(obra.nivel_bibliografico, 'm')
        self.assertEqual(obra.incipits_musicales.count(), 1)
        self.assertEqual(obra.codigos_lengua.count(), 1)
        self.assertEqual(obra.codigos_pais.count(), 1)
    
    def test_crear_obra_en_coleccion_impresa_con_0xx(self):
        """Test: Crear obra en colección impresa con bloque 0XX"""
        data = self._get_base_obra_data(tipo_obra='obra_en_coleccion_impresa')
        data['tipo_registro'] = 'c'
        data['nivel_bibliografico'] = 'a'
        
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-0-codigo_incipit': 'Vol. 1 No. 3',
            'incipits-0-fuente_incipit': 'Colección completa',
            'lenguas-TOTAL_FORMS': '1',
            'lenguas-0-codigo_lengua_texto': 'spa',
        })
        
        url = reverse('catalogacion:crear_obra', kwargs={'tipo': 'obra_en_coleccion_impresa'})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        obra = ObraGeneral.objects.first()
        self.assertEqual(obra.tipo_registro, 'c')
        self.assertEqual(obra.nivel_bibliografico, 'a')
        self.assertEqual(obra.incipits_musicales.count(), 1)
        self.assertEqual(obra.codigos_lengua.count(), 1)


class Bloque0XXUpdateTestCase(TransactionTestCase):
    """
    Tests para edición de obras con campos del bloque 0XX.
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.compositor = AutoridadPersona.objects.create(
            apellidos_nombres="Mozart, Wolfgang Amadeus",
            fechas="1756-1791"
        )
        
        # Crear obra base para editar
        self.obra = ObraGeneral.objects.create(
            num_control='TEST-EDIT-001',
            tipo_registro='d',
            nivel_bibliografico='m',
            titulo_principal='Sonata para violin',
            compositor=self.compositor,
        )
    
    def _get_edit_data(self):
        """Obtener datos base para editar obra"""
        return {
            'tipo_registro': self.obra.tipo_registro,
            'nivel_bibliografico': self.obra.nivel_bibliografico,
            'num_control': self.obra.num_control,
            'compositor': self.compositor.id,
            'titulo_principal': self.obra.titulo_principal,
            'titulo_uniforme_obra': 'Sonata para violin',
            'lugar_publicacion': 'Viena',
            'fecha_publicacion': '1780',
            
            # Management forms
            'incipits-TOTAL_FORMS': '0',
            'incipits-INITIAL_FORMS': '0',
            'lenguas-TOTAL_FORMS': '0',
            'lenguas-INITIAL_FORMS': '0',
            'paises-TOTAL_FORMS': '0',
            'paises-INITIAL_FORMS': '0',
            'funciones-TOTAL_FORMS': '0',
            'funciones-INITIAL_FORMS': '0',
            'titulos_alt-TOTAL_FORMS': '0',
            'titulos_alt-INITIAL_FORMS': '0',
            'ediciones-TOTAL_FORMS': '0',
            'ediciones-INITIAL_FORMS': '0',
            'produccion-TOTAL_FORMS': '0',
            'produccion-INITIAL_FORMS': '0',
            'medios_382-TOTAL_FORMS': '0',
            'medios_382-INITIAL_FORMS': '0',
            'menciones_490-TOTAL_FORMS': '0',
            'menciones_490-INITIAL_FORMS': '0',
            'notas_500-TOTAL_FORMS': '0',
            'notas_500-INITIAL_FORMS': '0',
            'contenidos_505-TOTAL_FORMS': '0',
            'contenidos_505-INITIAL_FORMS': '0',
            'sumarios_520-TOTAL_FORMS': '0',
            'sumarios_520-INITIAL_FORMS': '0',
            'biograficos_545-TOTAL_FORMS': '0',
            'biograficos_545-INITIAL_FORMS': '0',
            'materias_650-TOTAL_FORMS': '0',
            'materias_650-INITIAL_FORMS': '0',
            'generos_655-TOTAL_FORMS': '0',
            'generos_655-INITIAL_FORMS': '0',
            'nombres_700-TOTAL_FORMS': '0',
            'nombres_700-INITIAL_FORMS': '0',
            'entidades_710-TOTAL_FORMS': '0',
            'entidades_710-INITIAL_FORMS': '0',
            'enlaces_773-TOTAL_FORMS': '0',
            'enlaces_773-INITIAL_FORMS': '0',
            'enlaces_774-TOTAL_FORMS': '0',
            'enlaces_774-INITIAL_FORMS': '0',
            'relaciones_787-TOTAL_FORMS': '0',
            'relaciones_787-INITIAL_FORMS': '0',
            'ubicaciones_852-TOTAL_FORMS': '0',
            'ubicaciones_852-INITIAL_FORMS': '0',
            'disponibles_856-TOTAL_FORMS': '0',
            'disponibles_856-INITIAL_FORMS': '0',
        }
    
    def test_agregar_incipit_a_obra_existente(self):
        """Test: Agregar incipit musical a obra que no tenía"""
        data = self._get_edit_data()
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-0-codigo_incipit': 'KV 301',
            'incipits-0-fuente_incipit': 'Köchel-Verzeichnis',
        })
        
        url = reverse('catalogacion:editar_obra', kwargs={'pk': self.obra.pk})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        self.obra.refresh_from_db()
        self.assertEqual(self.obra.incipits_musicales.count(), 1)
        incipit = self.obra.incipits_musicales.first()
        self.assertEqual(incipit.codigo_incipit, 'KV 301')
    
    def test_editar_incipit_existente(self):
        """Test: Editar incipit musical existente"""
        # Crear incipit inicial
        incipit = IncipitMusical.objects.create(
            obra=self.obra,
            codigo_incipit='KV 300',
            fuente_incipit='Köchel-Verzeichnis'
        )
        
        data = self._get_edit_data()
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-INITIAL_FORMS': '1',
            'incipits-0-id': incipit.id,
            'incipits-0-codigo_incipit': 'KV 301',  # Cambio
            'incipits-0-fuente_incipit': 'Köchel-Verzeichnis Actualizado',
        })
        
        url = reverse('catalogacion:editar_obra', kwargs={'pk': self.obra.pk})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        incipit.refresh_from_db()
        self.assertEqual(incipit.codigo_incipit, 'KV 301')
        self.assertEqual(incipit.fuente_incipit, 'Köchel-Verzeichnis Actualizado')
    
    def test_eliminar_incipit_existente(self):
        """Test: Eliminar incipit musical existente"""
        # Crear incipit inicial
        incipit = IncipitMusical.objects.create(
            obra=self.obra,
            codigo_incipit='KV 301',
            fuente_incipit='Köchel-Verzeichnis'
        )
        
        data = self._get_edit_data()
        data.update({
            'incipits-TOTAL_FORMS': '1',
            'incipits-INITIAL_FORMS': '1',
            'incipits-0-id': incipit.id,
            'incipits-0-DELETE': 'on',
        })
        
        url = reverse('catalogacion:editar_obra', kwargs={'pk': self.obra.pk})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        self.obra.refresh_from_db()
        self.assertEqual(self.obra.incipits_musicales.count(), 0)
    
    def test_agregar_multiples_codigos_lengua(self):
        """Test: Agregar múltiples códigos de lengua a obra existente"""
        data = self._get_edit_data()
        data.update({
            'lenguas-TOTAL_FORMS': '3',
            'lenguas-0-codigo_lengua_texto': 'ger',
            'lenguas-1-codigo_lengua_texto': 'ita',
            'lenguas-2-codigo_lengua_texto': 'fre',
        })
        
        url = reverse('catalogacion:editar_obra', kwargs={'pk': self.obra.pk})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        self.obra.refresh_from_db()
        self.assertEqual(self.obra.codigos_lengua.count(), 3)
    
    def test_actualizar_bloque_0xx_completo(self):
        """Test: Actualizar todos los campos del bloque 0XX"""
        # Crear datos iniciales
        IncipitMusical.objects.create(
            obra=self.obra,
            codigo_incipit='OLD-001',
            fuente_incipit='Fuente antigua'
        )
        CodigoLengua.objects.create(
            obra=self.obra,
            codigo_lengua_texto='lat'
        )
        
        # Actualizar con nuevos datos
        data = self._get_edit_data()
        data.update({
            'incipits-TOTAL_FORMS': '2',
            'incipits-INITIAL_FORMS': '0',  # Ignorar existentes
            'incipits-0-codigo_incipit': 'NEW-001',
            'incipits-0-fuente_incipit': 'Fuente nueva',
            'incipits-1-codigo_incipit': 'NEW-002',
            'incipits-1-fuente_incipit': 'Otra fuente',
            
            'lenguas-TOTAL_FORMS': '2',
            'lenguas-INITIAL_FORMS': '0',
            'lenguas-0-codigo_lengua_texto': 'ger',
            'lenguas-1-codigo_lengua_texto': 'ita',
            
            'paises-TOTAL_FORMS': '1',
            'paises-0-codigo_pais': 'au',
        })
        
        url = reverse('catalogacion:editar_obra', kwargs={'pk': self.obra.pk})
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        
        self.obra.refresh_from_db()
        
        # Verificar nuevos datos
        self.assertEqual(self.obra.incipits_musicales.count(), 2)
        self.assertEqual(self.obra.codigos_lengua.count(), 2)
        self.assertEqual(self.obra.codigos_pais.count(), 1)
        
        # Verificar que los códigos son los nuevos
        lenguas = list(self.obra.codigos_lengua.values_list('codigo_lengua_texto', flat=True))
        self.assertIn('ger', lenguas)
        self.assertIn('ita', lenguas)
        self.assertNotIn('lat', lenguas)
