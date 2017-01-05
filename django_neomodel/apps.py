from django.apps import AppConfig
from django.conf import settings
from neomodel import config


config.AUTO_INSTALL_LABELS = False


class NeomodelConfig(AppConfig):
    name = 'django_neomodel'
    verbose_name = 'Django neomodel'

    def read_settings(self):
        config.DATABASE_URL = getattr(settings, 'NEOMODEL_NEO4J_BOLT_URL', config.DATABASE_URL)

    def ready(self):
        self.read_settings()