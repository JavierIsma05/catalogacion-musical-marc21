"""
Constantes y listas controladas para catalogación MARC21
Centralizadas para facilitar mantenimiento
"""

TONALIDADES = [
    ('Do mayor', 'Do mayor'),
    ('Do# mayor', 'Do# mayor'),
    ('Reb mayor', 'Re♭ mayor'),
    ('Re mayor', 'Re mayor'),
    ('Mib mayor', 'Mi♭ mayor'),
    ('Mi mayor', 'Mi mayor'),
    ('Fa mayor', 'Fa mayor'),
    ('Fa# mayor', 'Fa# mayor'),
    ('Sol mayor', 'Sol mayor'),
    ('Sol# mayor', 'Sol# mayor'),
    ('Lab mayor', 'La♭ mayor'),
    ('La mayor', 'La mayor'),
    ('Sib mayor', 'Si♭ mayor'),
    ('Si mayor', 'Si mayor'),
    ('Do menor', 'Do menor'),
    ('Do# menor', 'Do# menor'),
    ('Reb menor', 'Re♭ menor'),
    ('Re menor', 'Re menor'),
    ('Mib menor', 'Mi♭ menor'),
    ('Mi menor', 'Mi menor'),
    ('Fa menor', 'Fa menor'),
    ('Fa# menor', 'Fa# menor'),
    ('Sol menor', 'Sol menor'),
    ('Sol# menor', 'Sol# menor'),
    ('Lab menor', 'La♭ menor'),
    ('La menor', 'La menor'),
    ('Sib menor', 'Si♭ menor'),
    ('Si menor', 'Si menor'),
]

TECNICAS = [
    ('autógrafo', 'Autógrafo'),
    ('posible autógrafo', 'Posible autógrafo'),
    ('manuscrito', 'Manuscrito'),
    ('manuscrito de copista no identificado', 'Manuscrito de copista no identificado'),
    ('impreso', 'Impreso'),
    ('fotocopia de manuscrito', 'Fotocopia de manuscrito'),
    ('fotocopia de impreso', 'Fotocopia de impreso'),
]

FORMATOS = [
    ('parte', 'Parte'),
    ('partitura de piano', 'Partitura de piano'),
    ('partitura de coro', 'Partitura de coro'),
    ('partitura piano vocal', 'Partitura piano vocal'),
]

CODIGOS_LENGUAJE = [
    ('ger', 'Alemán'),
    ('spa', 'Español'),
    ('fre', 'Francés'),
    ('eng', 'Inglés'),
    ('ita', 'Italiano'),
    ('por', 'Portugués'),
]

CODIGOS_PAIS = [
    ('ar', 'Argentina'),
    ('bo', 'Bolivia'),
    ('br', 'Brasil'),
    ('cl', 'Chile'),
    ('co', 'Colombia'),
    ('cr', 'Costa Rica'),
    ('cu', 'Cuba'),
    ('ec', 'Ecuador'),
    ('sv', 'El Salvador'),
    ('gt', 'Guatemala'),
    ('ho', 'Honduras'),
    ('mx', 'México'),
    ('nq', 'Nicaragua'),
    ('pa', 'Panamá'),
    ('pe', 'Perú'),
    ('pr', 'Puerto Rico'),
    ('dr', 'República Dominicana'),
    ('uy', 'Uruguay'),
    ('ve', 'Venezuela'),
]

FUNCIONES_PERSONA = [
    ('arreglista', 'Arreglista'),
    ('coeditor', 'Coeditor'),
    ('compilador', 'Compilador'),
    ('compositor', 'Compositor'),
    ('copista', 'Copista'),
    ('dedicatario', 'Dedicatario'),
    ('editor', 'Editor'),
    ('prologuista', 'Prologuista'),
]

AUTORIAS_CHOICES = [
    ('atribuida', 'Atribuida'),
    ('certificada', 'Certificada'),
    ('erronea', 'Errónea'),
]

FUNCIONES_ENTIDAD = [
    ('coeditor', 'Coeditor'),
    ('dedicatario', 'Dedicatario'),
    ('editor', 'Editor'),
    ('lugar_ejecucion', 'Lugar de ejecución'),
    ('lugar_estreno', 'Lugar de estreno'),
    ('patrocinante', 'Patrocinante'),
]

MEDIOS_INTERPRETACION = [
    ('piano', 'Piano'),
    ('dos pianos', 'Dos pianos'),
    ('piano a cuatro manos', 'Piano a cuatro manos'),
    ('piano con acompañamiento', 'Piano con acompañamiento'),
]

# Mapeo de tipo_registro + nivel_bibliografico a tipo_obra
TIPO_OBRA_MAP = {
    ('d', 'c'): ('CM', 'Colección manuscrita'),
    ('d', 'a'): ('OICM', 'Obra en colección manuscrita'),
    ('d', 'm'): ('OIM', 'Obra manuscrita independiente'),
    ('c', 'c'): ('CI', 'Colección impresa'),
    ('c', 'a'): ('OICI', 'Obra en colección impresa'),
    ('c', 'm'): ('OII', 'Obra impresa independiente'),
}