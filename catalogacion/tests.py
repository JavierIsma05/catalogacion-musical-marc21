# """
# Tests unitarios para el sistema MARC21
# """
# from django.test import TestCase
# from django.core.exceptions import ValidationError

# from catalogacion.models.autoridades import AutoridadPersona, AutoridadTituloUniforme
# from catalogacion.models.bloque_0xx import CodigoPaisEntidad
# from catalogacion.models.utils import generar_numero_control, validar_obra_coleccion, validar_obra_en_coleccion, validar_obra_independiente

# from .models import ObraGeneral, NumeroControlSecuencia
# from .formatters import MARCFormatter


# class NumeroControlTest(TestCase):
#     """Tests para generación de números de control"""
    
#     def test_genera_numero_manuscrito(self):
#         """Verifica que genera números M000001 para manuscritos"""
#         num = generar_numero_control('d')
#         self.assertTrue(num.startswith('M'))
#         self.assertEqual(len(num), 7)
    
#     def test_genera_numero_impreso(self):
#         """Verifica que genera números I000001 para impresos"""
#         num = generar_numero_control('c')
#         self.assertTrue(num.startswith('I'))
#         self.assertEqual(len(num), 7)
    
#     def test_numeros_secuenciales(self):
#         """Verifica que los números sean secuenciales"""
#         num1 = generar_numero_control('d')
#         num2 = generar_numero_control('d')
        
#         valor1 = int(num1[1:])
#         valor2 = int(num2[1:])
        
#         self.assertEqual(valor2, valor1 + 1)
    
#     def test_secuencias_separadas(self):
#         """Verifica que manuscritos e impresos tengan secuencias separadas"""
#         NumeroControlSecuencia.objects.all().delete()
        
#         num_m1 = generar_numero_control('d')  # M000001
#         num_i1 = generar_numero_control('c')  # I000001
#         num_m2 = generar_numero_control('d')  # M000002
        
#         self.assertEqual(num_m1, 'M000001')
#         self.assertEqual(num_i1, 'I000001')
#         self.assertEqual(num_m2, 'M000002')


# class ObraGeneralTest(TestCase):
#     """Tests para el modelo ObraGeneral"""
    
#     def setUp(self):
#         """Preparar datos de prueba"""
#         self.compositor = AutoridadPersona.objects.create(
#             apellidos_nombres="Mozart, Wolfgang Amadeus",
#             fechas="1756-1791"
#         )
#         self.titulo_uniforme = AutoridadTituloUniforme.objects.create(
#             titulo="Sonatas para piano"
#         )
    
#     def test_crear_obra_con_compositor(self):
#         """Crea una obra con compositor (campo 100)"""
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Sonata para piano K. 331",
#             tipo_registro='d',
#             nivel_bibliografico='m'
#         )
        
#         self.assertIsNotNone(obra.num_control)
#         self.assertTrue(obra.num_control.startswith('M'))
#         self.assertEqual(obra.tipo_obra, 'OIM')
    
#     def test_crear_obra_con_titulo_uniforme(self):
#         """Crea una obra con título uniforme (campo 130)"""
#         obra = ObraGeneral.objects.create(
#             titulo_uniforme=self.titulo_uniforme,
#             titulo_principal="Sonatas completas",
#             tipo_registro='c',
#             nivel_bibliografico='m'
#         )
        
#         self.assertIsNotNone(obra.num_control)
#         self.assertTrue(obra.num_control.startswith('I'))
#         self.assertEqual(obra.tipo_obra, 'OII')
    
#     def test_no_puede_tener_compositor_y_titulo_uniforme(self):
#         """Valida que no se pueden tener ambos puntos de acceso"""
#         obra = ObraGeneral(
#             compositor=self.compositor,
#             titulo_uniforme=self.titulo_uniforme,
#             titulo_principal="Test",
#             tipo_registro='d',
#             nivel_bibliografico='m'
#         )
        
#         with self.assertRaises(ValidationError) as context:
#             obra.clean()
        
#         self.assertIn('compositor', context.exception.error_dict)
#         self.assertIn('titulo_uniforme', context.exception.error_dict)
    
#     def test_debe_tener_un_punto_acceso(self):
#         """Valida que debe existir al menos un punto de acceso"""
#         obra = ObraGeneral(
#             titulo_principal="Test sin punto de acceso",
#             tipo_registro='d',
#             nivel_bibliografico='m'
#         )
        
#         with self.assertRaises(ValidationError) as context:
#             obra.clean()
        
#         self.assertIn('compositor', context.exception.error_dict)
#         self.assertIn('titulo_uniforme', context.exception.error_dict)
    
#     def test_propiedades_computadas(self):
#         """Verifica propiedades computadas"""
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Test",
#             tipo_registro='d',
#             nivel_bibliografico='c'
#         )
        
#         self.assertTrue(obra.es_manuscrita)
#         self.assertFalse(obra.es_impresa)
#         self.assertTrue(obra.es_coleccion)
#         self.assertFalse(obra.es_obra_independiente)
#         self.assertEqual(obra.tipo_obra, 'CM')
#         self.assertEqual(obra.tipo_obra_descripcion, 'Colección manuscrita')
    
#     def test_signatura_completa(self):
#         """Verifica generación de signatura completa"""
        
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Test Signatura",
#             tipo_registro='d',
#             nivel_bibliografico='m',
#             centro_catalogador='UNL'
#         )
        
#         # Agregar país
#         CodigoPaisEntidad.objects.create(obra=obra, codigo_pais='ec')
        
#         signatura = obra.signatura_completa
#         self.assertIn('UNL', signatura)
#         self.assertIn('BLMP', signatura)
#         self.assertIn('EC', signatura)
#         self.assertIn('Ms', signatura)
#         self.assertIn(obra.num_control, signatura)


# class ManagerTest(TestCase):
#     """Tests para los managers personalizados"""
    
#     def setUp(self):
#         """Crear obras de diferentes tipos"""
#         compositor = AutoridadPersona.objects.create(
#             apellidos_nombres="Bach, Johann Sebastian"
#         )
        
#         # Manuscrita independiente
#         ObraGeneral.objects.create(
#             compositor=compositor,
#             titulo_principal="Obra Manuscrita 1",
#             tipo_registro='d',
#             nivel_bibliografico='m'
#         )
        
#         # Impresa independiente
#         ObraGeneral.objects.create(
#             compositor=compositor,
#             titulo_principal="Obra Impresa 1",
#             tipo_registro='c',
#             nivel_bibliografico='m'
#         )
        
#         # Colección manuscrita
#         ObraGeneral.objects.create(
#             compositor=compositor,
#             titulo_principal="Colección Manuscrita 1",
#             tipo_registro='d',
#             nivel_bibliografico='c'
#         )
    
#     def test_manager_manuscritas(self):
#         """Filtra obras manuscritas"""
#         manuscritas = ObraGeneral.objects.manuscritas()
#         self.assertEqual(manuscritas.count(), 2)
#         for obra in manuscritas:
#             self.assertEqual(obra.tipo_registro, 'd')
    
#     def test_manager_impresas(self):
#         """Filtra obras impresas"""
#         impresas = ObraGeneral.objects.impresas()
#         self.assertEqual(impresas.count(), 1)
#         for obra in impresas:
#             self.assertEqual(obra.tipo_registro, 'c')
    
#     def test_manager_colecciones(self):
#         """Filtra colecciones"""
#         colecciones = ObraGeneral.objects.colecciones()
#         self.assertEqual(colecciones.count(), 1)
#         for obra in colecciones:
#             self.assertEqual(obra.nivel_bibliografico, 'c')
    
#     def test_manager_obras_independientes(self):
#         """Filtra obras independientes"""
#         independientes = ObraGeneral.objects.obras_independientes()
#         self.assertEqual(independientes.count(), 2)
#         for obra in independientes:
#             self.assertEqual(obra.nivel_bibliografico, 'm')
    
#     def test_manager_con_compositor(self):
#         """Filtra obras con compositor"""
#         con_compositor = ObraGeneral.objects.con_compositor()
#         self.assertEqual(con_compositor.count(), 3)
#         for obra in con_compositor:
#             self.assertIsNotNone(obra.compositor)


# class FormatterTest(TestCase):
#     """Tests para el formateador MARC"""
    
#     def setUp(self):
#         """Crear obra de prueba"""
#         compositor = AutoridadPersona.objects.create(
#             apellidos_nombres="Beethoven, Ludwig van",
#             fechas="1770-1827"
#         )
        
#         self.obra = ObraGeneral.objects.create(
#             compositor=compositor,
#             titulo_principal="Sonata para piano no. 14",
#             subtitulo="Claro de luna",
#             tipo_registro='c',
#             nivel_bibliografico='m',
#             opus="Op. 27, No. 2",
#             isbn="978-3-16-148410-0"
#         )
    
#     def test_format_001(self):
#         """Formatea campo 001"""
#         formatter = MARCFormatter(self.obra)
#         campo_001 = formatter.format_001()
#         self.assertIn(self.obra.num_control, campo_001)
    
#     def test_format_020(self):
#         """Formatea campo 020 - ISBN"""
#         formatter = MARCFormatter(self.obra)
#         campo_020 = formatter.format_020()
#         self.assertIsNotNone(campo_020)
#         self.assertIn('978-3-16-148410-0', campo_020)
    
#     def test_format_100(self):
#         """Formatea campo 100 - Compositor"""
#         formatter = MARCFormatter(self.obra)
#         campo_100 = formatter.format_100()
#         self.assertIn('Beethoven, Ludwig van', campo_100)
#         self.assertIn('1770-1827', campo_100)
    
#     def test_format_245(self):
#         """Formatea campo 245 - Título principal"""
#         formatter = MARCFormatter(self.obra)
#         campo_245 = formatter.format_245()
#         self.assertIn('Sonata para piano no. 14', campo_245)
#         self.assertIn('Claro de luna', campo_245)
    
#     def test_format_383(self):
#         """Formatea campo 383 - Opus"""
#         formatter = MARCFormatter(self.obra)
#         campo_383 = formatter.format_383()
#         self.assertIn('Op. 27, No. 2', campo_383)
    
#     def test_full_record(self):
#         """Genera registro completo"""
#         formatter = MARCFormatter(self.obra)
#         record = formatter.format_full_record()
        
#         self.assertIn('001', record)
#         self.assertIn('020', record)
#         self.assertIn('100', record)
#         self.assertIn('245', record)
    
#     def test_to_dict(self):
#         """Convierte a diccionario"""
#         formatter = MARCFormatter(self.obra)
#         data = formatter.to_dict()
        
#         self.assertIsInstance(data, dict)
#         self.assertIn('001', data)
#         self.assertIn('100', data)
#         self.assertEqual(data['020']['a'], '978-3-16-148410-0')


# class ValidationTest(TestCase):
#     """Tests para validaciones específicas por tipo de obra"""
    
#     def setUp(self):
#         """Preparar datos de prueba"""
#         self.compositor = AutoridadPersona.objects.create(
#             apellidos_nombres="Test, Compositor"
#         )
    
#     def test_obra_manuscrita_no_puede_tener_isbn(self):
#         """Obras manuscritas no deben tener ISBN"""
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Test Manuscrita",
#             tipo_registro='d',
#             nivel_bibliografico='m',
#             isbn="978-3-16-148410-0"
#         )
        
#         errores = validar_obra_independiente(obra)
        
#         self.assertIn('isbn', errores)
    
#     def test_coleccion_debe_tener_contenidos(self):
#         """Colecciones deben tener contenidos 505"""
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Colección Test",
#             tipo_registro='d',
#             nivel_bibliografico='c'
#         )
        
#         errores = validar_obra_coleccion(obra)
        
#         self.assertIn('contenidos_505', errores)
    
#     def test_obra_en_coleccion_debe_tener_enlace_773(self):
#         """Obras en colección deben tener enlace 773"""
#         obra = ObraGeneral.objects.create(
#             compositor=self.compositor,
#             titulo_principal="Obra en Colección",
#             tipo_registro='d',
#             nivel_bibliografico='a'
#         )
        
#         errores = validar_obra_en_coleccion(obra)
        
#         self.assertIn('enlaces_documento_fuente_773', errores)


# # Comando para ejecutar tests:
# # python manage.py test marc21.tests