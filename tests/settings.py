import os
import sys

# import source code dir
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)
sys.path.insert(0, os.path.join(here, os.pardir))
SITE_ID = 300

DEBUG = True

ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'skskqlqlaskdsd'

AUTOCOMMIT = True


DATABASES = {
    'default': {
        'NAME': 'test.db',
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:foobar@localhost:7687')
NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_MAX_POOL_SIZE = 50

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

INSTALLED_APPS = [
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # Third party
    'django_neomodel',

    # Test
    'tests.someapp',
]

USE_TZ = True
TIME_ZONE = 'UTC'
MIDDLEWARE = []

