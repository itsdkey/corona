from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app.callbacks import update_graphs, update_metrics
from app.handlers import read_from_csv, unpack_csv_data


def get_app():
    csv_data = read_from_csv()
    data_sets = unpack_csv_data(csv_data)
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyo/pen/bWLwgP.css'])
    app.layout = html.Div(
        html.Div([
            html.H1(id='title', children='Wykres zarażonych przez covid-19.'),
            html.Div(
                id='subtitle',
                children='Prosta aplikacja dostarczona za pomocą frameworka Dash python.',
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
                id='live-update-text',
                children='Ostatnia aktualizacja o: ',
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

    return app
