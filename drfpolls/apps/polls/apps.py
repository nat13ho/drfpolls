from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'drfpolls.apps.polls'

    def ready(self):
        import drfpolls.apps.polls.signals

