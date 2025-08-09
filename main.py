from tools.generate_response import generate_response
from tools.get_client_data import get_client_data

from utils.authenticate import authenticate

import ollama


if __name__ == "__main__":
    
    current_user = None
    # se guarda el usuario actual en la sesión para obtener sus datos
    while not current_user:
        # los datos estarían encriptados (contraseña) y en una base de datos, para el caso de evaluación los puse en un json
        # las credenciales las pediría el bot de Whatsapp al iniciar la conversación
        user_id = input('Ingrese su nombre de usuario\n')
        password = input('Ingrese su contraseña\n')
        
        current_user = authenticate(user_id, password)

    
    query = input("Ingrese su pregunta\n")
    
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role':'user', 
                    'content': query}],
        # da acceso a los tools (el de responder al usuario los FAQs y el de revisar sus datos)
        tools = [{
            'type': 'function',
            'function':{
                'name':'generate_response',
                'description':'Responde las preguntas del usuario',
                'parameters':{
                    'type':'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'La pregunta del usuario',
                        },
                    },
                    'required': ['query'],
                },
                
            }
        },
            {'type': 'function',
            'function':{
                'name':'get_client_data',
                'description':'Devuelve los datos del usuario (cuentas, tarjetas y polizas)',
                'parameters':{
                    'type':'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'La pregunta del usuario',
                        },
                    },
                    'required': ['query'],
                },
            },
        }])
    
    tool_name = response['message']['tool_calls'][0]['function']['name']

    match tool_name:
        case 'generate_response':
            print(generate_response(query))
        case 'get_client_data':
            print(get_client_data(current_user))
        case _:
            print('No puedo responder la pregunta')


    # TODO 
    # CASO 1 (OBLIGATORIO) 
    # generar otra funcion (tool) que se encargue de devolver los datos del usuario autenticado DONE
    # usar encriptacion para asegurar seguridad 
    # probar utilizar langchain para el manejo de los tools correspondientes DONE (se implementó directamente con ollama tooling)
    # 
    # CASO 2 (OPCIONAL)
    # implementar lo mismo que la vtuber ai de speech to text 
    # conectarlo con la funcionalidad principal de LLMs
    # asegurar que la conexion se reestablezca en caso de desconectarse