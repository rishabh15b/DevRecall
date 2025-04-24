from github import Github
from sentence_transformers import SentenceTransformer
import chromadb

# Optional: set your token for private repos
g = Github()  # or Github("your-token-here")
repo = g.get_repo("psf/requests")  # Change to your own repo later
issues = repo.get_issues(state="all")[:10]

# Load model + vector store
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="devrecall_issues")

# Ingest issues
for i, issue in enumerate(issues):
    content = f"Issue Title: {issue.title}\n\n{issue.body or 'No description'}"
    embedding = model.encode(content).tolist()
    collection.add(
        documents=[content],
        embeddings=[embedding],
        ids=[f"issue_{issue.number}"],
        metadatas=[{"url": issue.html_url}]
    )

print("✅ GitHub Issues embedded into devrecall!")
