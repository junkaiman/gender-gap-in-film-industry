from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
# from pages.common import nav
import plotly.graph_objects as go

dframe = pd.read_csv('../data/imdb_all_v2.csv')
df = dframe[(10 <= dframe['star_index']) & (dframe['star_index'] <= 20)]

genre_list = []
for i in range(len(df)):
    try:
        genre_list.append(df.iloc[i]['certificate'].split(','))
    except:
        genre_list.append(None)
df['genre_list'] = genre_list
df = df.explode('genre_list')
df['genre_list'] = df['genre_list'].apply(lambda x: x.strip() if x != None else x)
genre_group = df.groupby('genre_list')

genres = []
number = []
years = []
for genre in genre_group:
    # for year_group in genre[1].groupby('year'):
    for i in range(1920, 2022):
        years.append(i)
        genres.append(genre[0])
        number.append(len(genre[1][genre[1]['year'] == i]))
output = pd.DataFrame(data = [genres, number, years]).T
output.columns = ['genre', 'count', 'year']

trace_dict = {}
all_genre = output['genre'].unique()

for genre in all_genre:
    trace_dict[genre] = go.Scatter(
                            x= output['year'], y = output[output['genre'] == genre]['count'],
                            name = genre,
                            mode = 'none', 
                            stackgroup = 'one', line_shape = 'spline')

fig = go.Figure()
# for genre in ['Adventure', 'Action', 'Drama']:
# for genre in ['R', 'PG-13', 'PG']:
for genre in all_genre:
    fig.add_trace(trace_dict[genre])

fig.update_layout(
    template = 'plotly_dark',
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Number of movies'),
                                html.H2('Fig3: Time River Chart'),
                                html.P('Visualising time series with Plotly - Dash.'),
                                html.P('Pick one or more stocks from the dropdown below.'),
                                html.Div(
                                    children=[
                                        html.Div(className='bottom-nav',
                                            children=[
                                                html.A(id='', className='', children=[
                                                    html.Button('<', id='button-prev', n_clicks=0)
                                                ], href='/vis2', style={'margin-right': '2rem'}),
                                                html.A(id='', className='', children=[
                                                    html.Button('>', id='button-next', n_clicks=0),
                                                ], href='/vis4'),
                                            ]
                                        )
                                    ]),
                                dcc.Dropdown(
                                    output['genre'].unique(),
                                    # all_genre,
                                    ['R', 'PG-13', 'PG'], 
                                    multi = True, id = 'my-check-box'
                                    ),
                                html.Div(style={'margin-top': '30px'}),
                                dcc.RangeSlider(10, 20, 1, tooltip={"placement": "bottom", "always_visible": False},
                                    value=[10, 20], id = 'my-range-slider')
                                # dcc.RangeSlider(1920, 2021, 1, tooltip={"placement": "bottom", "always_visible": False},
                                #         marks={
                                #         1920: '1920', 
                                #         1930: '1930',
                                #         1940: '1940', 
                                #         1950: '1950',
                                #         1960: '1960', 
                                #         1970: '1970',
                                #         1980: '1980', 
                                #         1990: '1990',
                                #         2000: '2000', 
                                #         2010: '2010',
                                #         2020: '2020'
                                #         },
                                #     value=[1920, 2021], id = 'year-range-slider')
                                ]
                            ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id='output-check-box',
                                animate=True,
                                config={'displayModeBar': False},
                                )
                            ])
                    # html.Div(id = 'output-check-box')
                            ])
        ]
)

@callback(
    Output('output-check-box', 'figure'),
    [Input('my-check-box', 'value'),
     Input('my-range-slider', 'value')
    #  Input('year-range-slider', 'value')
     ])
def update_check_box_output(value, value_range):
    df = dframe[(value_range[0] <= dframe['star_index']) & (dframe['star_index'] <= value_range[1])]
    # df = df[(value_year[0] <= df['year']) & (df['year'] <= value_year[1])]
    genre_list = []
    for i in range(len(df)):
        try:
            genre_list.append(df.iloc[i]['certificate'].split(','))
        except:
            genre_list.append(None)
    df['genre_list'] = genre_list
    df = df.explode('genre_list')
    df['genre_list'] = df['genre_list'].apply(lambda x: x.strip() if x != None else x)
    genre_group = df.groupby('genre_list')

    genres = []
    number = []
    years = []
    for genre in genre_group:
        # for year_group in genre[1].groupby('year'):
        for i in range(1920, 2022):
            years.append(i)
            genres.append(genre[0])
            number.append(len(genre[1][genre[1]['year'] == i]))
    output = pd.DataFrame(data = [genres, number, years]).T
    output.columns = ['genre', 'count', 'year']

    trace_dict = {}
    all_genre = output['genre'].unique()

    for genre in all_genre:
        trace_dict[genre] = go.Scatter(
                                x= output['year'], y = output[output['genre'] == genre]['count'],
                                name = genre,
                                mode = 'none', 
                                stackgroup = 'one', line_shape = 'spline')

    fig = go.Figure()
    # for genre in ['Adventure', 'Action', 'Drama']:
    # for genre in ['R', 'PG-13', 'PG']:
    #     fig.add_trace(trace_dict[genre])
    # fig = go.Figure()
    for genre in value:
        fig.add_trace(trace_dict[genre])

    fig.update_layout(
        template = 'plotly_dark',
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


# if __name__ == '__main__':
#     app.run_server(debug=True)
