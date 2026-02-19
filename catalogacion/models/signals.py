"""
Señales automáticas para:
- Actualización de signatura por cambios en campo 044
- Bidireccionalidad 773 $w ↔ 774 $w
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .bloque_0xx import CodigoPaisEntidad
from .bloque_7xx import (
    NumeroControl773,
    EnlaceUnidadConstituyente774,
    NumeroControl774,
)


@receiver(post_save, sender=CodigoPaisEntidad)
@receiver(post_delete, sender=CodigoPaisEntidad)
def actualizar_signatura_por_cambio_pais(sender, instance, **kwargs):
    """
    Actualiza automáticamente la signatura de la obra cuando se cambia un código de país.
    
    Esta señal se dispara cuando:
    - Se crea un nuevo código de país (post_save)
    - Se modifica un código de país existente (post_save)  
    - Se elimina un código de país (post_delete)
    
    Args:
        sender: Modelo CodigoPaisEntidad
        instance: Instancia del código de país modificado
        **kwargs: Argumentos adicionales de la señal
    """
    print(f"🚀 SEÑAL DISPARADA: {sender.__name__} - País: {instance.codigo_pais} - Obra: {instance.obra.num_control if instance.obra else 'None'}")
    
    try:
        obra = instance.obra
        
        # Verificar que la obra tenga los campos necesarios para generar signatura
        if obra.centro_catalogador and obra.num_control:
            # Importamos aquí para evitar importación circular
            from .utils import generar_signatura_completa, obtener_pais_principal
            
            # Generar nueva signatura con el país actualizado
            nueva_signatura = generar_signatura_completa(obra)
            pais_actual = obtener_pais_principal(obra)
            
            print(f"🔍 DEBUG: País actual = {pais_actual}")
            print(f"🔍 DEBUG: Nueva signatura = {nueva_signatura}")
            print(f"🔍 DEBUG: signatura_publica_display = {obra.signatura_publica_display}")
            
            # Forzar la recalculación de properties relacionadas con el país
            # Esto asegura que las views y templates obtengan el valor actualizado
            
            # Invalidar caché de properties si existe
            if hasattr(obra, '_signatura_completa_cache'):
                delattr(obra, '_signatura_completa_cache')
            if hasattr(obra, '_signatura_publica_display_cache'):
                delattr(obra, '_signatura_publica_display_cache')
            
            # Log para debugging
            import logging
            logger = logging.getLogger('marc21')
            logger.info(
                f"✅ Signatura actualizada automáticamente por cambio de país: "
                f"Obra {obra.num_control} - Nueva signatura: {nueva_signatura}"
            )
            
        else:
            print(f"❌ Obra sin campos necesarios: centro={obra.centro_catalogador}, num_control={obra.num_control}")

    except Exception as e:
        # Log del error pero sin interrumpir la operación
        print(f"❌ ERROR en señal: {str(e)}")
        import logging
        logger = logging.getLogger('marc21')
        logger.error(
            f"❌ Error al actualizar signatura por cambio de país: {str(e)}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Bidireccionalidad 773 $w ↔ 774 $w
# ─────────────────────────────────────────────────────────────────────────────

@receiver(post_save, sender=NumeroControl773)
def sincronizar_774_al_guardar_773(sender, instance, created, **kwargs):
    """
    Al guardar un 773 $w (obra hijo → colección padre), busca en la colección
    un 774 cuyo $t coincide con el título de la obra hijo y le asigna el $w.
    Si no existe ese 774 en la colección, lo crea completo ($a + $t + $w).

    Nota: en MARC21 el 774 de la colección describe la obra HIJO, por lo que
    $t debe ser el título de la obra hijo, no el título de la colección.
    """
    try:
        obra_hijo  = instance.enlace_773.obra
        obra_padre = instance.obra_relacionada

        # Título y compositor de la obra hijo (usados en el 774 de la colección)
        titulo_hijo  = obra_hijo.titulo_240 or obra_hijo.titulo_uniforme
        persona_hijo = obra_hijo.compositor

        if not titulo_hijo or not persona_hijo:
            return  # Sin datos suficientes para crear/vincular el 774

        # Buscar en la colección si ya existe un 774 con el $t del hijo
        enlace_774 = obra_padre.enlaces_unidades_774.filter(titulo=titulo_hijo).first()

        if not enlace_774:
            # La colección no tenía ese 774: crearlo completo ($a + $t)
            enlace_774 = EnlaceUnidadConstituyente774.objects.create(
                obra=obra_padre,
                encabezamiento_principal=persona_hijo,
                titulo=titulo_hijo,
            )

        # Asegurar que el $w apunta al hijo
        NumeroControl774.objects.get_or_create(
            enlace_774=enlace_774,
            obra_relacionada=obra_hijo,
        )

    except Exception as e:
        import logging
        logging.getLogger('marc21').error(
            f"Error en sincronizar_774_al_guardar_773: {e}"
        )


@receiver(post_delete, sender=NumeroControl773)
def limpiar_774_al_borrar_773(sender, instance, **kwargs):
    """
    Al borrar un 773 $w, borra el 774 $w correspondiente en la colección padre.
    Si el 774 queda sin $w (fue creado automáticamente), lo elimina también.
    """
    try:
        obra_hijo  = instance.enlace_773.obra
        obra_padre = instance.obra_relacionada

        titulo_hijo = obra_hijo.titulo_240 or obra_hijo.titulo_uniforme
        if not titulo_hijo:
            return

        enlace_774 = obra_padre.enlaces_unidades_774.filter(titulo=titulo_hijo).first()
        if enlace_774:
            enlace_774.numeros_control.filter(obra_relacionada=obra_hijo).delete()
            if not enlace_774.numeros_control.exists():
                enlace_774.delete()

    except Exception:
        pass  # La obra o el enlace ya pueden haber sido eliminados en cascada
