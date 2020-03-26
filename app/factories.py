from datetime import date
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .calculations import calculate_growth_factor
from .handlers import read_from_csv, unpack_csv_data
from .settings import BASE_DIR


def build_template_index():
    with open(os.path.join(BASE_DIR, 'index.html'), encoding='utf-8') as index_file:
        index = index_file.read()
    return index


def build_overall_cases_figure() -> go.Figure:
    """Build a figure that will be used in the overall cases graph."""
    csv_data = read_from_csv()
    data_sets = unpack_csv_data(csv_data)
    figure = make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    figure.append_trace(
        trace=go.Scatter(
            x=list(data_sets['cases'].keys()),
            y=list(data_sets['cases'].values()),
            mode='lines+markers',
            name='przypadki',
            marker={'color': 'blue'},
        ),
        row=1,
        col=1,
    )
    figure.append_trace(
        trace=go.Scatter(
            x=list(data_sets['recovered'].keys()),
            y=list(data_sets['recovered'].values()),
            mode='lines+markers',
            name='wyzdrowiali',
            marker={'color': '#00ff00'},
        ),
        row=2,
        col=1,
    )
    figure.append_trace(
        trace=go.Scatter(
            x=list(data_sets['deaths'].keys()),
            y=list(data_sets['deaths'].values()),
            mode='lines+markers',
            name='zgony',
            marker={'color': 'red'},
        ),
        row=2,
        col=1,
    )
    return figure


def build_daily_cases_figure():
    csv_data = read_from_csv()
    daily_cases = {
        date.fromisoformat(key_date): value['daily_cases'] for key_date, value in csv_data.items()
    }
    figure = go.Figure(
        data=go.Bar(
            x=list(daily_cases.keys()),
            y=list(daily_cases.values()),
        ),
    )
    figure.update_layout(
        title='Ilość nowych przypadków z podziałem na dni',
        xaxis_tickformat='%-d %B %Y',
    )
    return figure


def build_cases_datatable_data():
    """Generate data that will be used in the cases DataTable."""
    csv_data = read_from_csv()
    csv_data = calculate_growth_factor(csv_data)
    return [{'date': key, **value} for key, value in csv_data.items()]
