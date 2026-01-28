"""
Señales automáticas para actualización de signatura por cambios en campo 044
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .bloque_0xx import CodigoPaisEntidad


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
