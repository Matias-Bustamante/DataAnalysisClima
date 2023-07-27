import pandas as pd 
import json 
import requests

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
