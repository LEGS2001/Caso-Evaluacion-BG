# se podría utilizar como un Tool en langchain o alguna otra librería para que el LLM detecte automáticamente cuando el usuario
# pide revisar sus datos

# devuelve, cuentas, tarjetas, y polizas
def get_client_data(user):
    return {
        'cuentas': user['cuentas'],
        'tarjetas': user['tarjetas'],
        'polizas': user['polizas']
    }