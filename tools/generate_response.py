from utils.retrieve_embedding import retrieve_embedding
import ollama

def generate_response(query):
    data = retrieve_embedding(query)

    prompt = f"""
        Siempre debes responder en español.
        Eres un asistente que responde SOLO con base en el CONTEXTO proporcionado.
        Debes responder de forma simple y clara, fácilmente entendible a la siguiente pregunta {query}
        Limita tu respuesta a lo que está en CONTEXTO.
        CONTEXTO: {data}
        Si hay pasos/fechas/números, sé preciso.
        Debes hablar de forma natural, como si se tratara de una conversación humana con el cliente, ayudandolo en 
        todo lo que necesite.
    """

    output = ollama.generate(
    model="llama3.1",
    prompt=prompt,
    stream=False
    )
    return output['response']