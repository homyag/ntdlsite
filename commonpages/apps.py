from django.apps import AppConfig


class CommonpagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commonpages'

    def ready(self):
        import commonpages.signals
