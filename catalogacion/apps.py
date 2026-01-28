from django.apps import AppConfig


class CatalogacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogacion'
    
    def ready(self):
        """Importar señales cuando la app esté lista"""
        print("🔧 Cargando señales automáticas de actualización de país...")
        import catalogacion.models.signals  # noqa: F401
        print("✅ Señales cargadas correctamente")
