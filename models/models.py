from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey,Numeric
from sqlalchemy.orm import sessionmaker, relationship,backref
from sqlalchemy.ext.declarative import declarative_base 
from database.database import Conexion

Base=declarative_base()
engine=Conexion()

class Ciudad(Base): 
    __tablename__='ciudad' 
    id=Column(Integer, primary_key=True, autoincrement=True)
    nombre=Column(String(100))
    pais=relationship('Pais', backref='ciudad')

    def __str__(self): 
        return f"id:{self.id} Nombre {self.nombre}"
    
    def getId(id:int)->int:
        return id
    
    def getNombre(nombre:str)->str:  
        return nombre

class Clima(Base): 
    __tablename__='clima'
    id=Column(Integer, primary_key=True, autoincrement=True)
    temperatura=Column(Numeric)
    sensacionTermica=Column(Numeric)
    temperaturaMinima=Column(Numeric) 
    temperaturaMaxima=Column(Numeric) 
    presion=Column(Numeric) 
    humedad=Column(Numeric)
    nivelMar=Column(Numeric) 
    nivelSuelo=Column(Numeric) 
    visibilidad=Column(Numeric) 
    velocidadViento=Column(Numeric) 
    direccionViento=Column(Numeric) 
    rafagaViento=Column(Numeric) 
    nubosidad=Column(Numeric) 
    hora=Column(DateTime) 
    horaSalidaSol=Column(DateTime) 
    horaAtardecer=Column(DateTime)
    provinciaId=Column(Integer, ForeignKey('pais.id'))


class Pais(Base): 
    __tablename__='pais'
    id=Column(Integer, primary_key=True, autoincrement=True) 
    nombre=Column(String(100)) 
    clima=relationship('Clima', uselist=False, backref='pais')
    ciudad_id=Column(Integer, ForeignKey('ciudad.id'))



engine.get_conexion(engine.get_engine(), Base)
engine.get_Session()

