from django.apps import AppConfig


class CardiocareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cardiocare'

    def ready(self):
        import cardiocare.signals