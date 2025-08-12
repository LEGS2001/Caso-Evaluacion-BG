from tools.generate_response import generate_response
from tools.get_client_data import get_client_data

from utils.authenticate import authenticate
from utils.manage_audio import detect_voice, generate_audio

import ollama

if __name__ == "__main__":

    current_user = None # la sesion del usuario actual para así poder devolverle su información asociada
    modo = None # el modo de comunicarse con el agente, 1 es texto, 2 es voz
    rate = 200 # la velocidad con la que habla el agente de voz, el default es 200
    
    while True:
        # se guarda el usuario actual en la sesión para obtener sus datos
        if not current_user:
            # los datos estarían encriptados (contraseña) y en una base de datos, para el caso de evaluación los puse en un json
            # las credenciales las pediría el bot de Whatsapp al iniciar la conversación (o al pedir información privada del usuario)
            user_id = input('Ingrese su nombre de usuario\n')
            password = input('Ingrese su contraseña\n')
            current_user = authenticate(user_id, password)
            
            continue            
        
        # esto en el agente de WhatsApp estaría implicito, si se le envía un mensaje es texto, si se lo llama sería por voz
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
            
            # da acceso a los tools (el de responder al usuario los FAQs, revisar sus datos, etc) 
            # es sencillo agregar nuevos tools para cada funcionalidad nueva que tenga el agente, lo importante son los prompts en la 
            # descripcion de la función
            tools = [{
                'type': 'function',
                'function':{
                    'name':'generate_response',
                    'description':"""Responde las preguntas del usuario de acuerdo a los FAQs. Si el usuario hace una
                    pregunta que podría estar relacionada con cualquier duda que sería respondida como pregunta frecuente
                    del banco, se usa esta herramienta para buscar entre los datos correspondientes y responderla
                    de acuerdo a el contexto recibido.""",
                    'parameters':{
                        'type':'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'La pregunta del usuario acerca de uno de los FAQs',
                            },
                        },
                        'required': ['query'],
                    },
                    
                }
            },
                {'type': 'function',
                'function':{
                    'name':'get_client_data',
                    'description':"""Devuelve los datos del usuario (cuentas, tarjetas y polizas), 
                    solo si el usuario pidio directamente uno de estos 3 datos. Cuando el usuario hace una pregunta acerca de 
                    otra cosa no se usa este tool, pero si el usuario pregunta especificamente acerca de su informacion personal
                    de acuerdo a uno de estos 3 datos: sus tarjetas, sus cuentas o sus polizas, se llama a esta herramienta.""",
                    'parameters':{
                        'type':'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'El query del usuario preguntando acerca de sus tarjetas',
                            },
                        },
                        'required': ['query'],
                    },
                },
            },
                {'type': 'function',
                'function':{
                    'name':'repeat_response',
                    'description':"""Repite la respuesta anterior. Se usa cuando el usuario no entendio de manera correcta la respuesta
                    obtenida y usa frases como 'No entendi lo que dijiste', 'Podrias repetir eso', y otras frases parecidas que
                    impliquen que no capto de manera correcta la respuesta y necesita ser repetida nuevamente""",
                    'parameters':{
                        'type':'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'El query del usuario pidiendo repetir la respuesta',
                            },
                        },
                        'required': ['query'],
                    },
                }
            }])
            # agregar tool para bajar la velocidad de la voz

        tool_name = response['message']['tool_calls'][0]['function']['name']

        match tool_name:
            case 'generate_response':
                resp = generate_response(query)
            case 'get_client_data':
                resp = get_client_data(current_user)
            case 'repeat_response':
                if resp:
                    resp = resp
                else:
                    resp = 'No se había respondido nada anteriormente'
            case _:
                print('No puedo responder la pregunta')

        match modo:
            case 1:
                print(resp)
            case 2:
                generate_audio(str(resp), rate)

# TODO  
# CASO 2 (OPCIONAL)
# asegurar que la conexion se reestablezca en caso de desconectarse
# generar un tool que rediriga al usuario a un asistente humano
# puedes hablar mas despacio -> le bajo la frecuencia al audio