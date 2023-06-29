from pydantic import BaseModel
from pydantic import validator
from peewee import ModelSelect

#Pydantic en FastAPI es una herramienta poderosa para definir y validar
# los datos que entran y salen de las API
#Al nosotros heredar de BaseModel estamos garantizando que los valores que se 
#se van a almacenados para cada atributo corresponderan a lo definido en las anotaciones

#Con esta clase vamos a convertir un objeto a diccionario y solo va  funcionar cuando se trabaje con el ORM de peewee
from pydantic.utils import GetterDict
from typing import Any


#Vamos a convertir un objeto a un diccionario
class PeeweeGetterDict(GetterDict):
    def get(self,key:Any ,default:Any=None):
        #vamos a intentar obtener los atributos del modelo y compararlos con los del schema.
        res = getattr(self._obj , key , default)
        if isinstance(res , ModelSelect):
            return list(res)
        return res



#Con esto valido datos de entrada 
class UserBaseModel(BaseModel):
    username : str
    password : str
    
    #vamos a implementar una regla de negocio
    #validaciones
    # () {}  < >
    
    @validator('username')#validamos al atributo username
    def username_validator(cls, username):
        if len(username) < 3 or len(username)>50:
            raise ValueError('La longitud debe econtrarse entre 3 y 50 caracteres') 
            #Se utiliza para mandar una excepcion especifica en el codigo
        return username    
    
#Modelo para validar datos de salida
class UserResponseModel(BaseModel):
    #Aqui se va colocar los atributos que se quieren exponer al cliente
    id:int
    username : str
    
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        




class ReviewRequestModel(BaseModel):
    #recordar que lo que se ponga en este lado van a ser necesarios al momento de crear el objeto
    user_id : int
    movie_id : int
    review : str
    score : int
    
    # () {}  < >
    @validator('score')
    def score_validator(cls,score):
        if score < 0 or score >5 :
            raise ValueError('El valor ingresado no es digito permitido')
        return score

class ReviewResponseModel(BaseModel):
    #Estos son los que se envian en la respuesta
    #userreview_id : int
    movie_id : int
    review : str
    score : int    
    #class config que nos permite serializar nuestro objeto Model
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
    
    
    
class MovieRequestModel(BaseModel):
    title : str
    year : str
    #title year
    
    

class MovieResponseModel(BaseModel):
    title : str
    year : str
    
    class Config:
        orm_mode=True
        getter_dict = PeeweeGetterDict
        
    
    
    











