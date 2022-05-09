from pydoc import classname
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
from pages.common import nav

# layout = html.Div([
#     html.H3('Page 1'),
#     dcc.Dropdown(
#         {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
#         id='page-1-dropdown'
#     ),
#     html.Div(id='page-1-display-value'),
#     dcc.Link('Go to Page 2', href='/page2')
# ])


# @callback(
#     Output('page-1-display-value', 'children'),
#     Input('page-1-dropdown', 'value'))
# def display_value(value):
#     return f'You have selected {value}'


layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='ten columns div-user-controls',
                              children=[
                                  html.H1('Gender Gap in',
                                          className='index-title'),
                                  html.H1('Film Industry', style={
                                        'background-color': '#E0AE0A', 'max-width': '40%'}, className='index-title'),
                                  html.H1('over the Past', style={},
                                          className='index-title'),
                                  html.H1('100 Years', style={},
                                          className='index-title'),
                                  # html.P('Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.Visualising time series with Plotly - Dash.'),
                                  # html.P('Pick one or more stocks from the dropdown below.'),
                                  # nav
                              ]
                              ),
                     html.Div(className='five columns div-user-controls', children=[
                         html.P('Lorem Ipsum is simply dummy text of the \
                        printing and typesetting industry. Lorem Ipsum has been \
                        the industrys standard dummy text ever since the 1500s, when \
                        an unknown printer took a galley of type and scrambled it to make \
                        a type specimen book. It has survived not only five centuries, \
                        but also the leap into electronic typesetting, remaining essentially \
                        unchanged. It was popularised in the 1960s with the release of Letraset \
                        sheets containing Lorem Ipsum passages, and more recently with desktop \
                        publishing software like Aldus PageMaker including versions of Lorem Ipsum.', className='index-description'),
                     ]),
                     html.Div(className='four columns div-user-controls index-author-container',
                              children=[
                                  html.P('Authors: ', className='index-author', style={'margin-bottom': '5px'}),
                                  html.P('Junkai Man',
                                         className='index-author'),
                                  html.P('Ruitian Wu',
                                         className='index-author'),
                                  html.P('Chenglin Zhang',
                                         className='index-author'),
                              ]
                              ),
                 ]),
        html.Div(className='two columns', children=[
            nav,
        ]),
        html.Div(id='', className='', children=[
            html.Img(src='/assets/poster.jpeg', className='poster-img'),
        ])
    ]
)
