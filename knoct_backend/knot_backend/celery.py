import os
from celery import Celery
from .settings import BASE_REDIS_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knot_backend.settings')

app = Celery('knot_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'