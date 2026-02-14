from django.apps import AppConfig

class ApplicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications"

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import seed_stages
        post_migrate.connect(seed_stages, sender=self)
