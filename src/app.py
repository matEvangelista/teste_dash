from dash import Dash, html, dcc, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_iris = pd.read_csv("iris.csv")

media_sl = df_iris['sepal.length'].mean(skipna=True)
media_pw = df_iris['petal.width'].mean(skipna=True)

eixo_x = None
eixo_y = None

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    dbc.Container(children=[
    html.H1(children='Primeiro teste com Dash'),

    html.H1(id='selected-dropdown-value'),

    dbc.Row([
        dbc.Col(html.Div("Teste largura 2"), width=2, className='bg-danger'),
        dbc.Col(html.Div("Teste largura 10"), width=10, className='bg-success')
    ]),

    dbc.Row([
        dbc.Col(html.P(f"Média da coluna sepal.length: {media_sl}"), width=10, className='text-center bg-dark text-white'),
        dbc.Col(html.P(f"Média da coluna petal width: {media_pw}"), width=2, className='text-danger bg-warning')
    ]),

    dbc.Row([
       html.H2("Tabela mtcars", className='text-center')
    ]),

    dbc.Row(dash_table.DataTable(df_iris.to_dict('records'),[{"name": i, "id": i} for i in df_iris.columns], id='tbl_cars'),),

    dbc.Row(html.H2("Mexendo com gráficos"), className='text-center pt-5'),

    dbc.Row([
        dbc.Col(html.P("Escolha o eixo horizontal: ", className='text-bold'), width=3),
        dbc.Col([
            dcc.Dropdown(df_iris.columns[:-1], df_iris.columns[1], id='eixo-x', clearable=False),
            html.Div(id='dd-eixo-x')], width=3),
        dbc.Col(html.P("Escolha o eixo vertical: ", className='text-bold'), width=3),
        dbc.Col([
            dcc.Dropdown(df_iris.columns[:-1], df_iris.columns[1], id='eixo-y', clearable=False),
            html.Div(id='dd-eixo-y')], width=3)
    ], className='pb-5'),
    dbc.Row([
        dbc.Col(html.Div([eixo_x]))
    ], className='pb-5'),

    dcc.Graph(
        id='scatter-plot'
    )


]))

# Callback to update the H1 element based on the selected value in the dropdown
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('eixo-x', 'value'), Input('eixo-y', 'value')]
)
def scatter_plot(selected_x, selected_y):
    fig = px.scatter(df_iris, x=selected_x, y=selected_y, color='variety')
    return fig

if __name__ == '__main__':
    app.run(debug=True)