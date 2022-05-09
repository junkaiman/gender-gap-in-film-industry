from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
# from pages.common import nav

# app = Dash(__name__)

dframe = pd.read_csv('../data/imdb_all_v2.csv')
gender_frame = pd.read_csv('../data/gender.csv')

star_list = []
star_id_list = []
for i in range(0, len(dframe)):
    try:
        star_split = dframe['star'][i].split(',')
        id_split = dframe['star_id'][i].split(',')
        if len(star_split) == len(id_split):
            star_list += star_split
            star_id_list += id_split
    except:
        pass
    
name_id = pd.DataFrame(data = [star_list, star_id_list]).T
name_id = name_id.drop_duplicates()
name_id.columns = ['name', 'id']
name_id = name_id.set_index('id')
gender_frame = gender_frame.set_index('id')

name_id_gender = name_id.join(gender_frame, how = 'outer', on = 'id')
name_id_gender = name_id_gender.drop_duplicates('name')
name_id_gender = name_id_gender.set_index('name')

df = dframe[(1989 <= dframe['year']) & (dframe['year'] <= 2021)]
df = df.sort_values('num_votes', ascending = False).reset_index(drop = True)
df = df.iloc[0:100].reset_index(drop = True)

edges = []
nodes = []
for i in range(0, len(df)):
    try:
        this_star_list = df['star'][i].split(',')
        if len(this_star_list) == 4:
            nodes += this_star_list
            for m in range(len(this_star_list)):
                for n in range(m + 1, len(this_star_list)):
                    edges.append((this_star_list[m], this_star_list[n]))
    except:
        pass

G = nx.Graph(edges)
pos = nx.spring_layout(G)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.3, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    
node_adjacencies = []
node_gender = []
node_text = []

for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    try:
        node_gender.append(name_id_gender.loc[adjacencies[0]]['gender'])
            
    except:
        node_gender.append(None)
    node_text.append(str(adjacencies[0]) + ': ' + str(len(adjacencies[1])) + ' co-occurences')
    
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='Bluered',
        # reversescale = True,
        color = node_gender,
        opacity = 0.9,
        size = node_adjacencies,
        line_width = 0))
    
node_trace.text = node_text   

fig = go.FigureWidget(data=[edge_trace, node_trace],
             layout=go.Layout(
                # title='Movie Star Co-occurences',
                # titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                plot_bgcolor='black',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), width=float('inf'), height=800)
                )

layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Number of movies'),
                                html.H2('Fig2: Co-stardom Network'),
                                html.P('Visualising time series with Plotly - Dash.'),
                                html.P('Pick one or more stocks from the dropdown below.'),
                                html.Div(
                                    children=[
                                        html.Div(className='bottom-nav',
                                            children=[
                                                html.A(id='', className='', children=[
                                                    html.Button('<', id='button-prev', n_clicks=0)
                                                ], href='/vis1', style={'margin-right': '2rem'}),
                                                html.A(id='', className='', children=[
                                                    html.Button('>', id='button-next', n_clicks=0),
                                                ], href='/vis3'),
                                            ]
                                        )
                                    ]),
                                dcc.RangeSlider(1920, 2021, 1, tooltip={"placement": "bottom", "always_visible": False},
                                        marks={
                                        1920: '1920', 
                                        1930: '1930',
                                        1940: '1940', 
                                        1950: '1950',
                                        1960: '1960', 
                                        1970: '1970',
                                        1980: '1980', 
                                        1990: '1990',
                                        2000: '2000', 
                                        2010: '2010',
                                        2020: '2020'
                                        },
                                    value=[1989, 2021], id = 'my-range-slider')
                                ]
                            ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id='output-container-range-slider',
                                animate=True,
                                config={'displayModeBar': False},
                                # animation_options={
                                #     'frame': {'redraw': False},
                                #     'transition': {
                                #         'duration': 10000,
                                #         'ease': 'linear'
                                #     }
                                # }
                                )
                            ])
                            ]),
        ]
)


@callback(
    Output('output-container-range-slider', 'figure'),
    [Input('my-range-slider', 'value')])
def update_output(value):
    df = dframe[(value[0] <= dframe['year']) & (dframe['year'] <= value[1])]
    df = df.sort_values('num_votes', ascending = False).reset_index(drop = True)
    df = df.iloc[0:100].reset_index(drop = True)

    edges = []
    nodes = []
    for i in range(0, len(df)):
        try:
            this_star_list = df['star'][i].split(',')
            if len(this_star_list) == 4:
                nodes += this_star_list
                for m in range(len(this_star_list)):
                    for n in range(m + 1, len(this_star_list)):
                        edges.append((this_star_list[m], this_star_list[n]))
        except:
            pass

    G = nx.Graph(edges)
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_adjacencies = []
    node_gender = []
    node_text = []

    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        try:
            if name_id_gender.loc[adjacencies[0]]['gender'] == 1: # MALE
                node_gender.append('#9cccf9')
                # node_gender.append('#51a5d6')
            else:
                node_gender.append('#e9909d')
                # node_gender.append('#e73643')
            # node_gender.append(name_id_gender.loc[adjacencies[0]]['gender'])

        except:
            node_gender.append(None)
        node_text.append(str(adjacencies[0]) + ': ' + str(len(adjacencies[1])) + ' co-occurences')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            # showscale=True,
            # colorscale='Bluered',
            color = node_gender,
            opacity = 0.9,
            size = node_adjacencies,
            line_width = 0))

    node_trace.text = node_text   

    with fig.batch_update():
        fig.data[0].x = edge_trace.x
        fig.data[0].y = edge_trace.y
        fig.data[1].marker = node_trace.marker
        fig.data[1].text = node_trace.text
        fig.data[1].x = node_trace.x
        fig.data[1].y = node_trace.y
    
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)')
    
    return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)
