from django.apps import AppConfig

class ResponsesConfig(AppConfig):
    name = 'responses'

    def ready(self):
        import responses.signals