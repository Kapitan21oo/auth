from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main', broker='amqp://guest:guest@localhost//', backend='redis://127.0.0.1:6379/1',
             include=['auth_app.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
