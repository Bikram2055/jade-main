from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

ENVIRONMENT = os.environ.get("ENVIRONEMT", "dev")
if ENVIRONMENT == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.production")

app = Celery('src.config')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# tasks can be added below
