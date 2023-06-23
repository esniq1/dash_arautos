# ===== Importacao Bibliotecas
import dash
import dash_bootstrap_components as dbc 
from dash import html,dcc,Input,Output 
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.ZEPHYR,'https://drive.google.com/uc?export=view&id=1CXmY2pOAu2eyT6Y4F2xdxBpvaySBYcAA'],title='Dashboard Arautos')
server = app.server
#== Tratando Dados
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1hBvHV4aO1954BP50AIVEJDBj0ozXZvD1WX5vZmPktGo/gviz/tq?tqx=out:csv&sheet=cnsabr23_2',low_memory=False)

base_cns = 'https://docs.google.com/spreadsheets/d/1QWCYV0ZJ2YQD1G6O4be-2XWHNEJ7-eaR/gviz/tq?tqx=out:csv&sheet='
base_csv = 'https://docs.google.com/spreadsheets/d/1I-Hm7PMm48pCT4exw-3EoXpcCPcBTTrU/gviz/tq?tqx=out:csv&sheet='
base_col = 'https://docs.google.com/spreadsheets/d/11yJHJQc8hHljq0vrQDgcE1j9p0H-r5vt/gviz/tq?tqx=out:csv&sheet='
#Separando Data
df['data'] = df.apply(lambda x: x['data'].split(' ')[0],axis=1)
df['data'] = pd.to_datetime(df['data'],format='%Y-%m-%d')

# Contando Valores por dia e agrupando
df = df.sort_values('data').reset_index(drop=True)
#df['camp'] = df.apply(lambda x: x['camp'].upper(),axis=1)
df_a = df.groupby('data').count()

#DataFrame FB
df_fb = pd.concat([pd.read_csv(base_cns+'geral_fb'),pd.read_csv(base_csv+'geral_fb'),pd.read_csv(base_col+'geral_fb')],ignore_index=True)
df_fb['Data'] = pd.to_datetime(df_fb['Data'],format='%Y-%m-%d')
df_fb['Valor Gasto'] = df_fb.apply(lambda x:float(x['Valor Gasto'].replace('.','').replace(',','.')),axis=1)
df_fb['Leads'] = df_fb.apply(lambda x: float(x['Leads'].replace(',','.')) if type(x['Leads']) == type('') else x['Leads'],axis=1)
df_fb = df_fb[df_fb['Data'].between(df['data'].min(),df['data'].max())].reset_index(drop=True)
df_fb_dash = df_fb.groupby('Data').sum(numeric_only=True).sort_index()
df_fb_dash['CPA'] = df_fb_dash['Valor Gasto'] / df_fb_dash['Leads']

#DataFrame Google
df_yt = pd.concat([pd.read_csv(base_cns+'geral_yt'),pd.read_csv(base_csv+'geral_yt'),pd.read_csv(base_col+'geral_yt')],ignore_index=True)
df_yt['Data'] = pd.to_datetime(df_yt['Data'],format='%Y-%m-%d')
df_yt['Valor Gasto'] = df_yt.apply(lambda x:float(x['Valor Gasto'].replace('.','').replace(',','.')),axis=1)
df_yt['Leads'] = df_yt.apply(lambda x: float(x['Leads'].replace(',','.')) if type(x['Leads']) == type('') else x['Leads'],axis=1)
df_yt = df_yt[df_yt['Data'].between(df['data'].min(),df['data'].max())].reset_index(drop=True)
df_yt_dash = df_yt.groupby('Data').sum(numeric_only=True).sort_index()
df_yt_dash['CPA'] = df_yt_dash['Valor Gasto'] / df_yt_dash['Leads']

#== Funcoes Adicionais

def formatar_numero(numero):
    numero_formatado = "{:,.2f}".format(numero).replace(",", "temp").replace(".", ",").replace("temp", ".")

    return numero_formatado

def formatar_inteiro(numero):
    numero_formatado = "{:,.0f}".format(numero).replace(",", "temp").replace(".", ",").replace("temp", ".")

    return numero_formatado

def card_fb(title,contem):
    contem = f'\| {contem} \|'
    card = html.Div([
        # Cabecalho #
        html.Div([
            html.P(title,style={'margin-left':'5px'})
        ],style={'border-left':'10px solid #3b5998'},className='cabecalho_card'),
        html.Div([
            html.Div([
                html.P('CPA Max'),
                html.P('-')
            ],className='card_info'),
            html.Div([
                html.P('CPA'),
                html.P(f'R$ {formatar_numero(df_fb[df_fb["Nome Campanha"].str.contains(contem)]["Valor Gasto"].sum()/ df_fb[df_fb["Nome Campanha"].str.contains(contem)]["Leads"].sum())}')
            ],className='card_info')
        ],style={'display':'flex'}),
        html.Div([
            html.Div([
                html.P('Leads'),
                html.P(f'{formatar_inteiro(df_fb[df_fb["Nome Campanha"].str.contains(contem)]["Leads"].sum())}')
            ],className='card_info'),
            html.Div([
                html.P('Valor Gasto'),
                html.P(f'R$ {formatar_numero(df_fb[df_fb["Nome Campanha"].str.contains(contem)]["Valor Gasto"].sum())}')
            ],className='card_info')
        ],style={'display':'flex'})
    ],className='cabecalho_card',style={'flex':'1','margin':'10px'})

    return card

def card_yt(title,contem):
    contem = f'{contem}'
    card = html.Div([
        # Cabecalho #
        html.Div([
            html.P(title,style={'margin-left':'5px'})
        ],style={'border-left':'10px solid red'},className='cabecalho_card'),
        html.Div([
            html.Div([
                html.P('CPA Max'),
                html.P('-')
            ],className='card_info'),
            html.Div([
                html.P('CPA'),
                html.P(f'R$ {formatar_numero(df_yt[df_yt["Nome Campanha"].str.contains(contem)]["Valor Gasto"].sum()/ df_yt[df_yt["Nome Campanha"].str.contains(contem)]["Leads"].sum())}')
            ],className='card_info')
        ],style={'display':'flex'}),
        html.Div([
            html.Div([
                html.P('Leads'),
                html.P(f'{formatar_inteiro(df_yt[df_yt["Nome Campanha"].str.contains(contem)]["Leads"].sum())}')
            ],className='card_info'),
            html.Div([
                html.P('Valor Gasto'),
                html.P(f'R$ {formatar_numero(df_yt[df_yt["Nome Campanha"].str.contains(contem)]["Valor Gasto"].sum())}')
            ],className='card_info')
        ],style={'display':'flex'})
    ],className='cabecalho_card',style={'flex':'1','margin':'10px'})

    return card
#=== Sidebar
sidebar = dbc.Col([
    #html.Div([html.Img(src='https://docs.google.com/uc?id=1b1yD3pethxeXQ1d186lfyBUeUr8Zvh6M',style={'width':'100%'})]),
    html.Div([html.Img(src='https://s3.amazonaws.com/ahe.images/1/Assinatura-Oficial_AEB_Sem-efeitos.png',style={'width':'100%'})]),
    html.Hr(),
    #---- Nav -----#
    dbc.Nav([
        dbc.NavLink('Overview',href='/overview',active='exact'),
        dbc.NavLink('FB - Central',href='/fbcentral',active='exact'),
        dbc.NavLink('FB - Global',href='/fbglobal',active='exact'),
        dbc.NavLink('YT - Central',href='/ytcentral',active='exact'),
        dbc.NavLink('YT - Global',href='/ytglobal',active='exact'),
        dbc.NavLink('Testes',href='/testes',active='exact'),
        #dbc.NavLink('Remarketing',href='/remarketing',active='exact'),
    ],vertical=True,pills=True,id='nav-bar')
])

#== Home Page / Overview
overview_card_geral = html.Div([
    html.Div([
        html.P('Geral',style={'padding':'5px'})
    ],style={'background-color':'#2c2c2c','color':'white','border-radius':'5px'}),
    html.Div([
        html.Div([
            html.P('Valor Gasto'),
            html.P(f'R$ {formatar_numero(df_fb["Valor Gasto"].sum() + df_yt["Valor Gasto"].sum())}')
        ],className='card'),
        html.Div([
            html.P('Leads'),
            html.P(f'{formatar_inteiro(df_fb["Leads"].sum() + df_yt["Leads"].sum())}')
        ],className='card')
    ]),    
],className='card',style={'border':'1px solid'})

overview_card_fb = html.Div([
    html.Div([
        html.P('Facebook Ads',style={'padding':'5px'})
    ],style={'background-color':'#4e71ba','color':'white','border-radius':'5px'}),
    html.Div([
        html.Div([
            html.P('Leads'),
            html.P(f'{formatar_inteiro(df_fb["Leads"].sum())}')
        ],className='card'),
        html.Div([
            html.P('CPA'),
            html.P(f'R$ {formatar_numero(df_fb["Valor Gasto"].sum() / df_fb["Leads"].sum())}')
        ],className='card'),
        html.Div([
            html.P('CPA Max.'),
            html.P('-')
        ],className='card'),
        html.Div([
            html.P('Valor Gasto'),
            html.P(f'R$ {formatar_numero(df_fb["Valor Gasto"].sum())}')
        ],className='card')
    ]),    
],className='card',style={'border':'1px solid','margin-left':'10px','margin-right':'10px'})

overview_card_yt = html.Div([
    html.Div([
        html.P('Google Ads',style={'padding':'5px'})
    ],style={'background-color':'red','color':'white','border-radius':'5px'}),
    html.Div([
        html.Div([
            html.P('Leads'),
            html.P(f'{formatar_inteiro(df_yt["Leads"].sum())}')
        ],className='card'),
        html.Div([
            html.P('CPA'),
            html.P(f'R$ {formatar_numero(df_yt["Valor Gasto"].sum() / df_yt["Leads"].sum())}')
        ],className='card'),
        html.Div([
            html.P('CPA Max.'),
            html.P('-')
        ],className='card'),
        html.Div([
            html.P('Valor Gasto'),
            html.P(f'R$ {formatar_numero(df_yt["Valor Gasto"].sum())}')
        ],className='card')
    ]),    
],className='card',style={'border':'1px solid','margin-left':'10px'})
#=== Grafico Overview
grafico_leads = dcc.Graph(
    id="leads-banco",
    figure={
        "data": [
            go.Bar(x=df_a.index,y=df_a['id'].to_list(),name='Base'),
            go.Bar(x=df_fb_dash.index,y=df_fb_dash['Leads'].to_list(),name='Facebook'),
            go.Bar(x=df_yt_dash.index,y=df_yt_dash['Leads'].to_list(),name='Google')
        ],
        "layout": go.Layout(
            xaxis={"title": "Data"},
            yaxis={"title": "Numero de Leads"},
            title={'text':'Leads por dia','font':{'size':25}}
        ),
    },
)
grafico_gastos = dcc.Graph(
    id="leads-banco",
    figure={
        "data": [
            #go.Line(x=df_a.index,y=df_a['id'].to_list(),name='Base'),
            go.Line(x=df_fb_dash.index,y=df_fb_dash['CPA'].to_list(),name='Facebook'),
            go.Line(x=df_yt_dash.index,y=df_yt_dash['CPA'].to_list(),name='Google')
        ],
        "layout": go.Layout(
            xaxis={"title": "Data"},
            yaxis={"title": "Valor"},
            title={'text':'CPA','font':{'size':25}}
        ),
    },
)
overview = html.Div([
    # -- Cabecalho -- #
    html.Div([
        overview_card_geral,overview_card_fb,overview_card_yt      
    ],style={'background-color':'#c0c0c0','border-radius':'10px','height':'50%','margin':'0'}),
    grafico_leads,
    grafico_gastos    
],style={'background-color':'white'})

#== Pagina FB - Global
cabecalho_fb_global = html.Div([
    html.Div([
        html.Img(src='https://docs.google.com/uc?id=1ywTia_4RoRM4qd6eBE8d0HgPTfoRarZP',className='fb_logo')
    ],style={'display':'inline-block','height':'100%'}),
    html.Div([
        html.H3('Relatório dos Grupos do Exterior',style={'text-align':'left','margin-top':'10px'}),
        html.P('CSV | Consagración a la Santísima Virgen',style={'text-align':'left','padding':'0'})
    ],style={'display':'inline-block'})
    
],style={'height':'80px'})

fb_global = html.Div([
    # Cabecalho
    cabecalho_fb_global,
    html.Hr(),
    html.Div([
        card_fb('[ARG] | ARGENTINA','ARG'),
        card_fb('[MAD] | MADRID','MAD')
    ],style={'display':'flex'}),
    html.Div([
        card_fb('[PER] | PERU','PER'),
        card_fb('[SV] | EL SALVADOR','SV')
    ],style={'display':'flex'}),
    html.Div([
        card_fb('[URU] | URUGUAI','URU'),
        card_fb('[ESP] | ESPANHA','ESP')
    ],style={'display':'flex'}),
    html.Div([
        card_fb('[ReD] | REP.DOMINICANA','REPDOM'),
        card_fb('[GT] | GUATEMALA ','GT')
    ],style={'display':'flex'})
])
#== Pagina YT - Global
cabecalho_yt_global = html.Div([
    html.Div([
        #https://drive.google.com/file/d/1v6F3fVZTiD117BJEUEdyrWOffP27ePCc/view?usp=sharing
        html.Img(src='https://docs.google.com/uc?id=1v6F3fVZTiD117BJEUEdyrWOffP27ePCc',className='fb_logo')
    ],style={'display':'inline-block','height':'100%'}),
    html.Div([
        html.H3('Relatório dos Grupos do Exterior',style={'text-align':'left','margin-top':'10px'}),
        html.P('CSV | Consagración a la Santísima Virgen',style={'text-align':'left','padding':'0'})
    ],style={'display':'inline-block'})
    
],style={'height':'80px'})

yt_global = html.Div([
    # Cabecalho
    cabecalho_yt_global,
    html.Hr(),
    html.Div([
        card_yt('Leads - ARGENTINA','ARG'),
        card_yt('Leads - CHILE','CHILE')
    ],style={'display':'flex'}),
    html.Div([
        card_yt('Leads - PERU','PERU'),
        card_yt('Leads - EL SALVADOR','ELSALVADOR')
    ],style={'display':'flex'}),
    html.Div([
        card_yt('Leads - PARAGUAI','PARAGUAY'),
        card_yt('Leads - MAD','MAD')
    ],style={'display':'flex'})
])
# ==== Layout Principal
content = html.Div(id='page-content')

app.layout = dbc.Container(children=[
    dbc.Row([
        # ----- Sidebar ---- #
        dbc.Col([
            dcc.Location(id='url'),
            sidebar
        ],md=2),
        
        # ---- Content ---- #
        dbc.Col([
            content
        ],md=10)
    ])
],fluid=True)

#==== Callbacks === #
@app.callback(Output('page-content','children'),[Input('url', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/overview':
        return overview
    elif pathname == '/fbcentral':
        return fb_global
    elif pathname == '/fbglobal':
        return fb_global
    elif pathname == '/ytglobal':
        return yt_global
    elif pathname == '/ytcentral':
        return yt_global
if __name__=='__main__':
    app.run_server(debug=True)