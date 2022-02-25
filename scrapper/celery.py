"""
  import needed things
"""
from __future__ import absolute_import
import os
from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapper.settings')
APP = Celery('scrapper')

APP.config_from_object('django.conf:settings')
APP.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@APP.task(bind=True)
def debug_task(self):
    """
        debug_task
    """
    print('Request: {0!r}'.format(self.request))
