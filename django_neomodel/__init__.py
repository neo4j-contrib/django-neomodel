__author__ = 'Robin Edwards'
__email__ = 'robin.ge@gmail.com'
__license__ = 'MIT'
__package__ = 'django_neomodel'
__version__ = '0.0.1'


default_app_config = 'django_neomodel.apps.NeomodelConfig'


from django.db.models import signals
from django.conf import settings


def signal_exec_hook(hook_name, self, *args, **kwargs):
    if hasattr(self, hook_name):
        getattr(self, hook_name)(*args, **kwargs)

    if getattr(settings, 'NEOMODEL_SIGNALS', True) and hasattr(signals, hook_name):
        sig = getattr(signals, hook_name)
        sig.send(sender=self.__class__, instance=self)
