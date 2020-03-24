from datetime import datetime

from plotly.graph_objs import Figure

from .calculations import calculate_growth_factor
from .factories import build_cases_figure
from .handlers import read_from_csv


def update_graphs(n: int) -> Figure:
    """Update graphs."""
    return build_cases_figure()


def update_metrics(n: int) -> str:
    """Update 'update text'."""
    now = datetime.now().strftime('%d %b %Y %H:%M:%S')
    return f'Ostatnia aktualizacja: {now}'


def update_datatable(n: int) -> list:
    """Update data table."""
    data = read_from_csv()
    data = calculate_growth_factor(data)
    return [{'date': key, **value} for key, value in data.items()]
