from tools.generate_response import generate_response
from tools.get_client_data import get_client_data

from utils.authenticate import authenticate


if __name__ == "__main__":
    
    current_user = None
    
    # se guarda el usuario actual en la sesión para obtener sus datos
    while not current_user:
        # los datos estarían encriptados (contraseña) y en una base de datos, para el caso de evaluación los puse en un json
        # las credenciales las pediría el bot de Whatsapp al iniciar la conversación
        user_id = input('Ingrese su nombre de usuario\n')
        password = input('Ingrese su contraseña\n')
        
        current_user = authenticate(user_id, password)
    
    #query = input("Ingrese su pregunta\n")
    #print(generate_response(query))
    
    
    # TODO 
    # CASO 1 (OBLIGATORIO)
    # generar otra funcion (tool) que se encargue de devolver los datos del usuario autenticado
    # usar encriptacion para asegurar seguridad
    # probar utilizar langchain para el manejo de los tools correspondientes
    # 
    # CASO 2 (OPCIONAL)
    # implementar lo mismo que la vtuber ai de speech to text 
    # conectarlo con la funcionalidad principal de LLMs
    # asegurar que la conexion se reestablezca en caso de desconectarse