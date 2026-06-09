from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        # Import signals to ensure they are registered
        from . import signals  # noqa: F401
