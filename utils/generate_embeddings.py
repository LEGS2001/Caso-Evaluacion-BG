from .clean_text import load_clean_chunks

import chromadb
import ollama


# posible cambio, que el embedding solamente sea el titulo del documento, y funcione como vínculo al archivo entero
# el cual se pasaría luego al LLM como contexto, en lugar de guardar todo el archivo como un embedding, para así
# talvez mejorar la precisión de la búsqueda

def generate_embeddings():
    client = chromadb.PersistentClient(path="./embeddings_data")
    collection = client.get_or_create_collection(name="docs")

    records = load_clean_chunks("questions", 700, 120)

    ids = [f"{r['title']}:{r['chunk_id']}" for r in records]
    docs = [r["chunk"] for r in records]

    resp = ollama.embed(model="nomic-embed-text", input=docs)
    vectors = resp["embeddings"]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=docs,
    )

()