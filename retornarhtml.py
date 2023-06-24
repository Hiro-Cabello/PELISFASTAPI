from wsgiref.simple_server import make_server


HTML="""  
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Servidor en Python</title>
</head>
    <body>
     <h1>Hola mundo , desde mi primer servidor en Python</h1>
    </body>
</html>

"""
#env             -Diccionario donde vamos a almacenar info importante con respecto a la peticion del cliente
#start_response  -
def application(env,start_response):

    headers = [('Content-Type','text/html')]

    start_response('200 OK',headers)

    return [bytes(HTML,'utf-8')]

server = make_server('localhost',8000,application)
server.serve_forever()

#De esta manera se va crear el servidor.
