import os
from sentence_transformers import SentenceTransformer
import chromadb
from docx import Document 

# Load model and Chroma
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = get_model()

client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="documind_docs")

# Directory where your .md and .txt files are stored
docs_dir = "./data_docs"



for filename in os.listdir(docs_dir):
    file_path = os.path.join(docs_dir, filename)

    if filename.endswith(".md") or filename.endswith(".txt"):
        with open(file_path, "r") as file:
            content = file.read()

    elif filename.endswith(".docx"):
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

    else:
        continue  # skip other file types

    # Same embedding + add to Chroma
    embedding = model.encode(content).tolist()
    collection.add(
        documents=[content],
        embeddings=[embedding],
        ids=[filename],
        metadatas=[{"source": filename}]
    )


print("✅ Markdown and text files embedded into DocuMind!")
