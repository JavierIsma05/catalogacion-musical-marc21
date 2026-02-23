"""
Managers personalizados para consultas frecuentes
"""
from django.db import models


class ObraGeneralManager(models.Manager):
    """Manager con métodos de consulta comunes"""

    def activos(self):
        """Retorna solo obras activas (no eliminadas lógicamente)"""
        return self.filter(activo=True)

    def manuscritas(self):
        """Retorna solo obras manuscritas"""
        return self.filter(tipo_registro='d')

    def impresas(self):
        """Retorna solo obras impresas"""
        return self.filter(tipo_registro='c')

    def colecciones(self):
        """Retorna solo colecciones (nivel c)"""
        return self.filter(nivel_bibliografico='c')

    def obras_independientes(self):
        """Retorna obras independientes (nivel m)"""
        return self.filter(nivel_bibliografico='m')

    def obras_en_coleccion(self):
        """Retorna obras que forman parte de colecciones (nivel a)"""
        return self.filter(nivel_bibliografico='a')

    def con_compositor(self):
        """Retorna obras con compositor asignado (campo 100)"""
        return self.filter(compositor__isnull=False)

    def con_titulo_uniforme(self):
        """Retorna obras con título uniforme principal (campo 130)"""
        return self.filter(titulo_uniforme__isnull=False)

    def por_compositor(self, compositor):
        """
        Retorna obras de un compositor específico
        
        Args:
            compositor: Instancia de AutoridadPersona o ID
        """
        return self.filter(compositor=compositor)

    def buscar_por_titulo(self, termino):
        """
        Búsqueda de obras por título principal
        
        Args:
            termino: Texto a buscar en el título
        """
        return self.filter(titulo_principal__icontains=termino)

    def por_pais(self, codigo_pais):
        """
        Retorna obras asociadas a un país específico
        
        Args:
            codigo_pais: Código ISO del país (ej: 'ec', 'pe')
        """
        return self.filter(codigos_pais_entidad__codigo_pais=codigo_pais).distinct()

    def con_isbn(self):
        """Retorna obras con ISBN registrado"""
        return self.filter(isbn__isnull=False).exclude(isbn='')

    def con_ismn(self):
        """Retorna obras con ISMN registrado"""
        return self.filter(ismn__isnull=False).exclude(ismn='')

    def recientes(self, dias=30):
        """
        Retorna obras creadas recientemente
        
        Args:
            dias: Número de días hacia atrás (default: 30)
        """
        from django.utils import timezone
        from datetime import timedelta
        fecha_limite = timezone.now() - timedelta(days=dias)
        return self.filter(fecha_creacion_sistema__gte=fecha_limite)

    def modificadas_recientemente(self, dias=7):
        """
        Retorna obras modificadas recientemente
        
        Args:
            dias: Número de días hacia atrás (default: 7)
        """
        from django.utils import timezone
        from datetime import timedelta
        fecha_limite = timezone.now() - timedelta(days=dias)
        return self.filter(fecha_modificacion_sistema__gte=fecha_limite)