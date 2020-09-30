from django.apps import AppConfig
from django.conf import settings
from neomodel import config


config.AUTO_INSTALL_LABELS = False


class NeomodelConfig(AppConfig):
    name = 'django_neomodel'
    verbose_name = 'Django neomodel'

    def read_settings(self):
        # Support for older and newer versions of neomodel. If neither work, just use a sane default.
        default_max_pool_size = getattr(config, 'MAX_POOL_SIZE', getattr(config, 'MAX_CONNECTION_POOL_SIZE', 50))
        
        config.DATABASE_URL = getattr(settings, 'NEOMODEL_NEO4J_BOLT_URL', config.DATABASE_URL)
        config.FORCE_TIMEZONE = getattr(settings, 'NEOMODEL_FORCE_TIMEZONE', False)
        config.ENCRYPTED_CONNECTION = getattr(settings, 'NEOMODEL_ENCRYPTED_CONNECTION', True)
        config.MAX_POOL_SIZE = getattr(settings, 'NEOMODEL_MAX_POOL_SIZE', default_max_pool_size)

    def ready(self):
        self.read_settings()
