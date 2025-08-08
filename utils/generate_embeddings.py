from .clean_text import load_clean_chunks

import chromadb
import ollama

def generate_embeddings():
    client = chromadb.PersistentClient(path="./data")
    collection = client.create_collection(name="docs")

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