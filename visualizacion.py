from openpyxl.workbook import Workbook
import pandas as pd 
import streamlit as st 
import plotly.express as px
import io 
from pathlib import Path 
from api.clima import LoadAPIClima


@st.cache_data
def convert_to_csv(data): 
    return data.to_csv(index=False, encoding='utf-8')


if __name__=='__main__': 
    ##Retornamos una dashboard de dataframe de los datos del clima de los utlimos 5 dias 
    data=pd.read_excel('clima.xlsx') 
    tab1, tab2, tab3, tab4, tab5, tab6=st.tabs(['Tabla de Datos', 'Temperatura Media','Visualizacion', 'Mapa', 
                                    'Busqueda', 'Descargar Archivo'])
    
    tab1.header("Temperatura de los ultimos 5 dias ")
    tab1.subheader("Datos de Temperatura") 
    tab1.dataframe(data)
    ##Retornamos la temperatura media por ciudad y lo mostramos en un dashboard
    df_ciudad=data.groupby(by='ciudad', as_index=False)['Temperatura Actual'].mean()
    df_ciudad.rename(columns={"Temperatura Actual": "Temperatura media"}, inplace=True)
    print(data)
    tab2.subheader("Temperatura media por Ciudad") 
    tab2.dataframe(df_ciudad)

    ##Retornamos un grafico de pie donde se muestra la temperatura media y la ciudad
    grafico=px.pie(df_ciudad, 
                    title='Temperatura Media por Ciudad', 
                    values='Temperatura media', 
                    names='ciudad')
    tab3.plotly_chart(grafico)

    ciudad=data['ciudad'].unique()
    mapa=data[['ciudad','Latitud', 'Longitud']]
    mapa.rename(columns={"Latitud":"lat", "Longitud":"lon"}, inplace=True)

    ##Mostramos las latitudes y longitudes en un mapa
    tab4.map(mapa,zoom=2)

    ##Realiza la busqueda de la ciudad de interes y muestra las coordenadas geograficas
    select_city=tab5.selectbox("Selecciona una Ciudad:", ciudad)
    filtro=data[data['ciudad']==select_city] 
    tab5.markdown(f"Ciudad {filtro.iloc[0]['ciudad']} Latitud: {filtro.iloc[0]['Latitud']} Longitud: {filtro.iloc[0]['Longitud']}")

    ##Realiza la descarga de los datos en formato de Excel
    buffer=io.BytesIO() 
    df=data 
    with pd.ExcelWriter(buffer) as writer: 
        df.to_excel(writer, sheet_name='clima', index=False) 
        tab6.download_button(label='Descargar Archivo en Formato Excel',data=buffer, file_name='clima.xlsx', 
                            mime='application/vnd.ms-excel')
    
    ##Realiza la descarga de los datos en formato CSV
    csv=convert_to_csv(data) 
    tab6.download_button(label='Descargar Archivo en forma CSV', 
                         data=csv, 
                         file_name='clima.csv', 
                         mime='text/csv')
    
    ##Realiza la descarga de los datos en forma JSON
    API_JSON=LoadAPIClima()
    data_json=API_JSON.exportarAJSON(data)
    tab6.download_button(label='Descargar Archivo en forma JSON', 
                         data=Path('clima.json').read_text(), 
                         file_name='clima.json', 
                         mime='application/json')