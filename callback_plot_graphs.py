from dash.dependencies import Input, Output
import plotly.graph_objs as go


def get_callback_plots(app, df):

	@app.callback(Output('win_loss_fig', 'figure'),
				 [Input('graph_option', 'value')
				 ])

	def update_graph(column_options):
		if column_options == 'wins/losses':
			win_bars = go.Bar(x=df['owner_team_name'], y=df['wins'],
							  base=0,
							  marker_color='green',
							  name='Wins',
							  hoverinfo='y'
							 )

			loss_bars = go.Bar(x=df['owner_team_name'], y=df['losses'],
							   base= -1 * df['losses'].astype('int'),
							   text = 1 * df['losses'].astype('int'),
							   marker_color='red',
							   name='Losses',
							   hoverinfo='text'
							  )

			win_loss_data = [win_bars, loss_bars]

			win_loss_layout = go.Layout(barmode = 'overlay',
										hovermode = 'x',
										title = 'Wins/Losses',
										yaxis_range=[-5,5],
										yaxis = dict(tickvals = [5, 3, 0, -3, -5],
													 ticktext = [5, 3, 0, 3, 5],
													tickmode = 'array'
													)
									   )


			win_loss_fig = go.Figure(data=win_loss_data, layout=win_loss_layout)
		else:
			win_bars = go.Bar(x=df['owner_team_name'], y=df['points_for'],
							  base=0,
							  marker_color='green',
							  name='points_for',
							  hoverinfo='y'
							 )

			loss_bars = go.Bar(x=df['owner_team_name'], y=df['points_against'],
							   base= -1 * df['points_against'].astype('int'),
							   text = 1 * df['points_against'].astype('int'),
							   marker_color='red',
							   name='points_against',
							   hoverinfo='text'
							  )

			win_loss_data = [win_bars, loss_bars]

			win_loss_layout = go.Layout(barmode = 'overlay',
										hovermode = 'x',
										title = 'points_for/points_against',
										yaxis = dict(tickvals=[3000, 2000, 1000, 0, -1000, -2000, -3000], 
													 ticktext = [3000, 2000, 1000, 0, 1000, 2000, 3000]
													)
									   )


			win_loss_fig = go.Figure(data=win_loss_data, layout=win_loss_layout)
			
		return win_loss_fig