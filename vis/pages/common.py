from dash import dcc, html, Input, Output, callback


nav = html.Div(
    children=[
        html.Div(className='bottom-nav',  style={'position': 'absolute', 'bottom': '10rem'},
            children=[
                html.A(id='', className='', children=[
                    html.Button('<', id='button-prev', n_clicks=0)
                ], href='/', style={'margin-right': '2rem'}),
                html.A(id='', className='', children=[
                    html.Button('>', id='button-next', n_clicks=0),
                ], href='/vis1'),
            ]
        )
    ]
)