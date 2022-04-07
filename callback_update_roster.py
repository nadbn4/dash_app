from dash.dependencies import Input, Output
import plotly.graph_objs as go


def get_callback_update_roster(app, df):

	@app.callback(Output('roster_table', 'data'),
				 [Input('week', 'value'),
				  Input('owner_team', 'value')
				 ])

	def update_table(week, team):
		updated_df = df.loc[(df['week'] == week) & (df['owner_team'] == team)].sort_values('slot_id')
		
		return updated_df.to_dict(orient='records')