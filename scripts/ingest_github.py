from github import Github
from sentence_transformers import SentenceTransformer
import chromadb

# GitHub setup (no token needed for public repos)
g = Github()
repo = g.get_repo("psf/requests")  # You can change this later
pulls = repo.get_pulls(state='closed', sort='updated')[:5]

# Local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ChromaDB local setup
client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="devrecall_prs")

# Ingest PRs into Chroma
for i, pr in enumerate(pulls):
    content = f"Title: {pr.title}\n\n{pr.body or 'No description'}"
    embedding = model.encode(content).tolist()
    collection.add(
        documents=[content],
        ids=[f"pr_{i}"],
        embeddings=[embedding],
        metadatas=[{"url": pr.html_url}]
    )

print("✅ Ingested PRs into devrecall.")
