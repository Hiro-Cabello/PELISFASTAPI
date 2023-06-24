#FastApi se apoya en las anotaciones por eso es muy 
#importante

#Anotaciones en : () > {}
#   Variables
#   Funciones
#   Clases
#   Colecciones 


from typing import List  #Esto es para definir la clase List
from typing import Tuple #Esto es para definir la clase Tuple
from typing import Union  # 

from typing import Dict


#Pydantic
from pydantic import BaseModel


a : str = 'Hola , esta es una variable'
b : int = 30 
c : float = 3.14
d : bool = True

print(a)
print(b)
print(c)
print(d)


#def sumar
def sumar(numero1 : int , numero2 : int ) -> int :
    return numero1 + numero2

valor1 : int = 10 
valor2 : int = 20

#No definimos el valor pero si el tipo de dato
valor3 : int


resultado : int = sumar(valor1 , valor2) 
print('Este es el resultado de la suma :  {} '.format(resultado))


#Ahora vamos con clases

class User():
    def __init__(self,username:str,password:str) -> str :
        self.username= username
        self.password = password
        
    def saludar(self)->str:
        return f'Hola {self.username}'

cody = User('Cody' , 'password123')
print(
    cody.saludar()
)

#Las anotacones no son reglas para el lenguaje
#Las anotaciones van seguida a los desarrolladores para que se pueda seguir un estandar de codificacion



#Ahora vamos con colecciones
calificaciones : List[int] = [10,9,5,5,7,9,9]

def promedio(calificaciones : List[int]) -> float : 
    return sum(calificaciones)/len(calificaciones)

print( 'La calificacion para este usuario es {} '.format(promedio(calificaciones)) )



#Ahora vamos con Tuples
#Las anotaciones no estan implementadas para que se interpreten sino 
#para que sea interpretada por los desarrolladores.
configuraciones : Tuple[str] = ('localhost','3306','root')

configuraciones_2 : Tuple[Union[str,str,bool,int]] = ('root','localhost',123,True)
print(configuraciones_2)


#Uso de diccionarios.
usuarios : Dict[str , int] = {
    'eduardo':10 ,
    'cody':15
}

print( 'Los usuarios son {}'.format(usuarios) )

#Pydantic
#La libreria fastAPI usa la libre la libreria Pydantic , esta libreria nos permite validar los datos de entrada y de salida
#Pydantic es una biblioteca de validacion de python  , utilizada para definir modelos de datos
#Facilita la creacion de modelos de datos robustos y la manipulacion segura de datos
# () > {}

#Si en caso tenga un atributo que algunas veces se use o no 
#Para este caso se va usar import Optional
#  >  <

from typing import Optional
from pydantic import validator
from pydantic import ValidationError

class User_1(BaseModel):#User hereda de la clase BaseModel
    username : str  # requerido, quiere decir que si yo ingreso un valor diferente al especificado me va salir error
    password : str
    repeat_password : int 
    email : str 
    age : Optional[int] = None
    
#Validador de clase
    @validator('username') # para validar un atributo de la clase
    def username_validation_lenght(cls , username):
        if len(username) < 3:
            raise ValueError('La longitud mínima es de 4 caracteres')
        if len(username) > 50:
            raise ValueError('La longitud máxima es de 50 caracteres')
        
        return username
    
    @validator('repeat_password')                           #values no es más que un diccionario donde se va encontrar todos los atributos del modelo
    def password_validation_repeat(cls , repeat_password, values):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError('Las contraseñas son diferentes')
    
        return repeat_password
    

try:
    
    # Crear una instancia de la clase User y validar los campos
    user_data = {
        'password': 'password123',
        'username' : 'Co',
        'password':'asdf12345',
        'repeat_password':'123',
        'email' : 'ronal@unmsm.edu.pe',
        #age =21
    }
    
    user1 = User_1( **user_data)
    
    print(user1)
except ValidationError as e:
    print(e.json())








