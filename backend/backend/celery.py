from __future__ import absolute_import, unicode_literals
import os

import django
from celery import Celery

ENV = os.environ.get('ENV', 'local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')

django.setup()

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
