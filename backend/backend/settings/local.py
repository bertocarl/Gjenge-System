from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'trans',
        'USER': 'postgres',
        'PASSWORD': 'fiddlediddle',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

SHELL_PLUS_POST_IMPORTS = [
    ('apps.api.factories', '*')
]

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/%2f'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
