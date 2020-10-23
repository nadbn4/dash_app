import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### read in data
win_loss_df = pd.read_pickle("win_loss_df.pkl").sort_values(['wins', 'points_for'], ascending = False)

myheading = 'Raytonia Beach Fantasy Football League'
tabtitle='Raytown!'

########### Set up the chart
win_bars = go.Bar(x=win_loss_df['owner_team_name'], y=win_loss_df['wins'],
                  base=0,
                  marker_color='green',
                  name='Wins',
                  hoverinfo='y'
)

loss_bars = go.Bar(x=win_loss_df['owner_team_name'], y=win_loss_df['losses'],
                   base= -1 * win_loss_df['losses'].astype('int'),
                   text = 1 * win_loss_df['losses'].astype('int'),
                   marker_color='red',
                   name='Losses',
                   hoverinfo='text'
)

win_loss_data = [win_bars, loss_bars]

#fig.update_yaxes(tickvals=[5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5], ticktext = [5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5])

#win_loss_layout = go.Layout(barmode = 'overlay',
#                            hovermode = 'x',
#                            title = 'Wins/Losses',
#                            yaxis = {'tickvals' : [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5],
#                                     'ticktext' : [5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5]
#                                    }
#)

win_loss_layout = go.Layout(barmode = 'overlay',
                            hovermode = 'x',
                            title = 'Wins/Losses'
)

win_loss_fig = go.Figure(data=win_loss_data, layout=win_loss_layout)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='win_loss_fig',
        figure=win_loss_fig
    )
    ]
)

if __name__ == '__main__':
    app.run_server()