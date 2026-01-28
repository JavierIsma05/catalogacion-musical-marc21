"""
Funciones auxiliares para generación de números de control y códigos MARC
"""
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from django.db.models import Max


def generar_numero_control(tipo_registro):
    """
    Genera número de control único usando el máximo actual.
    Thread-safe mediante select_for_update.
    
    Args:
        tipo_registro: 'c' (impreso) o 'd' (manuscrito)
    
    Returns:
        str: Número de control en formato M000001 o I000001
    """
    # Importación lazy para evitar circular import
    from django.apps import apps
    NumeroControlSecuencia = apps.get_model('catalogacion', 'NumeroControlSecuencia')
    
    tipo_abrev = 'M' if tipo_registro == 'd' else 'I'
    
    with transaction.atomic():
        # Obtener o crear la secuencia para este tipo
        secuencia, created = NumeroControlSecuencia.objects.select_for_update().get_or_create(
            tipo_registro=tipo_registro,
            defaults={'ultimo_numero': 0}
        )
        
        # Incrementar el número
        secuencia.ultimo_numero += 1
        secuencia.save()
        
        siguiente_numero = secuencia.ultimo_numero
    
    return f"{tipo_abrev}{str(siguiente_numero).zfill(6)}"


def generar_codigo_informacion():
    """
    Genera el campo 008 (40 posiciones)
    Posiciones 00-05: Fecha de creación (ddmmaa)
    Posiciones 06-39: Barras verticales
    """
    now = timezone.now()
    # Formato: ddmmaa (día, mes, año con 2 dígitos)
    fecha_creacion = now.strftime('%d%m%y')
    # Completar con barras verticales hasta 40 posiciones
    resto = '|' * 34  # 40 - 6 = 34
    
    return fecha_creacion + resto

def actualizar_fecha_hora_transaccion():
    """
    Genera el campo 005 con fecha y hora actual
    Formato: ddmmaaaahhmmss
    """
    now = timezone.now()
    return now.strftime('%d%m%Y%H%M%S')


def obtener_pais_principal(obra):
    """
    Obtiene el código del país principal de una obra.
    
    Args:
        obra: Instancia de ObraGeneral
    
    Returns:
        str: Código del país en mayúsculas o 'EC' por defecto
    """
    try:
        paises = obra.codigos_pais_entidad.all()
        print(f"🔍 DEBUG: Países encontrados para obra {obra.num_control}: {[p.codigo_pais for p in paises]}")
        primer_pais = obra.codigos_pais_entidad.order_by('id').first()
        resultado = (primer_pais.codigo_pais if primer_pais else 'EC').upper()
        print(f"🔍 DEBUG: País seleccionado: {resultado}")
        return resultado
    except Exception as e:
        print(f"❌ ERROR en obtener_pais_principal: {e}")
        return 'EC'


def generar_signatura_completa(obra):
    """
    Genera la signatura completa para el campo 092.
    
    Args:
        obra: Instancia de ObraGeneral
    
    Returns:
        str: Signatura en formato UNL-BLMP-EC-Ms-M000001
    """
    if not all([
        obra.centro_catalogador,
        obra.num_control,
    ]):
        return "Pendiente de generar"
    
    # Determinar Ms o Imp según tipo_registro
    ms_imp = 'Ms' if obra.tipo_registro == 'd' else 'Imp'
    
    # Obtener país
    pais = obtener_pais_principal(obra)
    
    return (
        f"{obra.centro_catalogador}-"
        f"BLMP-"
        f"{pais}-"
        f"{ms_imp}-"
        f"{obra.num_control}"
    )


def validar_obra_coleccion(obra):
    """
    Valida que una colección tenga los campos requeridos.
    
    Args:
        obra: Instancia de ObraGeneral con nivel_bibliografico='c'
    
    Returns:
        dict: Diccionario con errores encontrados
    """
    errores = {}
    
    # Verificar si tiene contenidos 505
    if hasattr(obra, 'contenidos_505'):
        if not obra.contenidos_505.exists():
            errores['contenidos_505'] = "Las colecciones deben registrar al menos un contenido 505."
    
    # Verificar si tiene enlaces 774
    if hasattr(obra, 'enlaces_unidades_774'):
        if not obra.enlaces_unidades_774.exists():
            errores['enlaces_unidades_774'] = "Las colecciones deben detallar obras contenidas (774)."
    
    # Verificar que NO tenga enlaces 773
    if hasattr(obra, 'enlaces_documento_fuente_773'):
        if obra.enlaces_documento_fuente_773.exists():
            errores['enlaces_documento_fuente_773'] = "Las colecciones no pueden enlazarse mediante 773."
    
    # Verificar que NO tenga relaciones 787
    if hasattr(obra, 'otras_relaciones_787'):
        if obra.otras_relaciones_787.exists():
            errores['otras_relaciones_787'] = "Las colecciones no utilizan 787."
    
    # Validar que manuscritas no tengan ISBN/ISMN/número editor
    if obra.tipo_registro == 'd':
        if obra.isbn or obra.ismn or obra.numero_editor:
            errores['isbn'] = "Las colecciones manuscritas no utilizan identificadores 020/024/028."
    
    return errores


def validar_obra_en_coleccion(obra):
    """
    Valida que una obra en colección tenga los campos requeridos.
    
    Args:
        obra: Instancia de ObraGeneral con nivel_bibliografico='a'
    
    Returns:
        dict: Diccionario con errores encontrados
    """
    errores = {}
    
    # Verificar que tenga enlaces 773
    if hasattr(obra, 'enlaces_documento_fuente_773'):
        if not obra.enlaces_documento_fuente_773.exists():
            errores['enlaces_documento_fuente_773'] = "Debe registrar al menos un enlace 773 a la colección contenedora."
    
    # Verificar que NO tenga enlaces 774
    if hasattr(obra, 'enlaces_unidades_774'):
        if obra.enlaces_unidades_774.exists():
            errores['enlaces_unidades_774'] = "Las obras individuales no deben registrar 774."
    
    # Verificar que NO tenga relaciones 787
    if hasattr(obra, 'otras_relaciones_787'):
        if obra.otras_relaciones_787.exists():
            errores['otras_relaciones_787'] = "Esta plantilla no utiliza 787."
    
    # Verificar que NO tenga contenidos 505
    if hasattr(obra, 'contenidos_505'):
        if obra.contenidos_505.exists():
            errores['contenidos_505'] = "Las obras individuales no llevan campo 505."
    
    # Validar que manuscritas no tengan ISBN/ISMN/número editor
    if obra.tipo_registro == 'd':
        if obra.isbn or obra.ismn or obra.numero_editor:
            errores['isbn'] = "Las obras manuscritas no usan 020/024/028."
    
    return errores


def validar_obra_independiente(obra):
    """
    Valida que una obra independiente no tenga enlaces incorrectos.
    
    Args:
        obra: Instancia de ObraGeneral con nivel_bibliografico='m'
    
    Returns:
        dict: Diccionario con errores encontrados
    """
    errores = {}
    
    # Verificar que NO tenga enlaces 773
    if hasattr(obra, 'enlaces_documento_fuente_773'):
        if obra.enlaces_documento_fuente_773.exists():
            errores['enlaces_documento_fuente_773'] = "Las obras independientes no utilizan 773."
    
    # Verificar que NO tenga enlaces 774
    if hasattr(obra, 'enlaces_unidades_774'):
        if obra.enlaces_unidades_774.exists():
            errores['enlaces_unidades_774'] = "Las obras independientes no utilizan 774."
    
    # Para obras impresas independientes, el 505 no debe existir
    if obra.tipo_registro == 'c':
        if hasattr(obra, 'contenidos_505'):
            if obra.contenidos_505.exists():
                errores['contenidos_505'] = "Las obras individuales impresas no utilizan 505."
    
    # Validar que manuscritas no tengan ISBN/ISMN/número editor
    if obra.tipo_registro == 'd':
        if obra.isbn or obra.ismn or obra.numero_editor:
            errores['isbn'] = "Las obras manuscritas no usan 020/024/028."
    
    return errores