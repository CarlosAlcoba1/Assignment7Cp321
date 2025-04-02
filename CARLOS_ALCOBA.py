import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

def create_dataset():
    df = pd.read_html('https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals')[3] # cols-> Year	Winners	Score	Runners-up	Venue	Location	Attendance	Ref.

    for col in ['Winners', 'Runners-up', 'Location']:
        df[col] = df[col].replace({'West Germany': 'Germany', 'Munich, West Germany': 'Munich, Germany'})

    win_counts = df['Winners'].value_counts().reset_index()
    win_counts.columns = ["Country", "Wins"]
    return df, win_counts

df, winners = create_dataset()


app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H3("World Cup Year (No selection to see all winners)"),
            dcc.Dropdown(df['Year'].unique(),
                id='year-dropdown',

            ),
            dcc.Graph(id='map')
        ], style={'width': '100%', 'display': 'inline-block'}),
    ]),

    html.Div(
        style={'width':'250px'},
        children=[
            html.H3("Countries"),
            dcc.Dropdown(winners["Country"], id='country-dropdown')
        ]
    ),
    
    html.Div(
        style={'width': '250px'},
        children=[
            html.H3("Number of World Cup titles"),
            dcc.Textarea(
                id='numWins-display',
                value='',
                readOnly=True,
                style={"margin": "auto", 'textAlign':'center'}
            )
        ]       
    ) 
])

@callback(
    Output('map', 'figure'),
    Input('year-dropdown', 'value')
)

def update_map(selected_year):
    if selected_year is None:
        fig = px.choropleth(
            winners,
            locations = "Country",
            locationmode='country names',
            color="Wins",
            hover_name="Country",
            hover_data=["Wins"],
            title="All World Cup Winners",
            projection="natural earth"


        )
    else:
        
        data = df[df['Year'] == selected_year].iloc[0]
        data = pd.DataFrame({
            'Country': [data['Winners'], data['Runners-up']],
            'Result': ['Winner', 'Runner-up'],
            'Color': ['Winner', 'Runner-up']
        })
        fig = px.choropleth(
                data,
                locations = 'Country',
                locationmode='country names',
                color='Color',
                hover_name="Country",
                hover_data=["Result"],
                title=f"{selected_year} FIFA World Cup Finals",
                projection="natural earth"
    
    
            )
    return fig

@callback(
    Output('numWins-display', 'value'),
    Input('country-dropdown', 'value')  
)

def update_win(selected_country):
    if selected_country is None:
        return ""
    
    return str(winners.loc[winners['Country'] == selected_country, 'Wins'].values[0])


if __name__ == '__main__':
    app.run(debug=True, port=8054)
