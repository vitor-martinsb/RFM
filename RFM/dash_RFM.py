import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates

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

# Normalizar o monetário de 0 a 1
df['Monetário_Normalizado'] = (df['Monetário'] - df['Monetário'].min()) / (df['Monetário'].max() - df['Monetário'].min())
df['Recência_Normalizada'] = (df['Recência'] - df['Recência'].min()) / (df['Recência'].max() - df['Recência'].min())
df['Frequência_Normalizada'] = (df['Frequência'] - df['Frequência'].min()) / (df['Frequência'].max() - df['Frequência'].min())

# Calcular a contagem de clientes para cada combinação de classe e score
heatmap_data = df.groupby(['Classe', 'Score']).size().reset_index(name='Quantidade')

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div(
    children=[
        html.Div(
            className='header',
            children=[
                html.H2('Análise RFM', style={'text-align': 'left', 'font-family': 'Poppins'}),
            ],
            style={'background-color': 'white', 'padding': '10px'}
        ),
        html.Div(
            className='grid-container',
            style={'margin': '0'},
            children=[
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Heatmap de Concentração de Clientes', style={'text-align': 'center', 'font-family': 'Roboto'}),
                        dcc.Graph(
                            id='heatmap',
                            figure=go.Figure(
                                data=go.Heatmap(
                                    x=heatmap_data['Score'],
                                    y=heatmap_data['Classe'],
                                    z=heatmap_data['Quantidade'],
                                    colorscale='plasma',
                                    text=heatmap_data['Quantidade'],
                                    hovertemplate='Classe: %{y}<br>Score: %{x}<br>Quantidade: %{z}<extra></extra>',
                                    showscale=True
                                ),
                                layout=go.Layout(
                                    xaxis=dict(title='Score'),
                                    yaxis=dict(title='Classe')
                                )
                            )
                        )
                    ]
                ),
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Boxplot', style={'text-align': 'center', 'font-family': 'Roboto'}),
                        dcc.Dropdown(
                            id='boxplot-dropdown',
                            options=[
                                {'label': 'Recência', 'value': 'Recência'},
                                {'label': 'Frequência', 'value': 'Frequência'},
                                {'label': 'Monetário', 'value': 'Monetário'}
                            ],
                            value='Recência',
                            clearable=False
                        ),
                        dcc.Graph(
                            id='boxplot',
                            figure=px.box(df, x='Classe', y='Recência')
                        )
                    ]
                ),
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Distribuição de Clientes por Classe', style={'text-align': 'center', 'font-family': 'Roboto'}),
                        dcc.Graph(
                            id='barplot',
                            figure=px.histogram(df, x='Classe', color='Classe')
                        )
                    ]
                ),
                html.Div(
                    className='grid-item',
                    children=[
                        html.H2('Gráfico 3D - RFM', style={'text-align': 'center', 'font-family': 'Roboto'}),
                        dcc.Graph(
                            id='grafico-3d',
                            figure=make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter3d'}]]),
                        )
                    ]
                ),
            ]
        )
    ],
    style={'background-color': 'white', 'color': 'black', 'padding': '10px', 'margin': '0'}
)


# Atualização do Gráfico 3D
@app.callback(
    dash.dependencies.Output('grafico-3d', 'figure'),
    [dash.dependencies.Input('boxplot-dropdown', 'value')]
)
def update_3d_graph(selected_feature):
    return go.Figure(
        data=[
            go.Scatter3d(
                x=df['Recência_Normalizada'],
                y=df['Frequência_Normalizada'],
                z=df['Monetário_Normalizado'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df['Classe'].map({'Classe 1': 'red', 'Classe 2': 'green', 'Classe 3': 'blue'}),
                    opacity=0.8,
                    colorbar=dict(title='Classe', ticktext=['Classe 1', 'Classe 2', 'Classe 3'])
                )
            )
        ],
        layout=go.Layout(
            scene=dict(
                xaxis=dict(title='Recência'),
                yaxis=dict(title='Frequência'),
                zaxis=dict(title='Monetário'),
                bgcolor='white',
                camera=dict(
                    eye=dict(x=1.7, y=1.7, z=1.5)
                )
            )
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)
