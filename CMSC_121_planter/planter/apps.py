from django.apps import AppConfig


class PlanterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'planter'

    def ready(self):
        import planter.signals
