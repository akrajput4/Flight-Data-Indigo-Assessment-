import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_config.settings')

# Create a new Celery instance
celery_app = Celery('flight_config')

# Configure Celery using the Django settings
celery_app.config_from_object('flight_config.celery_config')

# celery_app.conf.timezone = settings.TIME_ZONE

# Automatically discover and import tasks from all registered Django app configs
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {

}
