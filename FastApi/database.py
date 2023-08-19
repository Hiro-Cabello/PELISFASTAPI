#Peewee es un ORM ligero y efectivo
from peewee import *
from datetime import datetime

import hashlib
# () {}  < >

#conexion a la base de datos
database = PostgresqlDatabase(
    'fastapi_project',
    user='postgres',
    password='jairo',
    host='localhost',
    port=5432)


#vamos a definir tres modelos user , movie y userreview
#Para que las clases se consideren modelos deben de heredar de model
class User(Model):
    username = CharField(max_length=50 , unique=True)
    password = CharField(max_length=50)
    create_at = DateTimeField(default=datetime.now)#No hay necesidad de indicar la fecha pues es automatico la captacion del valor
    
    
    #con esta clase podemos personalizar los modelos declarativos
    class Meta:
        database = database
        table_name = 'users'
        
    #Este decorador se utiliza para definir los métodos de clase.
    @classmethod #metodo de clase
    def create_password(cls,password):#cls de clase y password en texto plano
        h = hashlib.md5()
        #password = h.update(password)
        h.update(password.encode('utf-8'))
        
        return h.hexdigest()
    
    def __str__(self):
        return self.username
        
        


class Movie(Model):
    title = CharField(max_length=50)
    #year = CharField(max_length=4)
    created_at = DateTimeField(default=datetime.now)
    
    #def __str__(self):
    #    return self.title
    
    class Meta: 
        database = database
        table_name = 'movies'


class UserReview(Model):
    user=ForeignKeyField(User , backref='reviews')
    movie= ForeignKeyField(Movie)
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = database
        tablename = 'user_reviews'
        
        
    def __str__(self):
        return f' {self.user.username} - {self.movie.title} '
