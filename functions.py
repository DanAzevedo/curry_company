import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

# === FUNÇÕES ================
# === LIMPEZA DE DADOS =======
def clean_code(df1):
    ''' Função com a responsabilidade de limpar o DataFrame

        Tipos de limpeza:
        1. Remoção dos dados Nan
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: DataFrame
        Output: DataFrame
    '''
    # Eliminando as linhas com valores 'NaN ' para evitar erro ao converter
    df1 = df1.loc[df1['Delivery_person_Age'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['multiple_deliveries'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['City'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['Festival'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['Weatherconditions'] != 'conditions NaN', :].copy()
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN ', :].copy()
    
    # Removendo os espaços em branco dentro das strings sem usar o for para maior velocidade de processamento
    # Converting 'ID' column to string type before applying str.strip()
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].astype(str).str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].astype(str).str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].astype(str).str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].astype(str).str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].astype(str).str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].astype(str).str.strip()
    
    # Convertendo Delivery_person_Age, multiple_deliveries de string para int
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # Convertendo Delivery_person_Age, Restaurant_latitude, Restaurant_longitude, Delivery_location_latitude e Delivery_location_longitude em float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Restaurant_latitude'] = df1['Restaurant_latitude'].astype(float)
    df1['Restaurant_longitude'] = df1['Restaurant_longitude'].astype(float)
    df1['Delivery_location_latitude'] = df1['Delivery_location_latitude'].astype(float)
    df1['Delivery_location_longitude'] = df1['Delivery_location_longitude'].astype(float)
    
    # Convertendo Order_Date de string para date
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # Limpando a coluna Time_taken(min)
    df1.loc[:, 'Time_taken(min)'] = df1.loc[:, 'Time_taken(min)'].apply(lambda x: x.split('(min) ')[1]).astype(int)
    # ========================

    return df1

# VISÃO EMPRESAS ============
def order_metric(df1):        
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    
    return fig

def traffic_order_share(df1):            
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')

    return fig

def traffic_order_city(df1):
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()

    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def order_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')

    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    
    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig

def order_share_by_week(df1):
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    
    # junto os dois dfs
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
    fig = px.line(df_aux, x='week_of_year', y='order_by_delivery')

    return fig

def country_maps(df1):
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()
    
    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                     location_info['Delivery_location_longitude']],
                     popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    
    folium_static(map, width=1024, height=600)

    return None
# ============================

# VISÃO ENTREGADORES ===========
def top_delivers(df1, top_asc):
            df2 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index()

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
        
            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

            return df3

# VISÃO RESTAURANTES ===========
def distance(df1, fig):
    if fig == False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x: 
                                                 haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                           (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = np.round(df1['distance'].mean(), 2)
        return avg_distance
    else:
        df1['distance'] = df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']].apply(lambda x:
                                        haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                  (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])

        return fig


def avg_std_time_delivery(df1, op, festival):
    '''Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
       Parâmetros:
           Input:
               - df: DataFrame ccom os dados necessários para o cálculo
               - op: Tipo de operação que pode ser calculada 
                   'avg_time': Calcula o tempo médio
                   'std_time': Calcula o desvio padrão do tempo         
           Output: 
               - df: DataFrame com duas colunas e uma linha
    '''
    df_aux = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)

    return df_aux

def avg_std_time_graph(df1):                    
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Controle', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig

def evg_std_time_on_traffic(df1):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                     color='std_time', color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig