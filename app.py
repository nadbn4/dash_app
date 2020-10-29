### code version to run locally ###

import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

########### read in data
win_loss_df = pd.read_pickle("win_loss_df.pkl").sort_values(['wins', 'points_for'], ascending = False)
matchups_df = pd.read_csv("matchups_df.csv")
rosters_df = pd.read_csv("rosters_df.csv")
rosters_df = rosters_df[rosters_df.columns[rosters_df.columns!='Unnamed: 0']]

graph_options = ['wins/losses', 'points for/points against']

myheading = 'Raytonia Beach Fantasy Football League'
tabtitle='Raytown!'

weekly_points_fig = px.line(matchups_df, x="week", y="score", color = 'owner_team_name', title = 'Scores per Week',
                            hover_name='owner_team_name', hover_data={"week" : False,
                                                                      'owner_team_name' : False,
                                                                      'score' : True
                                                                     }
                           )

#weekly_points_fig = px.line(matchups_df, x="week", y="score", color = 'owner_team_name', title = 'Scores per Week')

weekly_points_fig.update_xaxes(range=[0.95, 7.05], dtick=1)
weekly_points_fig.layout.update(showlegend=False)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout
app.layout = html.Div(children = [
    html.H1(myheading),
    html.Div(
        dcc.Dropdown(id = 'graph_option', 
                     options = [{'label' : i, 'value' : i} for i in graph_options],
                     value = 'wins/losses'
        ),
        style = {'width': '15%'}
    ),
    html.Div([
        html.Div([
            html.H3(),
            dcc.Graph(id='win_loss_fig')
        ], className="six columns", style = {'width': '48%'}),

        html.Div([
            html.H3(),
            dcc.Graph(id='weekly_points', figure=weekly_points_fig)
        ], className="six columns", style = {'width': '48%'}),
    ], className="row"),
    html.Div([
        html.Div([
            html.H3(),
            dcc.Dropdown(id='week', 
                         options = [{'label' : i, 'value' : i} for i in rosters_df['week'].unique()],
                         value = 1
                        )
        ], className="six columns", style = {'width': '5%'}),
        html.Div([
            html.H3(),
            dcc.Dropdown(id='owner_team', 
                         options = [{'label' : i, 'value' : i} for i in rosters_df['owner_team'].unique()],
                         value = 'Happy Rock Homewreckers'
                        )
        ], className="six columns", style = {'width': '25%'}),
    ], className="row"),    
    html.Div(
        dash_table.DataTable(id = 'roster_table',
                             columns=[{"name": i, 
                                       "id": i} for i in rosters_df.columns]
        )
    )
]
)

@app.callback(
    Output('win_loss_fig', 'figure'),
    [Input('graph_option', 'value')
    ])

def update_graph(column_options):
    if column_options == 'wins/losses':
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

        win_loss_layout = go.Layout(barmode = 'overlay',
                                    hovermode = 'x',
                                    title = 'Wins/Losses',
                                    yaxis = dict(tickvals = [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5],
                                                 ticktext = [5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5]
                                                )
                                   )


        win_loss_fig = go.Figure(data=win_loss_data, layout=win_loss_layout)
    else:
        win_bars = go.Bar(x=win_loss_df['owner_team_name'], y=win_loss_df['points_for'],
                          base=0,
                          marker_color='green',
                          name='points_for',
                          hoverinfo='y'
                         )

        loss_bars = go.Bar(x=win_loss_df['owner_team_name'], y=win_loss_df['points_against'],
                           base= -1 * win_loss_df['points_against'].astype('int'),
                           text = 1 * win_loss_df['points_against'].astype('int'),
                           marker_color='red',
                           name='points_against',
                           hoverinfo='text'
                          )

        win_loss_data = [win_bars, loss_bars]

        win_loss_layout = go.Layout(barmode = 'overlay',
                                    hovermode = 'x',
                                    title = 'points_for/points_against',
                                    yaxis = dict(tickvals=[1200, 800, 400, 0, -400, -800, -1200], 
                                                 ticktext = [1200, 800, 400, 0, 400, 800, 1200]
                                                )
                                   )


        win_loss_fig = go.Figure(data=win_loss_data, layout=win_loss_layout)
        
    return win_loss_fig

@app.callback(
    Output('roster_table', 'data'),
    [Input('week', 'value'),
     Input('owner_team', 'value')
    ])

def update_table(week, team):
    updated_df = rosters_df.loc[(rosters_df['week'] == week) & (rosters_df['owner_team'] == team)].sort_values('slot_id')
    return updated_df.to_dict(orient='records')

if __name__ == '__main__':
    app.run_server()