from database.database import Conexion 
from sqlalchemy.ext.declarative import declarative_base 
import pandas as pd 
from api.clima import ExtractAPIClima
from api.clima import TransformAPIClima
from api.clima import LoadAPIClima
pd.options.display.max_columns=30



Base=declarative_base()
conexion=Conexion()
conexion.get_conexion(conexion.get_engine(), Base)
engine=conexion.get_engine()
conexion.get_Session()
session=conexion.get_Session() 







if __name__=='__main__': 
    cityList = ["Londres", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tiflis" "Bogota", "Tokio"]
    coordList=["lat=51.5085&lon=-0.1257","lat=40.7143&lon=-74.006", "lat=-31.4135&lon=-64.1811", "lat=25.0478&lon=121.5319", "lat=-34.6132&lon=-58.3772", "lat=19.4285&lon=-99.1277", "lat=37.7021&lon=-121.9358", "lat=41.6941&lon=44.8337","lat=4.6097&lon=-74.0817","lat=35.6895&lon=139.6917" ]
    extractAPI=ExtractAPIClima() 
    lista=extractAPI.extraerDatos(coordList=coordList, cityList=cityList)
    transformApi=TransformAPIClima(lista)
    data=transformApi.extraerWeather(lista)
    data=pd.concat([transformApi.data_original,data], axis=1)
    df_fecha=transformApi.extraerDT(data)
    data=pd.concat([data, df_fecha], axis=1) 
   
    df_fecha=transformApi.extraerSyssunrise(data)
    data=pd.concat([data, df_fecha], axis=1)
    df_fecha=transformApi.extraerSyssunset(data) 
    data=pd.concat([data, df_fecha], axis=1)
    data=transformApi.eliminarColumnas(data)
    
    print(data)
    
    loadApi=LoadAPIClima() 
    loadApi.exportarAJSON(data)
    loadApi.exportarASQL(data=data, engine=engine)
    
    
    

   
    
    
    
   
        


    



