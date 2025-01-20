from django.apps import AppConfig


class TaskappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskApp'

    def ready(self):
        # Import and start the scheduler
        from .scheduler import start
        start()
