# === Bibliotecas ============
import pandas as pd
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
st.set_page_config(page_title='Visão Entregadores', layout='wide')
# === Importando o DataSet ===
df = pd.read_csv('train.csv')
df1 = df.copy()
# print(df.head())
print("Funcionando")
# ======================================

# ==== Início  da estrutura lógica =====
df1 = clean_code(df1)

st.header('Marketplace -  Visão Entregador')

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
    
    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1:
        st.markdown('### Maior idade')

        maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric('', maior_idade)

    with col2:
        st.markdown('### Menor idade')

        menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric('', menor_idade)

    with col3:
        st.markdown('### Melhor condição')
        
        melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric('', melhor_condicao)

    with col4:
        st.markdown('### Pior condição')
        
        pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric('', pior_condicao)
        
with st.container():
    st.markdown("""---""")
    st.title('Avaliações')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Avaliação média por entregador')

        df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby(['Delivery_person_ID']).mean().reset_index()

        st.dataframe(df_avg_ratings_per_deliver)

    with col2:
        st.markdown('##### Avaliação média por trânsito')

        df_avg_std_ratting_by_traffic = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings': ['mean', 'std']})
        
        df_avg_std_ratting_by_traffic.columns = ['delivery_mean', 'delivery_std']
        
        df_avg_std_ratting_by_traffic.reset_index()

        st.dataframe(df_avg_std_ratting_by_traffic)
        
        st.markdown('##### Avaliação média por clima')

        df_avg_std_ratting_by_weatherconditions = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions']).agg({'Delivery_person_Ratings': ['mean', 'std']})
        
        df_avg_std_ratting_by_weatherconditions.columns = ['delivery_mean', 'delivery_std']
        
        df_avg_std_ratting_by_weatherconditions.reset_index()

        st.dataframe(df_avg_std_ratting_by_weatherconditions)

with st.container():
    st.markdown("""---""")
    st.title('Velocidade de entrega')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Top entregadores mais rápidos')
        df3 = top_delivers(df1, top_asc=True)
        st.dataframe(df3)       

    with col2:
        st.markdown('##### Top entregadores mais lentos')
        df3 = top_delivers(df1, top_asc=False)
        st.dataframe(df3)


            