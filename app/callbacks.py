from datetime import datetime

import plotly.graph_objs as go

from .calculations import calculate_growth_factor
from .handlers import read_from_csv, unpack_csv_data


def update_graphs(n):
    """Update graphs."""
    csv_data = read_from_csv()
    data_sets = unpack_csv_data(csv_data)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            **{
                'x': list(data_sets['cases'].keys()),
                'y': list(data_sets['cases'].values()),
                'mode': 'lines+markers',
                'name': 'przypadki',
                'marker': {'color': 'blue'},
            },
        ),
    )
    figure.add_trace(
        go.Scatter(
            **{
                'x': list(data_sets['recovered'].keys()),
                'y': list(data_sets['recovered'].values()),
                'mode': 'lines+markers',
                'name': 'wyleczeni',
                'marker': {'color': '#00ff00'},
            },
        ),
    )
    figure.add_trace(
        go.Scatter(
            **{
                'x': list(data_sets['deaths'].keys()),
                'y': list(data_sets['deaths'].values()),
                'mode': 'lines+markers',
                'name': 'zgony',
                'marker': {'color': 'red'},
            },
        ),
    )
    return figure


def update_metrics(n):
    """Update 'update text'."""
    now = datetime.now().strftime('%d %b %Y %H:%M:%S')
    return f'Ostatnia aktualizacja o: {now}'


def update_datatable(n):
    """Update data table."""
    data = read_from_csv()
    data = calculate_growth_factor(data)
    return [{'date': key, **value} for key, value in data.items()]
