import pandas as pd 
import json 
import requests
from database.database import Conexion
from models.models import Pais

class ExtractAPIPais(): 
    
    endpoint_pais='https://geocoding-api.open-meteo.com/v1/search?name='
    lista_pais=[]
    def extraer_pais(self, listaCiudad:list):

        for ciudad in listaCiudad: 
                busqueda=self.endpoint_pais+ciudad+'&count=1&language=es'
                response=requests.get(busqueda)

                if response.status_code==200: 
                    response_json=response.json()
                    self.lista_pais.append(response_json)
            
        return self.lista_pais
    
    def obtener_nombrePais(self)->list: 
        nombre_pais=[]
        for x in self.lista_pais: 
            nombre_pais.append(x['results'][0]['country'])
        return nombre_pais

class TransformAPIPais(): 
     
     def convertirATabla(self, lista_pais:list)->pd.DataFrame:
          data_pais={ 
               "nombres":lista_pais
          }
          df= pd.DataFrame(data_pais) 
          return df 
     
     def normalizar_datos(self, lista_pais:pd.DataFrame)->pd.DataFrame: 
          self.pais=lista_pais.replace(to_replace='RU', value='Reino Unidos', inplace=True)
          self.pais=lista_pais.replace(to_replace=['Taiwán','México','Japón'], value=['Taiwan','Mexico','Japon'], inplace=True)
          return self.pais 
     
     def convertirCiudadATabla(self, lista:list)->pd.DataFrame: 
         lista_id=[]
         lista_ciudad=[] 
         for ciudad in lista: 
              lista_id.append(ciudad['id'])
              lista_ciudad.append(ciudad['nombre']) 
        
         data= { 
             "id":lista_id, 
             "nombre":lista_ciudad
        }
         df=pd.DataFrame(data)
         return df
    
     def concatenarListas(self, lista_pais:pd.DataFrame, lista_ciudad:pd.DataFrame)->pd.DataFrame:
         lista_pais_ciudad=pd.concat([lista_pais, lista_ciudad], axis=1) 
         lista_pais_ciudad.rename(columns={"nombres":"Pais", "id":"ID", "nombre":"Ciudad"}, inplace=True)
         return lista_pais_ciudad



class LoadAPIPais(): 
     

     def load_pais(self, session:Conexion, pais:Pais): 
          session.add(pais) 
          session.commit()
          
     