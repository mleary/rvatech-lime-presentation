import dash
from dash import dash_table
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the data
df = pd.read_csv('./data/predictions.csv')
df['Risk Assessment'] = df['Predictions'].apply(lambda x: 'Low risk' if x == 'No Accident' else 'High chance of claim')
df = df.drop(['Accident_Reported', 'Predictions', 'Policy_Year'], axis=1)


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
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Risk Assessment'].unique()],
        value='All'
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
    )
])

# Define callback to update table
@app.callback(
    Output('table', 'data'),
    [Input('make-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('risk-dropdown', 'value')]
)
def update_table(selected_make, selected_month, selected_risk):
    if selected_risk == 'All':
        filtered_df = df[(df['Make'] == selected_make) & (df['Policy_Month'] == selected_month)]
    else:
        filtered_df = df[(df['Make'] == selected_make) & (df['Policy_Month'] == selected_month) & (df['Risk Assessment'] == selected_risk)]
    return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)