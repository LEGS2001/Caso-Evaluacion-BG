import chromadb
import ollama


def retrieve_embedding(query):
    client = chromadb.PersistentClient(path="./data")
    collection = client.get_or_create_collection(name="docs")

    qvec = ollama.embed(model="nomic-embed-text", input=[query])["embeddings"][0]

    results = collection.query(
    query_embeddings=[qvec],
    n_results=3
    )
    data = results['documents'][0][0]
    return data