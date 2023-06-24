from fastapi import FastAPI
from database import database as connection

from database  import User
from database import Movie
from database import UserReview

#Importamos las validaciones
from schemas import UserBaseModel

from fastapi import HTTPException

# () {}  < >

#Vamos a generar la instancia
app = FastAPI(
    title='Reseña de Peliculas',
    description='Con este proyecto se busca poder hacer reseñas de pelis',
    version=1
    )
                                            
#puede ser cualquier metodo http
@app.get('/') #es un decorador         
async def index():#La funcion se ejecuta de forma asincróna  
    return 'Hola mundo , desde un servidor en FastApi'


@app.get('/about')
async def about():
    return 'About'


#Eventos.

#Evento que se va lanzar antes que el servidor inicié
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
        
        print('Connecting .....')
        
    connection.create_tables([User,Movie,UserReview]) 
    # Si es que las tablas ya existen no pasa nada
    #Per sino está vamos a crear la base de datos
        
        
    

#Evento que se va lanzar cuando el servidor se encuentre finalizando 
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('Closed .....')
        


#Vamos a definir la creacion de un usuario
#usando el metodo post del http
#Fastapi se apoya de pydanti para validar los valores 
#de entrada como de salida
@app.post('/users')
async def create_user(user : UserBaseModel): # user es el nombre del parametro y UserBaseModel es el tipo de dato esperado
   #para que la funcion se ejecute debe de recibir un objeto UserBaseModel
   
   #Validacion de duplicidad de usuarios
   #                      Algun registro del username de la db que sea igual al username ingresado
    if User.select().where(User.username == user.username).exists():
       return HTTPException(409,'El username ya se encuentra en uso ')
   
    hash_password = User.create_password(user.password)
    
    user = User.create(
        username = user.username,
        password = hash_password
    )
    
    return user.id
    