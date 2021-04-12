from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'apps.polls'

    def ready(self):
        import apps.polls.signals

