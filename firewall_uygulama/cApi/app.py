from django.apps import AppConfig

class CapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cApi'
    def ready(self):
        import cApi.signals 
