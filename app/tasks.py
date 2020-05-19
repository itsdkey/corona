from datetime import datetime
import json

from celery.utils.log import get_task_logger
from pytz import timezone

from .celery import app
from .handlers import (
    get_actual_state,
    get_redis_instance,
    read_collected_data,
    write_to_csv,
)

logger = get_task_logger('server')


@app.task
def save_actual_state_in_redis() -> None:
    """Snapshot the actual state to Redis."""
    past_data = read_collected_data()
    actual_data = get_actual_state()
    gathered_data = {**past_data, **actual_data}
    cases_overall = 0
    for key, value in gathered_data.items():
        daily_cases = value['cases'] - cases_overall
        cases_overall = value['cases']
        gathered_data[key] = {'date': key, 'daily_cases': daily_cases, **value}

    with get_redis_instance() as redis:
        pipe = redis.pipeline()
        pipe.set('corona-database', json.dumps(gathered_data))
        pipe.set('last-update-at', datetime.now(tz=timezone('Europe/Warsaw')).strftime('%Y-%m-%d %H:%M:%S'))
        pipe.execute()


@app.task
def save_redis_to_file() -> None:
    """Save the collected data in Redis to a CSV file as a backup."""
    with get_redis_instance() as redis:
        try:
            collected = json.loads(redis.get('corona-database').decode())
        except AttributeError:
            return
        write_to_csv(collected)
