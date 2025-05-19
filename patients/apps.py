from django.apps import AppConfig

class PatientsConfig(AppConfig):
    name = 'patients'

    def ready(self):
        # Import here so Django picks up the signal handlers:
        import patients.signals