
from pydantic import BaseModel
#from pydantic import ResponseModel
from pydantic import validator
from peewee import ModelSelect

#Pydantic en FastAPI es una herramienta poderosa para definir y validar
# los datos que entran y salen de las API
#Al nosotros heredar de BaseModel estamos garantizando que los valores que se 
#se van a almacenados para cada atributo corresponderan a lo definido en las anotaciones

#Con esta clase vamos a convertir un objeto a diccionario y solo va  funcionar cuando se trabaje con el ORM
#de peewee
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



class ResponseModel(BaseModel):
    
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


#----------------USER -----------------------------

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
            raise ValueError('La longitud debe encontrarse entre 3 y 50 caracteres') 
            #Se utiliza para mandar una excepcion especifica en el codigo
        return username    
    
#Modelo para validar datos de salida
class UserResponseModel(ResponseModel):
    #Aqui se va colocar los atributos que se quieren exponer al cliente
    id:int
    username : str
    
#    class Config:
#        orm_mode = True
#        getter_dict = PeeweeGetterDict
        

#Vamos a abstraer la validacion
class ReviewValidator():
 # () {}  < >
    @validator('score')
    def score_validator(cls,score):
        if score < 0 or score >5 :
            raise ValueError('El valor ingresado no es digito permitido')
        return score

#------ MOVIE --------------------

class MovieRequestModel(BaseModel):
    title : str
    year : str
    #title year
    


class MovieResponseModel(ResponseModel ):
    id : int
    year : str
    
#    class Config:
#        orm_mode=True
#        getter_dict = PeeweeGetterDict

class MovieResponseModel2(ResponseModel ):
    id : int
    title : str
    

#class ReviewRequestModel(BaseModel , ReviewValidator):#Con esto estamos aprovechando la herencia multiple que se puede en el lenguaje
class ReviewRequestModel(BaseModel , ReviewValidator):
    #recordar que lo que se ponga en este lado van a ser necesarios al momento de crear el objeto
    user_id : int
    movie_id : int
    review : str
    score : int
    
#Estos son los que se envian en la respuesta

class ReviewResponseModel(ResponseModel):
    id : int 
    movie: MovieResponseModel2
    #cuando ponia movie_id me salia el error pues hasta donde entiendo hay problemas 
    review : str
    score : int    



# () {}  < >
#vamos a definir los valores de entrada
class ReviewRequestPutModel(BaseModel , ReviewValidator):
    review :str
    score:int

    @validator('score')
    def score_validator(cls,score):
        if score < 0 or score >5 :
            raise ValueError('El valor ingresado no es digito permitido')
        return score









