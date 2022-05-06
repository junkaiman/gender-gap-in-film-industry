
from dash import Dash, html, dcc, Input, Output, callback
from pages import index, vis1, vis2, vis3, vis4, vis5, networktest
import plotly.express as px
import pandas as pd
import networkx as nx

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/vis1':
        return vis1.layout
    elif pathname == '/vis2':
        return vis2.layout
    elif pathname == '/vis3':
        return vis3.layout
    elif pathname == '/vis4':
        return vis4.layout
    elif pathname == '/vis5':
        return vis5.layout
    elif pathname == '/networktest':
        return networktest.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
