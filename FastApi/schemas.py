from pydantic import BaseModel
from pydantic import validator

#Pydantic en FastAPI es una herramienta poderosa para definir y validar
# los datos que entran y salen de las API
#Al nosotros heredar de BaseModel estamos garantizando que los valores que se 
#se van a almacenados para cada atributo corresponderan a lo definido en las anotaciones
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