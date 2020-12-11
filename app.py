### code version to run from Haroku ###

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
tm_game_data = pd.read_csv("tm_game_data.csv")

########### define functions
# create agg_week function to sum all stats within the user defined time frame
def agg_week(weekly_boxscore, num_weeks):
    num_weeks = weekly_boxscore["week"].max() - num_weeks + 1
    weekly_boxscore = weekly_boxscore[(weekly_boxscore["week"] <= weekly_boxscore["week"].max()) & \
                                      (weekly_boxscore["week"] >= num_weeks)]
    gp_df = weekly_boxscore['team_abv'].value_counts().sort_index().reset_index()    
    weekly_boxscore = weekly_boxscore.groupby(['team_abv']).sum().sort_values(['team_abv']).reset_index()
    weekly_boxscore['gp'] = gp_df['team_abv']
    return weekly_boxscore

# create function to grab team or boxscore stat from prior_weeks dataframe
def get_values_list(prior_weeks, team, column):   
    data_list = []
    for i in team.tolist():
        team_idx = prior_weeks.index[prior_weeks['team_abv'] == i].tolist()[0]
        data_value = prior_weeks.at[team_idx, column]
        data_list.append(data_value)
    return np.array(data_list)

graph_options = ['wins/losses', 'points for/points against']
subset_options = ['QB', 'RB', 'WRTE', 'DEF', 'KICK']

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
app.layout = html.Div([
    html.H1(myheading),
    dcc.Tabs([
        dcc.Tab(label = 'League Overview', children = [
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
                ], className="six columns"),

                html.Div([
                    html.H3(),
                    dcc.Graph(id='weekly_points', figure=weekly_points_fig)
                ], className="six columns"),
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
                                     columns=[{"name": i, "id": i} for i in rosters_df.columns]
        )
    )
]),
        dcc.Tab(label = 'Weekly NFL Matchup Rankings', children = [
            html.Div([
                html.Div([
                    html.H3(),
                    dcc.Input(id="input_range", 
                              type="number", 
                              placeholder="num weeks", 
                              min=1, 
                              max=tm_game_data['week'].max(), 
                              step=1,
                    )
                ], className="six columns", style = {'width': '5%'}),
                html.Div([
                    html.H3(),
                    dcc.Dropdown(id = 'subset_option', 
                                 options = [{'label' : i, 'value' : i} for i in subset_options],
                                 value = 'QB'
                    )
                ], className="six columns", style = {'width': '10%'})
            ], className="row")
        ]),
        dcc.Tab(label = 'Weekly Raytonia Beach Rosters & Predictions')
])
])

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