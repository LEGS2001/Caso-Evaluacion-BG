from tools.generate_response import generate_response
from tools.get_client_data import get_client_data

from utils.authenticate import authenticate
from utils.detect_voice import detect_voice, generate_audio

import ollama

if __name__ == "__main__":

    current_user = None
    modo = None

    while True:
        # se guarda el usuario actual en la sesión para obtener sus datos
        if not current_user:
            # los datos estarían encriptados (contraseña) y en una base de datos, para el caso de evaluación los puse en un json
            # las credenciales las pediría el bot de Whatsapp al iniciar la conversación
            user_id = input('Ingrese su nombre de usuario\n')
            password = input('Ingrese su contraseña\n')
            current_user = authenticate(user_id, password)
            
            continue            

        if not modo:
            modo = int(input('Seleccione si quiere realizar su pregunta por texto, o por voz\n 1) Texto\n 2) Voz\n'))

        match modo:
            case 1:
                query = input("Escriba su pregunta\n")
            case 2:
                print("Diga su pregunta\n")
                query = detect_voice()
            case _:
                modo = int(input('Seleccione si quiere realizar su pregunta por texto, o por voz\n 1) Texto\n 2) Voz\n'))
                continue

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
            },
                {'type': 'function',
                    'function':{
                        'name':'exit_conversation',
                        'description':'Termina la conversación con el usuario',
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
                resp = generate_response(query)
            case 'get_client_data':
                resp = get_client_data(current_user)
            case 'exit_conversation':
                print('Terminando la conversación')
                break
            case _:
                print('No puedo responder la pregunta')

        match modo:
            case 1:
                print(resp)
            case 2:
                generate_audio(str(resp))

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
# generar un tool que rediriga al usuario a un asistente humano

# IMPORTANTE -> Falta implementar la parte de que el agente responda con voz

# puedes hablar mas despacio -> le bajo la frecuencia al audio
# repite eso/no te entiendo -> se guarda la respuesta del agente en una variable, y si se llama a este tool, se devuelve la
# misma respuesta