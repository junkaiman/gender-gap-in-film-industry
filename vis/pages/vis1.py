from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
from pages.common import nav

layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Number of movies'),
                                html.H2('Fig1: Time River Chart'),
                                html.P('Visualising time series with Plotly - Dash.'),
                                html.P('Pick one or more stocks from the dropdown below.'),
                                html.Div(
                                    children=[
                                        html.Div(className='bottom-nav', style={'position': 'absolute', 'bottom': '10rem'},
                                            children=[
                                                html.A(id='', className='', children=[
                                                    html.Button('<', id='button-prev', n_clicks=0)
                                                ], href='/', style={'margin-right': '2rem'}),
                                                html.A(id='', className='', children=[
                                                    html.Button('>', id='button-next', n_clicks=0),
                                                ], href='/vis2'),
                                            ]
                                        )
                                    ])
                                ]
                            ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                # dcc.Graph(id='timeseries',
                                #     config={'displayModeBar': False},
                                #     animate=True),
                                # dcc.Graph(id='change',
                                #     config={'displayModeBar': False},
                                #     animate=True),
                            ])
                            ])
        ]
)
