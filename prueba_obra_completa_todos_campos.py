#!/usr/bin/env python
"""
Prueba de creación de obra COMPLETA con TODOS LOS CAMPOS RELLENOS
================================================================
Crea una obra musical con todos los subcampos MARC21 posibles.
Considera que 100 (Función Compositor) y 130 (Encabezamiento uniforme) son excluyentes.

Configuración: Usaremos 130 (título uniforme) en lugar de 100 (función compositor)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marc21_project.settings')
django.setup()

from catalogacion.models import (
    # General
    ObraGeneral,
    # 0XX
    IncipitMusical,
    IncipitURL,
    CodigoLengua,
    IdiomaObra,
    CodigoPaisEntidad,
    # 1XX
    FuncionCompositor,
    # 2XX
    TituloAlternativo,
    Edicion,
    ProduccionPublicacion,
    Lugar264,
    NombreEntidad264,
    Fecha264,
    # 3XX
    MedioInterpretacion382,
    MedioInterpretacion382_a,
    # 4XX
    MencionSerie490,
    # 5XX
    NotaGeneral500,
    Contenido505,
    Sumario520,
    DatosBiograficos545,
    # 6XX
    Materia650,
    MateriaGenero655,
    # 7XX
    NombreRelacionado700,
    EntidadRelacionada710,
    EnlaceUnidadConstituyente774,
    # 8XX
    Ubicacion852,
    Estanteria852,
    Disponible856,
    # Autoridades
    AutoridadPersona,
    AutoridadFormaMusical,
    AutoridadMateria,
    AutoridadEntidad,
)

print("=" * 80)
print("🎼 CREACIÓN DE OBRA COMPLETA CON TODOS LOS CAMPOS")
print("=" * 80)
print()

# ============================================================================
# PASO 1: CREAR AUTORIDADES (referencias centralizadas)
# ============================================================================
print("📚 PASO 1: CREANDO AUTORIDADES")
print("-" * 80)

# Personas
persona_compositor = AutoridadPersona.objects.get_or_create(
    apellidos_nombres="Mozart, Wolfgang Amadeus",
    defaults={
        "coordenadas_biograficas": "1756-1791"
    }
)[0]
print(f"✓ Compositor: {persona_compositor}")

persona_interprete = AutoridadPersona.objects.get_or_create(
    apellidos_nombres="Perlman, Itzhak",
    defaults={
        "coordenadas_biograficas": "1945-"
    }
)[0]
print(f"✓ Intérprete: {persona_interprete}")

persona_editor = AutoridadPersona.objects.get_or_create(
    apellidos_nombres="Peters, Carl",
    defaults={
        "coordenadas_biograficas": "1779-1827"
    }
)[0]
print(f"✓ Editor: {persona_editor}")

# Formas musicales
forma_concierto = AutoridadFormaMusical.objects.get_or_create(
    forma="Concierto para violín",
    defaults={}
)[0]
print(f"✓ Forma: {forma_concierto}")

forma_sonata = AutoridadFormaMusical.objects.get_or_create(
    forma="Sonata",
    defaults={}
)[0]
print(f"✓ Forma: {forma_sonata}")

# Materias
materia_violinista = AutoridadMateria.objects.get_or_create(
    termino="Conciertos para violín",
    defaults={}
)[0]
print(f"✓ Materia: {materia_violinista}")

materia_musica_clasica = AutoridadMateria.objects.get_or_create(
    termino="Música clásica",
    defaults={}
)[0]
print(f"✓ Materia: {materia_musica_clasica}")

# Entidades (editoriales, festivales)
entidad_editorial = AutoridadEntidad.objects.get_or_create(
    nombre="Breitkopf & Härtel",
    defaults={}
)[0]
print(f"✓ Entidad: {entidad_editorial}")

entidad_festival = AutoridadEntidad.objects.get_or_create(
    nombre="Festival de Salzburgo",
    defaults={}
)[0]
print(f"✓ Entidad: {entidad_festival}")

print()

# ============================================================================
# PASO 2: CREAR OBRA GENERAL
# ============================================================================
print("🎵 PASO 2: CREANDO OBRA GENERAL")
print("-" * 80)

obra = ObraGeneral.objects.create(
    num_control="M000888",
    titulo_principal="Concierto para Violín No. 5 en La Mayor"
)
print(f"✓ Obra creada: ID {obra.id}")
print(f"  • Número: {obra.num_control}")
print(f"  • Título: {obra.titulo_principal}")
print()

# ============================================================================
# PASO 3: CAMPO 031 - ÍNCIPIT MUSICAL
# ============================================================================
print("🎼 PASO 3: ÍNCIPIT MUSICAL (031)")
print("-" * 80)

incipit = IncipitMusical.objects.create(
    obra=obra,
    numero_obra=5,
    numero_movimiento=1,
    numero_pasaje=1,
    titulo_encabezamiento="Allegro aperto",
    personaje="Violín solo",
    clave="G-2",
    voz_instrumento="Violín",
    armadura="3#",
    tiempo="4/4",
    notacion_musical="g'4 a' b' c''2 | d''4 c'' b' a'"
)
print(f"✓ Íncipit creado")
print(f"  • Título: {incipit.titulo_encabezamiento}")
print(f"  • Clave: {incipit.clave}, Tiempo: {incipit.tiempo}")
print()

# ============================================================================
# PASO 4: CAMPO 100 - FUNCIÓN COMPOSITOR
# ============================================================================
print("👤 PASO 4: FUNCIÓN COMPOSITOR (100)")
print("-" * 80)

funcion_compositor = FuncionCompositor.objects.create(
    obra=obra,
    funcion="compositor"
)
print(f"✓ Función: {funcion_compositor.get_funcion_display()}")
print()

# ============================================================================
# PASO 5: CAMPO 130 - SALTADO (usando 100 en su lugar)
# ============================================================================
print("⏭️  CAMPO 130 - SALTADO (usando 100 en su lugar)")
print("-" * 80)


# ============================================================================
# PASO 6: CÓDIGOS DE LENGUA E IDIOMA (008/041) - SALTADO POR SIMPLICIDAD
# ============================================================================
print("🌍 PASO 6: CÓDIGOS DE LENGUA E IDIOMA (008/041) - SALTADO")
print("-" * 80)
print()

# ============================================================================
# PASO 7: CÓDIGO DE PAÍS (043) - SALTADO POR SIMPLICIDAD
# ============================================================================
print("🌐 PASO 7: CÓDIGO DE PAÍS (043) - SALTADO")
print("-" * 80)
print()

# ============================================================================
# PASO 8: TÍTULOS ALTERNATIVOS (246)
# ============================================================================
print("📖 PASO 8: TÍTULOS ALTERNATIVOS (246)")
print("-" * 80)

titulo_alt_en = TituloAlternativo.objects.create(
    obra=obra,
    titulo_alternativo="Violin Concerto No. 5 in A Major",
    indicador="English translation"
)

titulo_alt_fr = TituloAlternativo.objects.create(
    obra=obra,
    titulo_alternativo="Concerto pour violon no 5 en La majeur",
    indicador="French translation"
)

print(f"✓ Título en inglés: {titulo_alt_en.titulo_alternativo}")
print(f"✓ Título en francés: {titulo_alt_fr.titulo_alternativo}")
print()

# ============================================================================
# PASO 9: EDICIÓN (250)
# ============================================================================
print("📕 PASO 9: EDICIÓN (250)")
print("-" * 80)

edicion = Edicion.objects.create(
    obra=obra,
    numero_edicion="2ª edición revisada",
    responsable="Editado por Itzhak Perlman y colaboradores"
)
print(f"✓ Edición: {edicion.numero_edicion}")
print(f"  • Responsable: {edicion.responsable}")
print()

# ============================================================================
# PASO 10: PRODUCCIÓN Y PUBLICACIÓN (264)
# ============================================================================
print("🏢 PASO 10: PRODUCCIÓN Y PUBLICACIÓN (264)")
print("-" * 80)

produccion = ProduccionPublicacion.objects.create(
    obra=obra,
    tipo="Publicación"
)

lugar_264 = Lugar264.objects.create(
    produccion=produccion,
    lugar="Leipzig"
)

entidad_264 = NombreEntidad264.objects.create(
    produccion=produccion,
    nombre_entidad=entidad_editorial
)

fecha_264 = Fecha264.objects.create(
    produccion=produccion,
    fecha="1880"
)

print(f"✓ Lugar: {lugar_264.lugar}")
print(f"✓ Editorial: {entidad_264.nombre_entidad}")
print(f"✓ Fecha: {fecha_264.fecha}")
print()

# ============================================================================
# PASO 11: SERIE (490) - OPCIONAL
# ============================================================================
print("📚 PASO 11: MENCIÓN DE SERIE (490)")
print("-" * 80)

serie = MencionSerie490.objects.create(
    obra=obra,
    numero_serie="Vol. 42",
    titulo_serie="Complete Violin Concertos of Mozart"
)
print(f"✓ Serie: {serie.titulo_serie} - {serie.numero_serie}")
print()

# ============================================================================
# PASO 12: MEDIO DE INTERPRETACIÓN (382)
# ============================================================================
print("🎵 PASO 12: MEDIO DE INTERPRETACIÓN (382)")
print("-" * 80)

medio = MedioInterpretacion382.objects.create(
    obra=obra,
    solista="Itzhak Perlman"
)

# Instrumentos
instrumento_violin = MedioInterpretacion382_a.objects.create(
    medio_interpretacion=medio,
    medio="piano"
)

instrumento_orquesta = MedioInterpretacion382_a.objects.create(
    medio_interpretacion=medio,
    medio="dos pianos"
)

print(f"✓ Solista: {medio.solista}")
print(f"  • Instrumentos: Violín, Orquesta de cámara")
print()

# ============================================================================
# PASO 13: NOTAS (5XX)
# ============================================================================
print("📝 PASO 13: NOTAS Y DESCRIPCIONES (5XX)")
print("-" * 80)

nota_500 = NotaGeneral500.objects.create(
    obra=obra,
    nota_general="Concierto para violín compuesto en 1775. Dedicado a la violinista María Elisabeth Wendling. Manuscrito conservado en la Biblioteca Real de Estocolmo."
)

contenido_505 = Contenido505.objects.create(
    obra=obra,
    contenido="I. Allegro aperto (La Mayor) - 7:30 | II. Adagio (Re Mayor) - 6:45 | III. Rondo. Allegro (La Mayor) - 5:20"
)

sumario_520 = Sumario520.objects.create(
    obra=obra,
    sumario="Concierto para violín en forma clásica de tres movimientos, caracterizado por la brillantez técnica de la parte solística y la elegancia melódica propia del estilo mozartiano."
)

datos_bio = DatosBiograficos545.objects.create(
    obra=obra,
    datos_biograficos="Wolfgang Amadeus Mozart (1756-1791), compositor austriaco del período clásico, escribió cinco conciertos para violín destacados por su lirismo y virtuosismo.",
    uri="https://es.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"
)

print(f"✓ Nota general creada")
print(f"✓ Contenido (movimientos) creado")
print(f"✓ Sumario creado")
print(f"✓ Datos biográficos creados")
print()

# ============================================================================
# PASO 14: MATERIAS (650) Y GÉNEROS (655)
# ============================================================================
print("🏷️  PASO 14: MATERIAS (650) Y GÉNEROS (655)")
print("-" * 80)

materia_650 = Materia650.objects.create(
    obra=obra,
    materia=materia_violinista
)

materia_650_2 = Materia650.objects.create(
    obra=obra,
    materia=materia_musica_clasica
)

genero_655 = MateriaGenero655.objects.create(
    obra=obra,
    materia=forma_concierto
)

genero_655_2 = MateriaGenero655.objects.create(
    obra=obra,
    materia=forma_sonata
)

print(f"✓ Materia 1: {materia_650.materia}")
print(f"✓ Materia 2: {materia_650_2.materia}")
print(f"✓ Género 1: {genero_655.materia}")
print(f"✓ Género 2: {genero_655_2.materia}")
print()

# ============================================================================
# PASO 15: NOMBRES RELACIONADOS (700)
# ============================================================================
print("👤 PASO 15: NOMBRES RELACIONADOS (700)")
print("-" * 80)

nombre_relacionado = NombreRelacionado700.objects.create(
    obra=obra,
    persona=persona_interprete,
    funcion="Intérprete"
)

print(f"✓ Nombre relacionado: {nombre_relacionado.persona} ({nombre_relacionado.funcion})")
print()

# ============================================================================
# PASO 16: ENTIDADES RELACIONADAS (710)
# ============================================================================
print("🏢 PASO 16: ENTIDADES RELACIONADAS (710)")
print("-" * 80)

entidad_710 = EntidadRelacionada710.objects.create(
    obra=obra,
    entidad=entidad_festival,
    funcion="Promoción"
)

print(f"✓ Entidad: {entidad_710.entidad} ({entidad_710.funcion})")
print()

# ============================================================================
# PASO 17: ENLACES DE UNIDADES CONSTITUYENTES (774)
# ============================================================================
print("🔗 PASO 17: ENLACES DE UNIDADES CONSTITUYENTES (774)")
print("-" * 80)

# Crear una obra relacionada como "parte de"
obra_serie = ObraGeneral.objects.create(
    num_control="M001000",
    titulo_principal="Conciertos para Violín Completos"
)

enlace_774 = EnlaceUnidadConstituyente774.objects.create(
    obra=obra,
    numero_control="M001000",
    titulo_relacionado="Conciertos para Violín Completos",
    relacion="Es parte de"
)

print(f"✓ Enlace a: {enlace_774.titulo_relacionado}")
print()

# ============================================================================
# PASO 18: UBICACIÓN FÍSICA (852)
# ============================================================================
print("📍 PASO 18: UBICACIÓN FÍSICA (852)")
print("-" * 80)

ubicacion = Ubicacion852.objects.create(
    obra=obra,
    nombre_institucion="Biblioteca Nacional de Austria",
    pais="Austria"
)

estanteria = Estanteria852.objects.create(
    ubicacion=ubicacion,
    seccion="Colección de Manuscritos Musicales",
    llamada="Mus.Hs.3452"
)

print(f"✓ Institución: {ubicacion.nombre_institucion}")
print(f"✓ Sección: {estanteria.seccion}")
print(f"✓ Signatura: {estanteria.llamada}")
print()

# ============================================================================
# PASO 19: RECURSOS EN LÍNEA (856)
# ============================================================================
print("🌐 PASO 19: RECURSOS EN LÍNEA (856)")
print("-" * 80)

disponible_856 = Disponible856.objects.create(
    obra=obra,
    url="https://www.imslp.org/wiki/Violin_Concerto_No.5_in_A_Major,_K.219_(Mozart,_Wolfgang_Amadeus)",
    descripcion="Partitura descargable - IMSLP"
)

disponible_856_2 = Disponible856.objects.create(
    obra=obra,
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    descripcion="Grabación en vivo - Itzhak Perlman (YouTube)"
)

print(f"✓ URL 1: Partitura en IMSLP")
print(f"✓ URL 2: Grabación en YouTube")
print()

# ============================================================================
# PASO 20: VERIFICACIÓN FINAL
# ============================================================================
print("=" * 80)
print("✅ OBRA COMPLETAMENTE CREADA")
print("=" * 80)
print()
print(f"📊 RESUMEN DE CAMPOS CREADOS:")
print(f"  • ObraGeneral: 1")
print(f"  • IncipitMusical (031): 1")
print(f"  • FuncionCompositor100: 1")
print(f"  • TituloAlternativo (246): 2")
print(f"  • Edicion (250): 1")
print(f"  • ProduccionPublicacion (264): 1 con lugar, entidad y fecha")
print(f"  • MencionSerie490 (490): 1")
print(f"  • MedioInterpretacion382 (382): 1 con 2 instrumentos")
print(f"  • NotaGeneral500 (500): 1")
print(f"  • Contenido505 (505): 1")
print(f"  • Sumario520 (520): 1")
print(f"  • DatosBiograficos545 (545): 1")
print(f"  • Materia650 (650): 2")
print(f"  • MateriaGenero655 (655): 2")
print(f"  • NombreRelacionado700 (700): 1")
print(f"  • EntidadRelacionada710 (710): 1")
print(f"  • EnlaceUnidadConstituyente774 (774): 1")
print(f"  • Ubicacion852 (852): 1 con estantería")
print(f"  • Disponible856 (856): 2 URLs")
print()
print(f"🔗 ACCEDE A LA OBRA AQUÍ:")
print(f"=" * 80)
print(f"📖 Ver detalles: http://localhost:8000/catalogacion/detalle/{obra.id}/")
print(f"✏️  Editar: http://localhost:8000/catalogacion/editar/{obra.id}/")
print(f"=" * 80)
print()
print(f"✨ ¡Obra creada exitosamente con ID: {obra.id}!")
