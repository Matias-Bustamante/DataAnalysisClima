from models.models import Ciudad, Pais,  Clima
from database.database import Conexion 
from sqlalchemy.ext.declarative import declarative_base 
import requests
import pandas as pd 
import json 
from api.ciudad import CiudadExtractAPI, TransformAPICiudad, LoadAPICiudad
from api.pais import ExtractAPIPais, TransformAPIPais, LoadAPIPais


Base=declarative_base()
conexion=Conexion()
conexion.get_conexion(conexion.get_engine(), Base)
engine=conexion.get_engine()
conexion.get_Session()
session=conexion.get_Session() 





if __name__=='__main__': 
    cityList = ["Londres", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin",  "Bogota", "Tokio"]
    """Instanciamos las correspondiente de ciudad encargado de realizar el proceso ETL
    CiudadExtractAPI: Se encarga de extraer los datos de la api
    TransformAPICiudad: Se encarga de Transformar los datos de la api, normalizar los datos
    LoadCiudadAPi: Se encarga de almacenar los datos en la base de datos 
    """
    ciudad_api=CiudadExtractAPI() 
    ciudadApiTransform=TransformAPICiudad()
    loadApiCiudad=LoadAPICiudad()
    print (ciudad_api.extraer_ciudad(cityList))
    lista_ciudad=ciudad_api.obtener_nombres()
    lista_ciudad=ciudadApiTransform.convertirATabla(lista_ciudad)
    print(ciudadApiTransform.normalizar_nombres(lista_ciudad))
    ##print(lista_ciudad)
    """
    for i in range(0, len(lista_ciudad)): 
        ciudad=Ciudad(nombre=lista_ciudad.iloc[i]['nombres'])
        loadApiCiudad.load_ciudad(session, ciudad)
        """
    """Proceso de ETL PAIS """
    pais_api=ExtractAPIPais()
    pais_transform=TransformAPIPais()
    loadAPIPais=LoadAPIPais()
    print(pais_api.extraer_pais(listaCiudad=cityList))
    lista_pais=pais_api.obtener_nombrePais()
    lista_pais=pais_transform.convertirATabla(lista_pais=lista_pais)
    pais_transform.normalizar_datos(lista_pais=lista_pais)
    ##print(lista_pais)
    lista=ciudad_api.leerDatosBaseDatos(session=session)
    lista_ciudad=pais_transform.convertirCiudadATabla(lista)
    lista_pais_ciudad=pais_transform.concatenarListas(lista_pais=lista_pais, lista_ciudad=lista_ciudad)
    for i in range(0, len(lista_pais_ciudad)): 

        pais=Pais(nombre=lista_pais_ciudad.iloc[i]['Pais'], ciudad_id=int(lista_pais_ciudad.iloc[i]['ID']))
        loadAPIPais.load_pais(session,pais)
    
    
   
        


    



