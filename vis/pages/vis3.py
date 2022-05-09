from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
# from pages.common import nav
import plotly.graph_objects as go

dframe = pd.read_csv('../data/imdb_all_v2.csv')

color_hue = ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f', '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1', 
'#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f', '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1']

female_df = dframe[(15 <= dframe['star_index']) & (dframe['star_index'] <= 20)]
female_genre_list = []
for i in range(len(female_df)):
    try:
        # genre_list.append(df.iloc[i]['genre'].split(','))
        female_genre_list.append(female_df.iloc[i]['certificate'].split(','))
    except:
        female_genre_list.append(None)
female_df['genre_list'] = female_genre_list
female_df = female_df.explode('genre_list')
female_df['genre_list'] = female_df['genre_list'].apply(lambda x: x.strip() if x != None else x)
female_genre_group = female_df.groupby('genre_list')

female_genres = []
female_number = []
female_years = []
for female_genre in female_genre_group:
    # for year_group in genre[1].groupby('year'):
    for i in range(1920, 2022):
        female_years.append(i)
        female_genres.append(female_genre[0])
        female_number.append(len(female_genre[1][female_genre[1]['year'] == i]))
female_output = pd.DataFrame(data = [female_genres, female_number, female_years]).T
female_output.columns = ['genre', 'count', 'year']

female_trace_dict = {}
female_all_genre = female_output['genre'].unique()

for i in range(len(female_all_genre)):
    female_genre = female_all_genre[i]
    female_trace_dict[female_genre] = go.Scatter(
                            x= female_output['year'], y = -female_output[female_output['genre'] == female_genre]['count'],
                            name = female_genre + ' (female)',
                            mode = 'none', 
                            fillcolor = color_hue[i],
                            stackgroup = 'two', line_shape = 'spline')

male_df = dframe[(10 <= dframe['star_index']) & (dframe['star_index'] <= 14)]
male_genre_list = []
for i in range(len(male_df)):
    try:
        # genre_list.append(df.iloc[i]['genre'].split(','))
        male_genre_list.append(male_df.iloc[i]['certificate'].split(','))
    except:
        male_genre_list.append(None)
male_df['genre_list'] = male_genre_list
male_df = male_df.explode('genre_list')
male_df['genre_list'] = male_df['genre_list'].apply(lambda x: x.strip() if x != None else x)
male_genre_group = male_df.groupby('genre_list')

male_genres = []
male_number = []
male_years = []
for male_genre in male_genre_group:
    # for year_group in genre[1].groupby('year'):
    for i in range(1920, 2022):
        male_years.append(i)
        male_genres.append(male_genre[0])
        male_number.append(len(male_genre[1][male_genre[1]['year'] == i]))
male_output = pd.DataFrame(data = [male_genres, male_number, male_years]).T
male_output.columns = ['genre', 'count', 'year']

male_trace_dict = {}
male_all_genre = male_output['genre'].unique()

for i in range(len(female_all_genre)): #####
    male_genre = female_all_genre[i]
    if male_genre != 'Open' and male_genre != 'TV-13':
        male_trace_dict[male_genre] = go.Scatter(
                                x= male_output['year'], y = male_output[male_output['genre'] == male_genre]['count'],
                                name = male_genre + ' (male)',
                                mode = 'none', 
                                fillcolor = color_hue[i],
                                stackgroup = 'one', line_shape = 'spline')

male_list = list(male_output['genre'].unique())
female_list = list(female_output['genre'].unique())

for i in range(len(male_list)):
    male_list[i] = male_list[i] + ' (male)'

for i in range(len(female_list)):
    female_list[i] = female_list[i] + ' (female)'

drop_down_input = male_list + female_list

drop_down_input.sort()

fig = go.Figure()
for genre in ['R', 'PG-13', 'PG']:
    fig.add_trace(female_trace_dict[genre])

for genre in ['R', 'PG-13', 'PG']:
    fig.add_trace(male_trace_dict[genre])

fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(rangeslider=dict(
            visible=True
        ),
        type="date"
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)', width=float('inf'), height=800)
# fig.update_layout(
#     template = 'plotly_dark',
#     xaxis=dict(
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )

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
                                    drop_down_input,
                                    # drop_down_input,
                                    ['R (male)', 'R (female)', 'PG-13 (male)', 'PG-13 (female)', 'PG (male)', 'PG (female)'], 
                                    multi = True, id = 'my-check-box'
                                    ),
                                html.Div(style={'margin-top': '30px'}),
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
    [Input('my-check-box', 'value')
    #  Input('my-range-slider', 'value')
    #  Input('year-range-slider', 'value')
     ])
def update_check_box_output(value):
    # color_hue = ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f', '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1', 
    # '#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f', '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1']

    female_df = dframe[(15 <= dframe['star_index']) & (dframe['star_index'] <= 20)]
    female_genre_list = []
    for i in range(len(female_df)):
        try:
            # genre_list.append(df.iloc[i]['genre'].split(','))
            female_genre_list.append(female_df.iloc[i]['certificate'].split(','))
        except:
            female_genre_list.append(None)
    female_df['genre_list'] = female_genre_list
    female_df = female_df.explode('genre_list')
    female_df['genre_list'] = female_df['genre_list'].apply(lambda x: x.strip() if x != None else x)
    female_genre_group = female_df.groupby('genre_list')

    female_genres = []
    female_number = []
    female_years = []
    for female_genre in female_genre_group:
        # for year_group in genre[1].groupby('year'):
        for i in range(1920, 2022):
            female_years.append(i)
            female_genres.append(female_genre[0])
            female_number.append(len(female_genre[1][female_genre[1]['year'] == i]))
    female_output = pd.DataFrame(data = [female_genres, female_number, female_years]).T
    female_output.columns = ['genre', 'count', 'year']

    female_trace_dict = {}
    female_all_genre = female_output['genre'].unique()

    for i in range(len(female_all_genre)):
        female_genre = female_all_genre[i]
        female_trace_dict[female_genre] = go.Scatter(
                                x= female_output['year'], y = -female_output[female_output['genre'] == female_genre]['count'],
                                name = female_genre + ' (female)',
                                mode = 'none', 
                                fillcolor = color_hue[i],
                                stackgroup = 'two', line_shape = 'spline')

    male_df = dframe[(10 <= dframe['star_index']) & (dframe['star_index'] <= 14)]
    male_genre_list = []
    for i in range(len(male_df)):
        try:
            # genre_list.append(df.iloc[i]['genre'].split(','))
            male_genre_list.append(male_df.iloc[i]['certificate'].split(','))
        except:
            male_genre_list.append(None)
    male_df['genre_list'] = male_genre_list
    male_df = male_df.explode('genre_list')
    male_df['genre_list'] = male_df['genre_list'].apply(lambda x: x.strip() if x != None else x)
    male_genre_group = male_df.groupby('genre_list')

    male_genres = []
    male_number = []
    male_years = []
    for male_genre in male_genre_group:
        # for year_group in genre[1].groupby('year'):
        for i in range(1920, 2022):
            male_years.append(i)
            male_genres.append(male_genre[0])
            male_number.append(len(male_genre[1][male_genre[1]['year'] == i]))
    male_output = pd.DataFrame(data = [male_genres, male_number, male_years]).T
    male_output.columns = ['genre', 'count', 'year']

    male_trace_dict = {}
    male_all_genre = male_output['genre'].unique()

    for i in range(len(female_all_genre)): #####
        male_genre = female_all_genre[i]
        if male_genre != 'Open' and male_genre != 'TV-13':
            male_trace_dict[male_genre] = go.Scatter(
                                    x= male_output['year'], y = male_output[male_output['genre'] == male_genre]['count'],
                                    name = male_genre + ' (male)',
                                    mode = 'none', 
                                    fillcolor = color_hue[i],
                                    stackgroup = 'one', line_shape = 'spline') 

    fig = go.Figure()
    for genre in value:
        if '(female)' in genre:
            fig.add_trace(female_trace_dict[genre.split('(')[0][:-1]])

    for genre in value:
        if '(male)' in genre and (genre != 'Open (male)') and (genre != 'TV-13 (male)'):
            fig.add_trace(male_trace_dict[genre.split('(')[0][:-1]])

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(rangeslider=dict(
                visible=True
            ),
            type="date"
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)', width=float('inf'), height=800)
    # fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
    #               plot_bgcolor='rgba(0, 0, 0, 0)')
    return fig


# if __name__ == '__main__':
#     app.run_server(debug=True)
