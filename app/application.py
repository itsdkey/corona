import dash
import dash_core_components as dcc
import dash_html_components as html

from app.handlers import read_from_csv


def get_app():
    data_sets = read_from_csv()
    app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyo/pen/bWLwgP.css'])
    app.layout = html.Div(
        children=[
            html.H1(children='Wykres zarażonych przez covid-19.'),
            html.Div(children='Prosta aplikacja dostarczona za pomocą frameworka Dash python.'),
            dcc.Graph(
                id='example-graph',
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
        ],
    )
    return app
