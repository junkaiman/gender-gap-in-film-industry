from dash import dcc, html, Input, Output, callback, Dash
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
from pages import common

master = pd.read_csv('../data/bubble_chart.csv')


def move_particle(x):
    if x[-1] == ',':
        return x[:-1]
    else:
        return x


PI = np.pi


def check_data(data_matrix):
    L, M = data_matrix.shape
    if L != M:
        raise ValueError('Data array must have (n,n) shape')
    return L


def moduloAB(x, a, b):  # maps a real number onto the unit circle identified with
    # the interval [a,b), b-a=2*PI
    if a >= b:
        raise ValueError('Incorrect interval ends')
    y = (x-a) % (b-a)
    return y+b if y < 0 else y+a


def test_2PI(x):
    return 0 <= x < 2*PI


def get_ideogram_ends(ideogram_len, gap):
    ideo_ends = []
    left = 0
    for k in range(len(ideogram_len)):
        right = left+ideogram_len[k]
        ideo_ends.append([left, right])
        left = right+gap
    return ideo_ends


def map_data(L, data_matrix, row_value, ideogram_length):
    mapped = np.zeros(data_matrix.shape)
    for j in range(L):
        mapped[:, j] = ideogram_length*data_matrix[:, j]/row_value
    return mapped


def make_ideogram_arc(R, phi, a=50):
    # R is the circle radius
    # phi is the list of ends angle coordinates of an arc
    # a is a parameter that controls the number of points to be evaluated on an arc
    if not test_2PI(phi[0]) or not test_2PI(phi[1]):
        phi = [moduloAB(t, 0, 2*PI) for t in phi]
    length = (phi[1]-phi[0]) % 2*PI
    nr = 5 if length <= PI/4 else int(a*length/PI)

    if phi[0] < phi[1]:
        theta = np.linspace(phi[0], phi[1], nr)
    else:
        phi = [moduloAB(t, -PI, PI) for t in phi]
        theta = np.linspace(phi[0], phi[1], nr)
    return R*np.exp(1j*theta)


def make_ribbon_ends(mapped_data, ideo_ends,  idx_sort):
    L = mapped_data.shape[0]
    ribbon_boundary = np.zeros((L, L+1))
    for k in range(L):
        start = ideo_ends[k][0]
        ribbon_boundary[k][0] = start
        for j in range(1, L+1):
            J = idx_sort[k][j-1]
            ribbon_boundary[k][j] = start+mapped_data[k][J]
            start = ribbon_boundary[k][j]
    return [[(ribbon_boundary[k][j], ribbon_boundary[k][j+1]) for j in range(L)] for k in range(L)]


def control_pts(angle, radius):
    # angle is a  3-list containing angular coordinates of the control points b0, b1, b2
    # radius is the distance from b1 to the  origin O(0,0)
    b_cplx = np.array([np.exp(1j*angle[k]) for k in range(3)])
    b_cplx[1] = radius*b_cplx[1]
    # print(b_cplx.real)
    # print(b_cplx.imag)
    # print(zip(b_cplx.real, b_cplx.imag))
    return zip(b_cplx.real, b_cplx.imag)


def ctrl_rib_chords(l, r, radius):
    # this function returns a 2-list containing control poligons of the two quadratic Bezier
    # curves that are opposite sides in a ribbon
    # l (r) the list of angular variables of the ribbon arc ends defining
    # the ribbon starting (ending) arc
    # radius is a common parameter for both control polygons
    if len(l) != 2 or len(r) != 2:
        raise ValueError('the arc ends must be elements in a list of len 2')
    return [control_pts([l[j], (l[j]+r[j])/2, r[j]], radius) for j in range(2)]


def make_q_bezier(b):  # defines the Plotly SVG path for a quadratic Bezier curve defined by the
    # list of its control points
    # if len(b) != 3:
    #     raise valueError('control poligon must have 3 points')
    A, B, C = b
    return 'M '+str(A[0])+',' + str(A[1])+' '+'Q ' +\
        str(B[0])+', '+str(B[1]) + ' ' +\
        str(C[0])+', '+str(C[1])


def make_ribbon_arc(theta0, theta1):

    if test_2PI(theta0) and test_2PI(theta1):
        if theta0 < theta1:
            theta0 = moduloAB(theta0, -PI, PI)
            theta1 = moduloAB(theta1, -PI, PI)
            if theta0*theta1 > 0:
                raise ValueError('incorrect angle coordinates for ribbon')

        nr = int(40*(theta0-theta1)/PI)
        if nr <= 2:
            nr = 3
        theta = np.linspace(theta0, theta1, nr)
        pts = np.exp(1j*theta)  # points on arc in polar complex form

        string_arc = ''
        for k in range(len(theta)):
            string_arc += 'L '+str(pts.real[k])+', '+str(pts.imag[k])+' '
        return string_arc
    else:
        raise ValueError(
            'the angle coordinates for an arc side of a ribbon must be in [0, 2*pi]')


def make_layout(plot_size, title):
    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    return go.Layout(
        title=dict(
            text=title, font=dict(
                family='Droid',
                size=20)),
        xaxis=dict(axis),
        yaxis=dict(axis),
        legend=dict(
            orientation="h"),
        showlegend=True,
        width=plot_size,
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        height=plot_size+150,
        margin=dict(t=40, b=25, l=25, r=25),
        hovermode='closest'  # to this list one appends below the dicts defining the ribbon,
        # respectively the ideogram shapes
    )


def make_ideo_shape(path, line_color, fill_color):
    # line_color is the color of the shape boundary
    # fill_collor is the color assigned to an ideogram
    return dict(
        line=dict(
            color=line_color,
            width=1
        ),

        path=path,
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def make_ribbon(l, r, line_color, fill_color, radius=0.2):
    # l=[l[0], l[1]], r=[r[0], r[1]]  represent the opposite arcs in the ribbon
    # line_color is the color of the shape boundary
    # fill_color is the fill color for the ribbon shape
    poligon = ctrl_rib_chords(l, r, radius)
    b, c = poligon
    b = list(b)
    c = list(c)
    # print(b,c)

    return dict(
        line=dict(
            color=line_color, width=0.5
        ),
        path=make_q_bezier(b)+make_ribbon_arc(r[0], r[1]) +
        make_q_bezier(c[::-1])+make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def make_self_rel(l, line_color, fill_color, radius):
    # radius is the radius of Bezier control point b_1
    b = control_pts([l[0], (l[0]+l[1])/2, l[1]], radius)
    return dict(
        line=dict(
            color=line_color, width=0.5
        ),
        path=make_q_bezier(b)+make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
        layer='below'
    )


def invPerm(perm):
    # function that returns the inverse of a permutation, perm
    inv = [0] * len(perm)
    for i, s in enumerate(perm):
        inv[s] = i
    return inv


def chord_by_year(year, master, gender, title):
    data = master[master['year'].isin(year)]
    data["genre"] = data["genre"].str.split()
    data2 = data.explode('genre')
    data2['genre'] = data2['genre'].apply(move_particle)
    genre_list = data2.groupby('genre')['title'].count(
    ).sort_values(ascending=False)[:9].index.tolist()
    data2_1 = data2[data2['genre'].isin(genre_list)]
    if gender == 'male':
        data3 = data2_1[data2_1['star_index'] < 15]
    else:
        data3 = data2_1[data2_1['star_index'] >= 15]
    s = pd.crosstab(data3['title'], data3['genre'])
    s = s.T.dot(s).astype(float)
    s.values[np.triu_indices(len(s))] = np.nan
    films_intersection = s.stack()
    number_of_genres = 9
    genre_matrix = np.zeros((number_of_genres, number_of_genres))

    for i, v in films_intersection.iteritems():
        to = genre_list.index(i[0])
        frm = genre_list.index(i[1])
        genre_matrix[to, frm] = v
        genre_matrix[frm, to] = v

    genre_matrix = genre_matrix.astype(int)

    L = check_data(genre_matrix)

    row_sum = [np.sum(genre_matrix[k, :]) for k in range(L)]

    # set the gap between two consecutive ideograms
    gap = 2*PI*0.005
    ideogram_length = 2*PI*np.asarray(row_sum)/sum(row_sum)-gap*np.ones(L)
    # print(ideogram_length)
    ideo_ends = get_ideogram_ends(ideogram_length, gap)
    # print(ideo_ends)
    z = make_ideogram_arc(1.3, [11*PI/6, PI/17])
    # print(z)
    ideo_colors = ['#ffadad',
                   '#ffd6a5',
                   '#fdffb6',
                   '#caffbf',
                   '#9bf6ff',
                   '#a0c4ff',
                   '#bdb2ff',
                   '#ffc6ff',
                   '#fffffc']  # brewe

    mapped_data = map_data(L, genre_matrix, row_sum, ideogram_length)
    idx_sort = np.argsort(mapped_data, axis=1)
    ribbon_ends = make_ribbon_ends(mapped_data, ideo_ends,  idx_sort)
    # print('ribbon ends starting from the ideogram[2]\n', ribbon_ends[2])
    ribbon_color = [L*[ideo_colors[k]] for k in range(L)]
    layout = make_layout(450, title)
    radii_sribb = [0.4, 0.30, 0.35, 0.39, 0.12]
    ribbon_info = []

    for k in range(L):
        sigma = idx_sort[k]
        sigma_inv = invPerm(sigma)
        for j in range(k, L):
            if genre_matrix[k][j] == 0 and genre_matrix[j][k] == 0:
                continue
            eta = idx_sort[j]
            eta_inv = invPerm(eta)
            l = ribbon_ends[k][sigma_inv[j]]

            if j == k:
                # print(make_self_rel(l, 'rgb(175,175,175)',
                #                    ideo_colors[k], radius=radii_sribb[k]))
                layout['shapes'] = layout['shapes'] + (make_self_rel(l, 'rgb(139,137,137)',
                                                                        ideo_colors[k], radius=radii_sribb[k]),)
                z = 0.9*np.exp(1j*(l[0]+l[1])/2)
                # the text below will be displayed when hovering the mouse over the ribbon
                text = genre_list[k]+' has ' + \
                    '{:d}'.format(genre_matrix[k][k]) + \
                    ' number of coocurence with itself ',
                ribbon_info.append(go.Scatter(x=[z.real],
                                              y=[z.imag],
                                              mode='markers',
                                              showlenged=False,
                                              marker=dict(
                    size=0.5, color=ideo_colors[k]),
                    text=text,
                    hoverinfo='text'
                )
                )

            else:
                r = ribbon_ends[j][eta_inv[k]]
            zi = 0.9*np.exp(1j*(l[0]+l[1])/2)
            zf = 0.9*np.exp(1j*(r[0]+r[1])/2)
            # texti and textf are the strings that will be displayed when hovering the mouse
            # over the two ribbon ends
            texti = genre_list[k]+' genre has ' + '{:d}'.format(genre_matrix[k][j])+' occurences with ' +\
                genre_list[j] + ' genre',

            textf = genre_list[j]+' genre has ' + '{:d}'.format(genre_matrix[j][k])+' occurences with ' +\
                genre_list[k] + ' genre',
            ribbon_info.append(go.Scatter(x=[zi.real],
                                          y=[zi.imag],
                                          mode='markers',
                                          showlegend=False,
                                          marker=dict(
                size=0.5, color=ribbon_color[k][j]),
                text=texti,
                hoverinfo='text'
            )
            ),
            ribbon_info.append(go.Scatter(x=[zf.real],
                                          y=[zf.imag],
                                          mode='markers',
                                          showlegend=False,
                                          marker=dict(
                size=0.5, color=ribbon_color[k][j]),
                text=textf,
                hoverinfo='text'
            )
            )
            # IMPORTANT!!!  Reverse these arc ends because otherwise you get
            r = (r[1], r[0])
            # a twisted ribbon
            # print(make_ribbon(
            #     l, r, 'rgb(175,175,175)', ribbon_color[k][j]))
            # append the ribbon shape
            layout['shapes'] = layout['shapes'] + (make_ribbon(
                l, r, 'rgb(139,137,137)', ribbon_color[k][j]),)

    ideograms = []

    for k in range(len(ideo_ends)):
        z = make_ideogram_arc(1.1, ideo_ends[k])
        zi = make_ideogram_arc(1.0, ideo_ends[k])
        m = len(z)
        n = len(zi)
        ideograms.append(go.Scatter(x=z.real,
                                    y=z.imag,
                                    mode='lines',
                                    showlegend=True,
                                    name=genre_list[k],
                                    line=dict(
                                        color=ideo_colors[k], shape='spline', width=1),
                                    text=genre_list[k]+'<br>' +
                                    '{:d}'.format(row_sum[k]),
                                    hoverinfo='text'
                                    )
                         )

        path = 'M '
        for s in range(m):
            path += str(z.real[s])+', '+str(z.imag[s])+' L '
        Zi = np.array(zi.tolist()[::-1])
        for s in range(m):
            path += str(Zi.real[s])+', '+str(Zi.imag[s])+' L '
        path += str(z.real[0])+' ,'+str(z.imag[0])

        layout['shapes'] = layout['shapes'] + ((make_ideo_shape(
            path, 'rgb(139,137,137)', ideo_colors[k])),)

    return(ideograms, ribbon_info, layout)


year = list(range(2010, 2022))
ideograms, ribbon_info, layout = chord_by_year(
    year, master, 'male', 'Male Chord')
data = go.Data(ideograms+ribbon_info)
fig = go.Figure(data=data, layout=layout)

ideograms2, ribbon_info2, layout2 = chord_by_year(
    year, master, 'female', 'Female Chord')
data2 = go.Data(ideograms2+ribbon_info2)
fig2 = go.Figure(data=data2, layout=layout2)


layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                #   html.H2('Number of movies'),
                                  html.H2('Fig1: Genre Chord Diagram'),
                                #   html.P(
                                #       'Visualising time series with Plotly - Dash.'),
                                  html.P(
                                      'We make two chord diagrams to show how actor-dominant and actress-dominant movies would differ in genres across time.  From the visualization result over time, we figured out that years ago actresses   mostly only dominate in romance and drama movies while  action, crime and advatages are dominant by actors. Compared to previous time, the gaps are narrowed down: actress-dominant movies tend to resemple the constitution of actor-dominant ones more and more. Bias towards genres are gradually eliminated.'),
                                  html.Div(style={'margin-top': '20px'}),
                                  html.Div(
                                      children=[
                                          html.Div(className='bottom-nav',
                                                   children=[
                                                       html.A(id='', className='', children=[
                                                           html.Button(
                                                             '<', id='button-prev', n_clicks=0)
                                                       ], href=common.base_url+'/', style={'margin-right': '2rem'}),
                                                       html.A(id='', className='', children=[
                                                           html.Button(
                                                              '>', id='button-next', n_clicks=0),
                                                       ], href=common.base_url+'/vis2'),
                                                   ]
                                                   )
                                      ]),
                                  dcc.Slider(1920, 2010, 10,
                                             value=2010,
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
                                                 2010: '2010'
                                             },
                                             id='my-slider'
                                             )
                              ]
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey chord-diagrams',
                              children=[
                                  dcc.Graph(
                                      id='output_slider',
                                      animate=False,
                                      config={'displayModeBar': False},
                                      figure=fig
                                  ),
                                  dcc.Graph(
                                      id='output_slider_2',
                                      animate=False,
                                      config={'displayModeBar': False},
                                      figure=fig2
                                  )
                              ])
                     # html.Div(id = 'output-check-box')
                 ])
    ]
)


@callback(
    [Output('output_slider', 'figure'),
     Output('output_slider_2', 'figure')],
    [Input('my-slider', 'value')])
def update_output(value):
    if value == 2010:
        year = list(range(2010, 2022))
    elif value == 1940:
        year = list(range(1935, 1946))
    elif value == 1950:
        year = list(range(1955, 1966))
    else:
        year = list(range(value, value+11))

    ideograms, ribbon_info, layout = chord_by_year(
        year, master, 'male', 'Male Chord')
    data = go.Data(ideograms+ribbon_info)
    fig = go.Figure(data=data, layout=layout)

    ideograms2, ribbon_info2, layout2 = chord_by_year(
        year, master, 'female', 'Female Chord')
    data2 = go.Data(ideograms2+ribbon_info2)
    fig2 = go.Figure(data=data2, layout=layout2)

    return fig, fig2
