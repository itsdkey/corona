import os

from plotly.graph_objs import Figure, Scatter

from .calculations import calculate_growth_factor
from .handlers import read_from_csv, unpack_csv_data
from .settings import BASE_DIR


def build_template_index():
    with open(os.path.join(BASE_DIR, 'index.html'), encoding='utf-8') as index_file:
        index = index_file.read()
    return index


def build_cases_figure() -> Figure:
    """Build a figure that will be used in the cases graph."""
    csv_data = read_from_csv()
    data_sets = unpack_csv_data(csv_data)
    figure = Figure(
        data={
            'data': [
                Scatter(
                    **{
                        'x': list(data_sets['cases'].keys()),
                        'y': list(data_sets['cases'].values()),
                        'mode': 'lines+markers',
                        'name': 'przypadki',
                        'marker': {'color': 'blue'},
                    },
                ),
                Scatter(
                    **{
                        'x': list(data_sets['recovered'].keys()),
                        'y': list(data_sets['recovered'].values()),
                        'mode': 'lines+markers',
                        'name': 'wyleczeni',
                        'marker': {'color': '#00ff00'},
                    },
                ),
                Scatter(
                    **{
                        'x': list(data_sets['deaths'].keys()),
                        'y': list(data_sets['deaths'].values()),
                        'mode': 'lines+markers',
                        'name': 'zgony',
                        'marker': {'color': 'red'},
                    },
                ),
            ],
        },
    )
    return figure


def build_cases_datatable_data():
    """Generate data that will be used in the cases DataTable."""
    csv_data = read_from_csv()
    csv_data = calculate_growth_factor(csv_data)
    return [{'date': key, **value} for key, value in csv_data.items()]
