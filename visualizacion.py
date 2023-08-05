from openpyxl.workbook import Workbook
import pandas as pd 
import streamlit as st 
import plotly.express as px
data=pd.read_excel('clima.xlsx') 

st.set_page_config(page_title="Temperatura OpenWeather Map", layout='wide')
st.header("Temperatura de los ultimos 5 dias ")
st.subheader("Datos de Temperatura") 
st.dataframe(data)
df_ciudad=data.groupby(by='ciudad', as_index=False)['Temperatura Actual'].mean()
df_ciudad.rename(columns={"Temperatura Actual": "Temperatura media"}, inplace=True)
print(data)
st.subheader("Temperatura media por Ciudad") 
st.dataframe(df_ciudad)

grafico=px.pie(df_ciudad, 
                   title='Temperatura Media por Ciudad', 
                   values='Temperatura media', 
                   names='ciudad')
st.plotly_chart(grafico)

ciudad=data['ciudad'].unique()
mapa=data[['ciudad','Latitud', 'Longitud']]
mapa.rename(columns={"Latitud":"lat", "Longitud":"lon"}, inplace=True)

st.map(mapa,zoom=2)

select_city=st.selectbox("Selecciona una Ciudad:", ciudad)

filtro=data[data['ciudad']==select_city] 

st.markdown(f"Ciudad {filtro.iloc[0]['ciudad']} Latitud: {filtro.iloc[0]['Latitud']} Longitud: {filtro.iloc[0]['Longitud']}")

