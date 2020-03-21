from celery.utils.log import get_task_logger

from .celery import app
from .handlers import write_to_csv

logger = get_task_logger('server')


@app.task
def save_actual_state() -> None:
    """Snapshot the actual state to a csv file."""
    write_to_csv()
