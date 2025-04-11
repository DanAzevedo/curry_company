# === Bibliotecas ============
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static
from functions import *
# ======================================
st.set_page_config(page_title='Visão Restaurantes', layout='wide')
# === Importando o DataSet ===
df = pd.read_csv('train.csv')
df1 = df.copy()
# print(df.head())
print("Funcionando")
# ======================================

# ==== Início  da estrutura lógica =====
df1 = clean_code(df1)

st.header('Marketplace -  Visão Restaurantes')

# ======================================
# Barra Lateral no Streamlit 
# ======================================

# image = Image.open()
# st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## O delivery mais rápido da cidade')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Daniel Azevedo Marcondes de Souza')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito 
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ========================
# Layout no Streamlit 
# ========================
with st.container():
    st.markdown('##### Métricas gerais')
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        col1.metric('Entregadores únicos', delivery_unique)
        
    with col2:
        avg_distance = distance(df1, fig=False)
        col2.metric('A distância média', avg_distance)
    
    with col3:
        df_aux =  avg_std_time_delivery(df1, 'avg_time', 'Yes')
        col3.metric('Tempo médio', df_aux)
    
    with col4:
        df_aux =  avg_std_time_delivery(df1, 'std_time', 'Yes')
        col4.metric('STD Entrega', df_aux)
        
    with col5:
        df_aux =  avg_std_time_delivery(df1, 'avg_time', 'No')
        col5.metric('Tempo médio', df_aux)
        
    with col6:    
        df_aux =  avg_std_time_delivery(df1, 'std_time', 'No')
        col6.metric('STD Entrega', df_aux)

with st.container():
    st.markdown("""---""")    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Tempo médio de entrega por cidade')

        fig = avg_std_time_graph(df1)
        st.plotly_chart(fig)

    with col2:
        st.markdown('##### Distribuição da distância')
    
        df_aux = df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
    
        st.dataframe(df_aux)
    
        

with st.container():
    st.markdown("""---""")
    st.markdown('##### Distribuição do tempo')

    col1, col2 = st.columns(2)

    with col1:
        fig = distance(df1, fig=True)
        st.plotly_chart(fig)
        
    with col2:
        fig = evg_std_time_on_traffic(df1)
        st.plotly_chart(fig)



