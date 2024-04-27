import pandas as pd
import plotly.express as px
from dash import dash, html

from dash.dependencies import Input,Output

app = dash.Dash(__name__)

# import data and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

grp_col = ['State','ANSI','Affected by','Year','state_code']

df = df.groupby(grp_col)[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])
print(df)

