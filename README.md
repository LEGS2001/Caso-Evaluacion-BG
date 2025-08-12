# Caso de Evaluación: WhatsApp Chatbot Assistant

Este proyecto consiste en un Asistente Virtual en forma de chatbot que cumple con la función de asistir al cliente respondiendo a las dudas que pueda llegar a tener.

## Funciones
- Ayudar al usuario a resolver una duda que tenga por medio de los FAQs extraídos de la página web.
- Darle al usuario sus datos de: tarjetas, cuentas, y pólizas

## Requerimientos
- Python 3.13
- pip o uv (cualquiera de las dos funciona)
- Ollama (llama3.1 y nomic-embed-text)

## Instalación

### Opción 1: Usando UV
- Instalar librerías (uv sync)
- Abrir Ollama e instalar los modelos 
    - llama pull llama3.1
    - llama pull nomic-embed-text
- Correr el programa (uv run main.py)

### Opción 2: Usando pip
- Crear un ambiente virtual (python -m venv venv)
- Abrir Ollama e instalar los modelos 
    - llama pull llama3.1
    - llama pull nomic-embed-text
- Instalar librerías y dependencias (pip install -r requirements.txt)
- Correr el programa (python main.py)