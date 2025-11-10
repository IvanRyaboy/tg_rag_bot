from celery import Celery
from celery.schedules import crontab
import os

celery = Celery(
    'app_celery',
    broker='redis://redis:6379/2',
    backend='redis://redis:6379/2',
)
celery.autodiscover_tasks(['tasks'])

celery.conf.update(
    timezone='UTC',
    enable_utc=True,
    beat_schedule={}
)
