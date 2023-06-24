from wsgiref.simple_server import make_server

#env             -Diccionario donde vamos a almacenar info importante con respecto a la peticion del cliente
#start_response  -
def application(env,start_response):

    headers = [('Content-Type','text/plain')]

    start_response('200 OK',headers)

    return ['Hola mundo , desde mi primer servidor en Python'.encode('utf-8')]

server = make_server('localhost',8000,application)
server.serve_forever()

#De esta manera se va crear el servidor.
