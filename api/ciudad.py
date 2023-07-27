from models.models import Ciudad
import requests 
import json 
import pandas as pd
from pandas import json_normalize
from database.database import Conexion

class CiudadExtractAPI(): 
    endpoint_ciudad='https://geocoding-api.open-meteo.com/v1/search?name='
    listaCiudad=[]

    
    def extraer_ciudad(self, listaCiudad:list): 

        for ciudad in listaCiudad: 
            busqueda=self.endpoint_ciudad+ciudad+'&count=1&language=es'
            response=requests.get(busqueda)

            if response.status_code==200: 
                response_json=response.json()
                self.listaCiudad.append(response_json)
        
        return len(self.listaCiudad)
    
    def obtener_nombres(self): 
        lista_nombres=[]
        for x in self.listaCiudad: 
            lista_nombres.append(x['results'][0]['name'])
        return lista_nombres

class TransformAPICiudad(): 

    def convertirATabla(self, listaCiudad:list)->pd.DataFrame: 
        data_nombres={ 
            "nombres":listaCiudad
        }
        df=pd.DataFrame(data_nombres) 
        return df 
    
    def normalizar_nombres(self, listaCiudad:pd.DataFrame)->None: 
        self.ciudad= listaCiudad.replace(to_replace='York', value='New York', inplace=True)
        self.ciudad=listaCiudad.replace(to_replace=['Córdoba','Taipéi','Ciudad de México','Dublín', 'Santafe de Bogotá'], value=['Cordoba', 'Tapei','Ciudad de Mexico' ,'Dublin', 'SantaFe de Bogota'], inplace=True)
        return self.ciudad


class LoadAPICiudad(): 

    def load_ciudad(self, session:Conexion, ciudad:Ciudad): 
        session.add(ciudad)
        session.commit()
   
    
   
        
        
    

