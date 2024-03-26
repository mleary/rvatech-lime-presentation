import dash
from dash import dash_table
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('./data/predictions.csv')
df['Risk_Assessment'] = df['Predictions'].apply(lambda x: 'Low risk' if x == 'No Accident' else 'High chance of claim')
df = df.drop(['Accident_Reported', 'Predictions', 'Policy_Year'], axis=1)

explanations = pd.read_csv('./data/explanations.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('LIME Insurance - Policy System'),
    html.H3('Hello Matt, please see a list of upcoming renewals and their risk assessment.'),
    html.Hr(style={'borderWidth': "5vh", "width": "100%", "backgroundColor": "#AB87FF","opacity": "unset", "opacity":"1"}),
    dcc.Dropdown(
        id='make-dropdown',
        options=[{'label': i, 'value': i} for i in df['Make'].unique()],
        value=df['Make'].unique()[0]
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': i, 'value': i} for i in df['Policy_Month'].unique()],
        value=df['Policy_Month'].unique()[0]
    ),
    dcc.Dropdown(
        id='risk-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Risk_Assessment'].unique()],
        value='All'
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        tooltip_data=[
            {
                'Risk_Assessment': {'value': str(row['Risk_Assessment']), 'type': 'markdown'}
            } for row in df.to_dict('records')
        ],
           # Overflow into ellipsis
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        tooltip_delay=0,
        tooltip_duration=None
    )
    
], style={'white-space': 'pre-line'})

# Define callback to update table
@app.callback(
    Output('table', 'data'),
    Output('table', 'tooltip_data'),
    [Input('make-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('risk-dropdown', 'value')]
)
def update_table(selected_make, selected_month, selected_risk):
    if selected_risk == 'All':
        filtered_df = df[(df['Make'] == selected_make) & (df['Policy_Month'] == selected_month)]
    else:
        filtered_df = df[(df['Make'] == selected_make) & (df['Policy_Month'] == selected_month) & (df['Risk_Assessment'] == selected_risk)]
    data = filtered_df.to_dict('records')

    # Filter the explanations DataFrame
    filtered_explanations = explanations[explanations['Policy_Id'].isin(filtered_df['Policy_Id'])]
    
    # Group by 'Policy_Id' and get the first three rows of each group
    grouped_explanations = filtered_explanations.groupby('Policy_Id').apply(lambda x: x.head(3)).reset_index(drop=True)
    # Create a dictionary where the keys are the 'Policy_Id' values and the values are the concatenated explanations
    explanation_dict = grouped_explanations.groupby('Policy_Id')['feature'].apply(lambda x: '\n'.join(x)).to_dict()
    
    tooltip_data = [
        {
            #'Risk_Assessment': {'value': explanation_dict.get(d['Policy_Id'], ''), 'type': 'markdown'}
            'Risk_Assessment': {
                'value': "Top Three drivers for prediction:\n" + explanation_dict.get(d['Policy_Id'], ''),
                'type': 'markdown'
            }
        } for d in data
    ]
    return data, tooltip_data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)