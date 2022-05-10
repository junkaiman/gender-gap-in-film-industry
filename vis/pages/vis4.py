from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
from pages import common



layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                # html.H2('Number of movies'),
                                html.H2('Fig4: Theme Word Cloud'),
                                html.P('To measure the frequency of words in description of actor-dominant and actress-dominant movies, we build two word clouds and portrait their differences based on the plots. We calculated a gender index to represent whether the movie is actor-dominated or actress-dominated using the cast data. We partitioned the movies into two groups according to their gender index. From the word clouds, we can find some general similar topics shared by the two groups like "life", "love" and "family". However, for actor-dominant ones, there are also topics related to "war", "world" and "murder", which are rarely observed in the other plot. For actress-dominant ones, some words like "girl", "wife" and "mother" are observed, indicating more explorations in self-identity in these movies.'),
                                # html.P('Pick one or more stocks from the dropdown below.'),
                                html.Div(
                                    children=[
                                        html.Div(className='bottom-nav',
                                            children=[
                                                html.A(id='', className='', children=[
                                                    html.Button('<', id='button-prev', n_clicks=0)
                                                ], href=common.base_url+'/vis3', style={'margin-right': '2rem'}),
                                                html.A(id='', className='', children=[
                                                    html.Button('>', id='button-next', n_clicks=0),
                                                ], href=common.base_url+'/vis5'),
                                            ]
                                        )
                                    ])
                                ]
                            ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                html.Div(style={'margin-top': '5rem'}),
                                html.Iframe(src="./assets/male_word.html", style={'height': '40%'}),
                                html.Div(style={'margin-top': '4rem'}),
                                html.Iframe(src="./assets/female_word.html", style={'height': '40%'}, ),
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
