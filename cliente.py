#Vamos a realizar un cliente que haga la peticion al servidor hemos creado
#modulo que es bastante facil de utilizar
from urllib import request

#Direccion a la cual se va hacer la peticion
URL='http://127.0.0.1:8000/'

response = request.urlopen(URL)

#print(response.__dict__)
print(response.read())








