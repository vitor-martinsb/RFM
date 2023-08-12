import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import dash_bootstrap_components as dbc
import dash_table

pio.templates.default = "plotly_dark"  # Set the default template to dark mode

# Dados de exemplo
np.random.seed(0)
clientes = ['Cliente {}'.format(i) for i in range(1, 101)]

recencia = np.random.randint(1, 365, size=100)
frequencia = np.random.randint(1, 50, size=100)
monetario = np.random.randint(100, 1000, size=100)
score = np.random.randint(1, 11, size=100)
classe = ['Classe {}'.format(i) for i in np.random.randint(1, 4, size=100)]

df = pd.DataFrame({
    'Cliente': clientes,
    'Recência': recencia,
    'Frequência': frequencia,
    'Monetário': monetario,
    'Score': score,
    'Classe': classe
})

# Calcular a contagem de clientes para cada combinação de classe e score
heatmap_data = df.groupby(['Classe', 'Score']).size().reset_index(name='Quantidade')

# Obter todas as classes únicas
classes = df['Classe'].unique()

# Inicialização do aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do dashboard
app.layout = html.Div(
    children=[
        html.Div(
            className='grid-container',
            style={'margin': '0'},
            children=[
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Heatmap de Concentração de Clientes',
                                style={'text-align': 'center', 'font-family': 'Poppins', 'color': 'white'}),
                        dcc.Graph(
                            id='heatmap',
                            figure=px.imshow(heatmap_data.pivot('Classe', 'Score', 'Quantidade'), color_continuous_scale='plasma')
                        )
                    ]
                ),
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Distribuição do RFM',
                                style={'text-align': 'center', 'font-family': 'Poppins', 'color': 'white'}),
                        dcc.Dropdown(
                            id='boxplot-dropdown',
                            options=[
                                {'label': 'Recência', 'value': 'Recência'},
                                {'label': 'Frequência', 'value': 'Frequência'},
                                {'label': 'Monetário', 'value': 'Monetário'}
                            ],
                            value='Recência',
                            clearable=False,
                            style={'color': '#222222'}
                        ),
                        dcc.Graph(
                            id='boxplot',
                            style={'color': 'gray'}
                        )
                    ]
                ),
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Distribuição de Clientes por Classe',
                                style={'text-align': 'center', 'font-family': 'Poppins', 'color': 'white'}),
                        dcc.Graph(
                            id='barplot',
                            style={'color': 'gray'}
                        )
                    ]
                ),
            ]
        ),
        html.Div(
            className='table-container',
            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-top': '20px'},  # Center the table horizontally and vertically
            children=[
                html.H2('Dados do DataFrame', style={'text-align': 'center', 'font-family': 'Poppins', 'color': 'white'}),
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in df.columns if '_Normalizado' not in col],  # Remove normalized columns
                    data=df.to_dict('records'),
                    page_size=30,  # Define o tamanho da página para 10 linhas
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    export_format="csv",  # Habilita a exportação para CSV
                    export_headers="display",
                    style_table={'overflowX': 'auto', 'width': '100%'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'text-align': 'center'},  # Centraliza o texto do cabeçalho
                    style_cell={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white',
                        'maxWidth': '180px',
                        'whiteSpace': 'normal',
                        'textAlign': 'center',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    style_filter_conditional=[
                        {'filter_query': '{col} eq ""', 'color': 'white'}                        
                        for col in df.columns if '_Normalizado' not in col
                    ]
                )
            ]
        )
    ],
    style={'background-color': '#111111', 'color': 'gray', 'padding': '10px', 'margin': '0', 'display': 'grid', 'grid-gap': '0px'}
)

# Atualização do Dropdown de Boxplot
@app.callback(
    dash.dependencies.Output('boxplot', 'figure'),
    [dash.dependencies.Input('boxplot-dropdown', 'value')]
)
def update_boxplot(selected_feature):
    return px.box(df, x='Classe', y=selected_feature)

# Atualização do Histograma
@app.callback(
    dash.dependencies.Output('barplot', 'figure'),
    [dash.dependencies.Input('boxplot-dropdown', 'value')]
)
def update_barplot(selected_feature):
    return px.histogram(df, x='Classe', y=selected_feature, color='Classe')


if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
