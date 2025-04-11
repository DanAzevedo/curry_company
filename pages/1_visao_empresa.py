# === Importações ============
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
st.set_page_config(page_title='Visão Empresas', layout='wide')
# === Importando o DataSet ===
df = pd.read_csv('train.csv')
df1 = df.copy()
# print(df.head())
print("Funcionando")
# ======================================

# ==== Início  da estrutura lógica =====
df1 = clean_code(df1)

st.header('Marketplace -  Visão Cliente')

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
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    
    with st.container():
        st.markdown('### Pedidos por dia')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Pedidos por tipo de tráfego')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown('### Pedidos por cidade e tipo de tráfego')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)        
            
with tab2:
    
    with st.container():
        st.markdown('### Pedidos por semana')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('### Pedidos por entregadores por semana')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)    
    
with tab3:
    st.markdown('### Mapa')
    country_maps(df1)