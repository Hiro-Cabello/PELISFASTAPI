from fastapi import FastAPI
from database import database as connection

from database  import User
from database import Movie
from database import UserReview

#Importamos las validaciones
from schemas import UserBaseModel
from schemas import UserResponseModel


from fastapi import HTTPException


from schemas import ReviewRequestModel
from schemas import ReviewResponseModel


from schemas import MovieRequestModel
from schemas import MovieResponseModel

from schemas import ReviewRequestPutModel


from typing import List #Al usar List podemos especificar el tipo de elemento de la lista 

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
@app.post('/users' , response_model = UserResponseModel)#Con el response_model nos indica que la respuesta del servidor va ser un objeto tipo UserResponseModel
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
    
    #Con esto nos damos cuenta que los modelos nos permiten validar datos de salida como de entrada
#    return UserResponseModel(id=user.id , username=user.username)
#Con esto podremos convertir nuestros modelos de peewee a modelos de pydantic
    return user




@app.post('/reviews',response_model = ReviewResponseModel)#
async def create_review(user_review : ReviewRequestModel):
    #user movie review  score
    
    # () {}  < >
    
    #Esto es para validar la primera coincidencia
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code = 404 , detail = 'User not found')
    
    if Movie.select().where(Movie.id == user_review.movie_id ).first() is None:
        raise HTTPException(status_code = 404 , detail = 'Movie no encontrada')
    #Izquierdo va los nombres que estan en la tabla
    #           UserReview es el modelo
    user_review = UserReview.create(
        user_id = user_review.user_id ,
        movie_id = user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review





#crear un endpoint en fastapi
#Con el metodo post es para enviar datos al servidor
@app.post('/movies',response_model=MovieResponseModel)#Aqui defino la respuesta
async def create_movie(movie : MovieRequestModel):
    
    movie = Movie.create(
        title = movie.title,
        year = movie.year
    )
    
    return movie

    # () {}  < >


#Endpoint para poder obtener del servidor una lista de reseñas
#Con el metodo get lo que vamos a conseguir es recuperar datos del servidor
#En este caso la funcion no posee ningun parametro no se le pasa nada como parametro
 #Aquí estoy definiendo mi respuesta y especificandole que va ser una lista y los elemtos van a ser de tipo ReviewResponseModel
@app.get('/reviews' , response_model = List[ReviewResponseModel])
async def get_reviews():
    #vamos a realizar una peticion a la base de datos
    reviews = UserReview.select() #Select * from user_rev
    
    return [user_review for user_review in reviews]
 

#EndPoint para obtener un reseña ingresando id de la pelicula
@app.get('/reviews/{movie_id}' , response_model=ReviewResponseModel)#Si en caso no definimos como va ser la salida se puede obtener una estructura rara de salida
async def get_reviewsformovie(movie_id:int):

    reviewsformovie = UserReview.select().where(UserReview.movie_id == movie_id).first()
    
    if reviewsformovie is None:
        raise HTTPException(status_code=404,detail='Review Not found for the displayed movie ID')
    #Ahora que sucederia si para este idmovie tiene mas reseñas
    return reviewsformovie
         
         

#EndPoint para obtener un reseña ingresando id de la pelicula
@app.get('/reviewid/{review_id}' , response_model=ReviewResponseModel)#Si en caso no definimos como va ser la salida se puede obtener una estructura rara de salida
async def get_reviews(review_id:int):

    reviewsforid = UserReview.select().where(UserReview.id == review_id).first()
    
    if reviewsforid is None:
        raise HTTPException(status_code=404,detail='Review Not found for the displayed movie ID')
    #Ahora que sucederia si para este idmovie tiene mas reseñas
    return reviewsforid

#Vamos a actualizar las reseñas
    # () {}  < >

@app.put('/reviews/{review_id}' , response_model=ReviewResponseModel)#ahora tambien vamos a indicar el endpoint va retornar un ReviewResponseModel
async def update_review(review_id:int , review_request : ReviewRequestPutModel ):#Este es el molde como va recibir el parametro
    
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    
    if user_review is None:
        raise HTTPException(status_code=404,detail='Review Not found for the displayed movie ID')
    
    user_review.review = review_request.review
    user_review.score  = review_request.score
    
    
    #para persistir los cambios nosotros vamos a hacer
    user_review.save()
    

    return user_review