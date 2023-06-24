from fastapi import FastAPI
from database import database as connection

from database  import User
from database import Movie
from database import UserReview

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
        
    connection.create_tables([User,Movie,UserReview]) # Si es que las tablas ya existen no pasa nada
        
        
    

#Evento que se va lanzar cuando el servidor se encuentre finalizando 
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('Closed .....')
        

    
    





