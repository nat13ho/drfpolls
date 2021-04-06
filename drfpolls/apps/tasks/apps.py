from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'drfpolls.apps.tasks'

    def ready(self):
        import drfpolls.apps.tasks.signals
