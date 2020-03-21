import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyo/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_cases():
    """Gather past cases."""
    past_data = {
        '2020-03-04': 1,
        '2020-03-05': 1,
        '2020-03-06': 5,
        '2020-03-07': 6,
        '2020-03-08': 11,
        '2020-03-09': 17,
        '2020-03-10': 22,
        '2020-03-11': 31,
        '2020-03-12': 50,
        '2020-03-13': 66,
        '2020-03-14': 88,
        '2020-03-15': 109,
        '2020-03-16': 160,
        '2020-03-17': 220,
        '2020-03-18': 269,
        '2020-03-19': 337,
        '2020-03-20': 407,
        '2020-03-21': 452,
    }
    return past_data


def get_recoveries():
    """Gather past recoveries."""
    past_data = {
        '2020-03-04': 0,
        '2020-03-05': 0,
        '2020-03-06': 0,
        '2020-03-07': 0,
        '2020-03-08': 0,
        '2020-03-09': 0,
        '2020-03-10': 0,
        '2020-03-11': 0,
        '2020-03-12': 0,
        '2020-03-13': 0,
        '2020-03-14': 13,
        '2020-03-15': 13,
        '2020-03-16': 13,
        '2020-03-17': 13,
        '2020-03-18': 13,
        '2020-03-19': 13,
        '2020-03-20': 13,
        '2020-03-21': 13,
    }
    return past_data


def get_deaths():
    """Gather past deaths."""
    past_data = {
        '2020-03-04': 0,
        '2020-03-05': 0,
        '2020-03-06': 0,
        '2020-03-07': 0,
        '2020-03-08': 0,
        '2020-03-09': 0,
        '2020-03-10': 0,
        '2020-03-11': 0,
        '2020-03-12': 1,
        '2020-03-13': 2,
        '2020-03-14': 3,
        '2020-03-15': 3,
        '2020-03-16': 4,
        '2020-03-17': 5,
        '2020-03-18': 5,
        '2020-03-19': 5,
        '2020-03-20': 5,
        '2020-03-21': 5,
    }
    return past_data


cases = get_cases()
recoveries = get_recoveries()
deaths = get_deaths()

app.layout = html.Div(
    children=[
        html.H1(children='Wykres zarażonych przez covid-19.'),
        html.Div(children='Prosta aplikacja dostarczona za pomocą frameworka Dash python.'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {
                        'x': list(cases.keys()),
                        'y': list(cases.values()),
                        'type': 'line',
                        'name': 'przypadki',
                        'marker': {'color': 'blue'},
                    },
                    {
                        'x': list(recoveries.keys()),
                        'y': list(recoveries.values()),
                        'type': 'line', 'name': 'wyleczeni',
                        'marker': {'color': '#00ff00'},
                    },
                    {
                        'x': list(deaths.keys()),
                        'y': list(deaths.values()),
                        'type': 'line',
                        'name': 'zgony',
                        'marker': {'color': 'red'},
                    },
                ],
                'layout': {
                    'title': 'Wykres zarażonych',
                    'xaxis': {'type': 'date'},
                },
            },
        ),
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)
