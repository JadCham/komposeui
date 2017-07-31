from django.apps import AppConfig
from webapp.kompose.KomposeWrapper import checkKomposeInstall


class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        # Check if kompose is installed
        checkKomposeInstall()
