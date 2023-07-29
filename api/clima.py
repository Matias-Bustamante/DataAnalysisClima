from dotenv import load_dotenv
import requests 
import os 
from datetime import datetime
import time 
import math 
import pandas as pd 
from pandas import json_normalize
from openpyxl.workbook import Workbook
from database.database import Conexion 


load_dotenv()

class ExtractAPIClima(): 
    Base_URL='https://api.openweathermap.org/data/2.5/weather?'
    APIKEY=os.getenv('APIKEY')
    key='&appid='+APIKEY
    clima=[]
    def extraerDatos(self, coordList:list, cityList:list):
        fecha=datetime.now() 
        clave="rain"
        for i in range(0,len(cityList)+1): 
            fechaActual=fecha
            fechaActual=time.mktime(fechaActual.timetuple())
            for j in range(5): 
               
                dt='&dt='+str(int(fechaActual))
                url=self.Base_URL+coordList[i]+dt+self.key
                response=requests.get(url) 
                if response.status_code==200: 
                    

                    self.clima.append(response.json())
                    fechaActual=fechaActual-86400
                else: 
                    return None 
        
        return self.clima


class TransformAPIClima(): 
       
       data_original=pd.DataFrame()

       def __init__(self, lista:list): 
        self.data_original=pd.json_normalize(lista)
        self.data_original.drop(['weather'], axis=1, inplace=True)
        
       def extraerWeather(self, lista:list)->pd.DataFrame:
             weather=pd.json_normalize(lista)['weather']
             weather=pd.json_normalize(weather)
             weather=pd.json_normalize(weather[0]) 
             weather.rename({'id':'weather.id', 'main':'weather.main','description':'weather.description','icon':'weather.icon'},axis=1, inplace=True)
             return weather
       
       def extraerDT(self, data:pd.DataFrame)->pd.DataFrame:
           lista=[]
           for i in range(len(data)): 
               lista.append(str(datetime.fromtimestamp(data.iloc[i]['dt'])))
           
           data={ 
                "date":lista
            }
           df=pd.DataFrame(data)
           return df
       
       def eliminarColumnas(self, data:pd.DataFrame)->pd.DataFrame: 
           data.drop(['dt', 'sys.sunrise', 'sys.sunset', 'wind.gust','rain.1h'], axis=1, inplace=True)
           data.rename({'date':'dt', 'date_sys':'sys.sunrise', 'data_sunset':'sys.sunset'}, axis=1, inplace=True)

           return data 
       
       def extraerSyssunrise(self, data:pd.DataFrame)->pd.DataFrame: 
           lista=[] 
           for i in range(len(data)): 
               lista.append(str(datetime.fromtimestamp(data.iloc[i]['sys.sunrise'])))
            
           data={ 
                "date_sys":lista
            }
           df=pd.DataFrame(data) 
           return df 
       
       def extraerSyssunset(self, data:pd.DataFrame)->pd.DataFrame: 
           lista=[] 
           for i in range(len(data)): 
               lista.append(str(datetime.fromtimestamp(data.iloc[i]['sys.sunset'])))
           data= { 
              "data_sunset":lista 
          }
           df=pd.DataFrame(data) 
           return df 


class LoadAPIClima(): 

    def exportarACSV(self, data:pd.DataFrame): 
        data.to_csv('clima.csv', index=False)
        
           
    def exportarAExcel(self, data:pd.DataFrame): 
        data.to_excel('clima.xlsx', index=False)  
       

    def exportarAJSON(self, data:pd.DataFrame):
        data.to_json('clima.json',orient='index') 
    
    def exportarASQL(self, data:pd.DataFrame, engine:Conexion): 
        data.to_sql('clima', engine, if_exists='replace', index=False)


                

      