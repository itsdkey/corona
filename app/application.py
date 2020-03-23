from dash import Dash
from dash_table import DataTable
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app.callbacks import update_graphs, update_metrics, update_datatable
from app.calculations import calculate_growth_factor
from app.handlers import read_from_csv, unpack_csv_data


def get_app():
    csv_data = read_from_csv()
    csv_data = calculate_growth_factor(csv_data)
    data_sets = unpack_csv_data(csv_data)
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyo/pen/bWLwgP.css'])
    app.layout = html.Div(
        html.Div([
            html.H1(id='title', children='Wykres zarażonych przez covid-19.'),
            html.Div(
                id='subtitle',
                children='Prosta aplikacja dostarczona za pomocą frameworka Dash python.',
            ),
            html.Div(
                id='live-update-text',
                children='Ostatnia aktualizacja o: ',
            ),
            dcc.Graph(
                id='live-update-graph',
                figure={
                    'data': [
                        {
                            'x': list(data_sets['cases'].keys()),
                            'y': list(data_sets['cases'].values()),
                            'type': 'line',
                            'name': 'przypadki',
                            'marker': {'color': 'blue'},
                        },
                        {
                            'x': list(data_sets['recovered'].keys()),
                            'y': list(data_sets['recovered'].values()),
                            'type': 'line', 'name': 'wyleczeni',
                            'marker': {'color': '#00ff00'},
                        },
                        {
                            'x': list(data_sets['deaths'].keys()),
                            'y': list(data_sets['deaths'].values()),
                            'type': 'line',
                            'name': 'zgony',
                            'marker': {'color': 'red'},
                        },
                    ],
                    'layout': {
                        'title': 'Wykres zarażonych',
                    },
                },
            ),
            html.Div(
                DataTable(
                    id='live-update-datatable',
                    style_cell={'textAlign': 'center'},
                    columns=[
                        {'name': i[1], 'id': i[0]}
                        for i in [
                            ('date', 'data'),
                            ('cases', 'łączna liczba przypadków'),
                            ('growth_factor', 'współczynnik wzrostu'),
                            ('recovered', 'łączna liczba wyzdrowiało'),
                            ('deaths', 'łączna liczba zgonów'),
                        ]
                    ],
                    data=[{'date': key, **value} for key, value in csv_data.items()],
                ),
            ),
            dcc.Interval(
                id='interval-component',
                interval=1000 * 60 * 15,
                n_intervals=0,
            ),
        ]),
    )

    app.callback(
        Output('live-update-text', 'children'),
        [Input('interval-component', 'n_intervals')],
    )(update_metrics)
    app.callback(
        Output('live-update-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
    )(update_graphs)
    app.callback(
        Output('live-update-datatable', 'data'),
        [Input('interval-component', 'n_intervals')],
    )(update_datatable)

    return app
