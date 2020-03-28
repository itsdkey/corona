from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable

from .callbacks import (
    update_daily_cases_graph,
    update_datatable,
    update_log_graph,
    update_metrics,
    update_overall_graph,
)
from .factories import (
    build_cases_datatable_data,
    build_daily_cases_figure,
    build_log_graph,
    build_overall_cases_figure,
    build_template_index,
)
from .settings import COLUMN_TRANSLATION, UPDATE_INTERVAL


def get_app() -> Dash:
    """Return a Dash application."""
    app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/dZVMbK.css'])
    app.index_string = build_template_index()
    app.layout = html.Div(
        html.Div([
            dcc.Interval(
                id='interval-component',
                interval=UPDATE_INTERVAL,
                n_intervals=0,
            ),
            html.Div(
                className='row',
                style={'textAlign': 'center'},
                children=[
                    html.H1(
                        children='Wykres zarażonych przez covid-19',
                    ),
                    html.P(
                        children='Prosta aplikacja dostarczona za pomocą frameworka Dash python',
                    ),
                    html.P(
                        children=f'Aktualizacje co {UPDATE_INTERVAL // (1000 * 60)} minut',
                    ),
                    html.P(
                        id='live-update-text',
                        children='Ostatnia aktualizacja:',
                    ),
                ],
            ),
            html.Div(
                className='row',
                children=[
                    dcc.Graph(
                        id='live-cases-overall-graph',
                        figure=build_overall_cases_figure(),
                    ),
                ],
            ),
            html.Div(
                className='row',
                children=[
                    dcc.Graph(
                        id='live-daily-cases-graph',
                        figure=build_daily_cases_figure(),
                    ),
                ],
            ),
            html.Div(
                className='row',
                children=[
                    dcc.Graph(
                        id='live-log-graph',
                        figure=build_log_graph(),
                    ),
                ],
            ),
            html.Div(
                DataTable(
                    id='live-update-datatable',
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)',
                        },
                        {
                            'if': {
                                'column_id': 'growth_factor',
                                'filter_query': '{growth_factor} <= 1.1',
                            },
                            'color': 'green',
                            'fontWeight': 'bold',
                        },
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                    },
                    style_cell={'textAlign': 'center'},
                    style_table={
                        'maxHeight': '300px',
                        'overflowX': 'scroll',
                        'overflowY': 'scroll',
                    },
                    columns=[{'id': data_key, 'name': column_name} for data_key, column_name in COLUMN_TRANSLATION],
                    data=build_cases_datatable_data(),
                ),
            ),
        ]),
    )

    app.callback(
        Output('live-update-text', 'children'),
        [Input('interval-component', 'n_intervals')],
    )(update_metrics)
    app.callback(
        Output('live-cases-overall-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
    )(update_overall_graph)
    app.callback(
        Output('live-daily-cases-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
    )(update_daily_cases_graph)
    app.callback(
        Output('live-log-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
    )(update_log_graph)
    app.callback(
        Output('live-update-datatable', 'data'),
        [Input('interval-component', 'n_intervals')],
    )(update_datatable)

    return app
