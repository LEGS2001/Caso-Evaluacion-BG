from .generate_embeddings import generate_embeddings

import chromadb
import ollama


def retrieve_embedding(query):
    client = chromadb.PersistentClient(path="./embeddings_data")
    collection = client.get_or_create_collection(name="docs")

    count = collection.count()
    if count == 0:
        print('Generando embeddings.')
        generate_embeddings()
    
    else:
        print('Generando embeddings.')

    qvec = ollama.embed(model="nomic-embed-text", input=[query])["embeddings"][0]

    results = collection.query(
    query_embeddings=[qvec],
    n_results=5
    )
    data = results['documents'][0][0]
    return data