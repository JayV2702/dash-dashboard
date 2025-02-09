import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Load cleaned data
file_path = "/mnt/data/Lithum ion.xlsx"
xls = pd.ExcelFile(file_path)
value_df = pd.read_excel(xls, sheet_name="Value")
quantity_df = pd.read_excel(xls, sheet_name="Quantity")

# Data cleaning
value_df.replace({" ": None}, inplace=True)
quantity_df.replace({" ": None}, inplace=True)
value_df.iloc[:, 1:] = value_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
quantity_df.iloc[:, 1:] = quantity_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Dashboard setup
app = Dash(__name__)

def get_top_10(year):
    df = value_df[['Country', year]].dropna().sort_values(by=year, ascending=False).head(10)
    total_import = df[year].sum()
    df['Percentage Share'] = (df[year] / total_import) * 100
    return df, total_import

app.layout = html.Div([
    html.H1("EV Battery Imports in India"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2014, 2025)],
        value=2023
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])

@app.callback(
    [dcc.Output('bar-chart', 'figure'), dcc.Output('pie-chart', 'figure')],
    [dcc.Input('year-dropdown', 'value')]
)
def update_charts(year):
    top_10_df, total_import = get_top_10(year)
    
    bar_chart = px.bar(top_10_df, x='Country', y=year, title=f"Top 10 Importing Countries - {year}")
    pie_chart = px.pie(top_10_df, names='Country', values='Percentage Share', title=f"Percentage Share - {year}")
    
    return bar_chart, pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)
