from datetime import datetime

from plotly.graph_objs import Figure
from pytz import timezone
from redis import Redis

from .calculations import calculate_growth_factor
from .factories import (
    build_daily_cases_figure,
    build_log_graph,
    build_overall_cases_figure,
)
from .handlers import read_from_csv


def update_overall_graph(n: int) -> Figure:
    """Update graph with overall data."""
    return build_overall_cases_figure()


def update_daily_cases_graph(n: int) -> Figure:
    """Update graph with daily cases data."""
    return build_daily_cases_figure()


def update_metrics(n: int) -> str:
    """Update 'update text'."""
    with Redis(db=1) as redis:
        if redis.exists('last-update-at'):
            data_collected_at = datetime.strptime(redis.get('last-update-at').decode(), '%Y-%m-%d %H:%M:%S')
        else:
            data_collected_at = datetime.now(tz=timezone('Europe/Warsaw'))
    display_date = data_collected_at.strftime('%d %b %Y %H:%M:%S')
    return f'Ostatnia aktualizacja: {display_date}'


def update_datatable(n: int) -> list:
    """Update data table."""
    data = read_from_csv()
    data = calculate_growth_factor(data)
    return [{'date': key, **value} for key, value in data.items()]


def update_log_graph(n: int) -> Figure:
    """Update log graph with overall cases."""
    return build_log_graph()
