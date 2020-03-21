import os

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

broker_url = os.environ['BROKER_URL']

# List of modules to import when the Celery worker starts.
imports = ('app.tasks',)

enable_utc = True
timezone = 'Europe/Warsaw'

beat_schedule = {
    'save-actual-state': {
        'task': 'app.tasks.save_actual_state',
        'schedule': crontab(minute='*/15'),
        'args': None,
    },
}
