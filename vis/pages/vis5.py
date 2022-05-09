import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from pages.common import nav

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


data = pd.read_csv('../data/bubble_chart.csv')
top500 = data.sort_values('num_votes', ascending=False)[:500]
top500["rank"] = top500.groupby("year")["differ"].rank("dense", ascending=True)


hover_text = []
for index, row in top500.iterrows():
    hover_text.append(('Title: {title}<br>' +
                      'Number of Votes: {vote}<br>' +
                       'Difference: {rate}<br>' +
                       'Certificate: {cert}<br>' +
                       'Year: {year}').format(title=row['title'],
                                              vote=row['num_votes'],
                                              rate=row['differ'],
                                              cert=row['certificate'],
                                              year=row['year']))
colorline = top500['all']
fig = go.Figure()
sizeref = 2.*max(top500['num_votes'])/200
fig.add_trace(go.Scatter(
    x=top500['year'], y=top500['rank'],
    mode='markers', text=hover_text,
    hoverinfo='text',
    marker=dict(color=colorline,
                colorbar=dict(
                    tickfont=dict(
                        size=10),
                    title=dict(
                        side='top',
                        text='Gender Gap',
                        font=dict(size=12)
                    )
                ),
                colorscale='greens',
                opacity=0.8, size=top500['num_votes'],
                sizemode='area', sizeref=sizeref,
                sizemin=4, showscale=True
                )))
fig.update_layout(title="Aggregated film preferences for both male and female audience",
                  title_font_size=20, template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  width=float('inf'), height=400)
fig.update_xaxes(title_text='Year',
                 title_font=dict(size=15, family='Verdana',
                                 color='purple'),
                 tickfont=dict(family='Calibri', color='black',
                               size=10))
fig.update_yaxes(title_text="Count", range=(0, top500['rank'].max()+1),
                 title_font=dict(size=15, family='Verdana',
                                 color='orange'),
                 tickfont=dict(family='Calibri', color='black',
                               size=10))

hover_text2 = []
for index, row in top500.iterrows():
    hover_text2.append(('Title: {title}<br>' +
                        'Number of Votes: {vote}<br>' +
                       'Difference: {rate}<br>' +
                        'Certificate: {cert}<br>' +
                        'Year: {year}').format(title=row['title'],
                                               vote=row['num_votes'],
                                               rate=row['differ'],
                                               cert=row['certificate'],
                                               year=row['year']))
colorline = top500['differ']
fig2 = go.Figure()
sizeref = 2.*max(top500['num_votes'])/200
fig2.add_trace(go.Scatter(
    x=top500['year'], y=top500['rank'],
    mode='markers', text=hover_text2,
    hoverinfo='text',
    marker=dict(color=colorline,
                colorbar=dict(
                    tickfont=dict(
                        size=10),
                    title=dict(
                        side='top',
                        text='Gender Gap',
                        font=dict(size=12)
                    )
                ),
                colorscale='rdbu',
                opacity=0.8, size=top500['num_votes'],
                sizemode='area', sizeref=sizeref,
                sizemin=4, showscale=True
                )))
fig2.update_layout(title="Difference in film preferences between male and female audience",
                   title_font_size=20, template='plotly_dark', paper_bgcolor='rgba(0, 0, 0, 0)',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   width=float('inf'), height=400)
fig2.update_xaxes(title_text='Year',
                  title_font=dict(size=15, family='Verdana',
                                  color='purple'),
                  tickfont=dict(family='Calibri', color='black',
                                size=10))
fig2.update_yaxes(title_text="Count", range=(0, top500['rank'].max()+1),
                  title_font=dict(size=15, family='Verdana',
                                  color='orange'),
                  tickfont=dict(family='Calibri', color='black',
                                size=10))

bubblechart1 = fig

bubblechart2 = fig2


layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2('Number of movies'),
                                  html.H2('Fig5: Bubble Chart'),
                                  html.P(
                                      'Visualising time series with Plotly - Dash.'),
                                  html.P(
                                      'Pick one or more stocks from the dropdown below.'),
                                  html.Div(
                                      children=[
                                          html.Div(className='bottom-nav',
                                                   children=[
                                                       html.A(id='', className='', children=[
                                                           html.Button(
                                                             '<', id='button-prev', n_clicks=0)
                                                       ], href='/vis4', style={'margin-right': '2rem'}),
                                                       html.A(id='', className='', children=[
                                                           html.Button(
                                                              '>', id='button-next', n_clicks=0),
                                                       ], href='/vis5'),
                                                   ]
                                                   )
                                      ])
                              ],
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id='bubble1',
                                            config={'displayModeBar': False},
                                            animate=True, figure=bubblechart1),
                                  dcc.Graph(id='bubble2',
                                            config={'displayModeBar': False},
                                            animate=True, figure=bubblechart2),
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
