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
    'save-actual-state-in-redis': {
        'task': 'app.tasks.save_actual_state_in_redis',
        'schedule': crontab(minute='*/15'),
        'args': None,
    },
    'save-redis-to-file': {
        'task': 'app.tasks.save_redis_to_file',
        'schedule': crontab(minute=5, hour=0),
        'args': None,
    },
}
