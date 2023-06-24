from jinja2 import Environment
from jinja2 import FileSystemLoader
from wsgiref.simple_server import make_server #Proporciona un servidor HTTP en desarrollo


#env             -Diccionario donde vamos a almacenar info importante con respecto a la peticion del cliente
#start_response  -
def application(env,start_response):

    headers = [('Content-Type','text/html')]

    start_response('200 OK',headers)
    
    env = Environment(loader=FileSystemLoader('templates')) #Esta es nuestra carpeta y folder

    template = env.get_template('index.html') # Nombre del template
    
    html= template.render( #Nos va renderizar el maquetado
      { 
        'title':'S-Python',
        'name': 'Eduardo Ismael'
      }
    )
    
    return [bytes(html,'utf-8')]

server = make_server('localhost',8000,application)
server.serve_forever()

#De esta manera se va crear el servidor.
