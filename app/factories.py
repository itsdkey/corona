from datetime import date
import locale
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .calculations import calculate_growth_factor
from .handlers import read_collected_data, unpack_csv_data
from .settings import BASE_DIR

locale.setlocale(locale.LC_ALL, '')


def build_template_index():
    with open(os.path.join(BASE_DIR, 'index.html'), encoding='utf-8') as index_file:
        index = index_file.read()
    return index


def build_overall_cases_figure() -> go.Figure:
    """Build a figure that will be used in the overall cases graph."""
    csv_data = read_collected_data()
    data_sets = unpack_csv_data(csv_data)
    figure = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.2,
        subplot_titles=[
            'Wykres ilości potwierdzonych przypadków',
            'Wykres ilości zgonów oraz wyzdrowień',
        ],
    )
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
    csv_data = read_collected_data()
    daily_cases = {
        date.fromisoformat(key_date).strftime('%x'): value['daily_cases'] for key_date, value in csv_data.items()
    }
    figure = go.Figure(
        data=go.Bar(
            x=list(daily_cases.keys()),
            y=list(daily_cases.values()),
        ),
    )
    figure.update_layout(
        title='Ilość nowych przypadków z podziałem na dni',
        xaxis={'type': 'category'},
        height=300,
    )
    return figure


def build_cases_datatable_data():
    """Generate data that will be used in the cases DataTable."""
    csv_data = read_collected_data()
    csv_data = calculate_growth_factor(csv_data)
    return [{'date': key, **value} for key, value in csv_data.items()]


def build_log_graph():
    """Generate data that will be used by the log plot."""
    csv_data = read_collected_data()
    cases = {
        date.fromisoformat(key_date).strftime('%x'): value['cases'] for key_date, value in csv_data.items()
    }
    figure = go.Figure(
        data=go.Scatter(
            x=list(cases.keys()),
            y=list(cases.values()),
        ),
        layout={
            'title': 'Wykres logarytmiczny ilości przypadków w Polsce',
            'yaxis_type': 'log',
            'height': 300,
        },
    )
    return figure
