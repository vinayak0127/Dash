import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash, html, dcc

from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# import data and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

grp_col = ['State', 'ANSI', 'Affected by', 'Year', 'state_code']

df = df.groupby(grp_col)[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])
# print(df)


# App layout

app.layout = html.Div([
    html.H1("Web Dashboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year", options=[
        {"label": "2015", "value": 2015},
        {"label": "2016", "value": 2016},
        {"label": "2017", "value": 2017},
        {"label": "2018", "value": 2018}
    ], multi=False, value=2015, style={'width': "40%"}),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id="my_bee_map", figure={})
])


# Connect plotly graph with dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd]
    dff = dff[dff['Affected by'] == "Varroa_mites"]

    #plotly express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # plotly graph objects
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode=dff['USA-states'],
    #         locations=dff['state_code'],
    #         z=dff['Pct of Colonies Impacted'].astype(float),
    #         colorscale='Reds'
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text='Bees Affected by mites in the USA',
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa')
    # )

    return container, fig


if __name__ == '__main__':
    app.run(debug=True)
