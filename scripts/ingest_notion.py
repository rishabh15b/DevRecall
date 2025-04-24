from notion_client import Client
from sentence_transformers import SentenceTransformer
import chromadb

NOTION_API_KEY = "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"
PAGE_IDS = [
    "your-notion-page-id-1",
    "your-notion-page-id-2"
]

# Setup Notion + Chroma + model
notion = Client(auth=NOTION_API_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection("documind_docs")

def extract_text_from_blocks(blocks):
    texts = []
    for block in blocks:
        b_type = block["type"]
        if b_type in block and "text" in block[b_type]:
            for t in block[b_type]["text"]:
                texts.append(t["plain_text"])
    return "\n".join(texts)

for page_id in PAGE_IDS:
    blocks = notion.blocks.children.list(page_id)["results"]
    full_text = extract_text_from_blocks(blocks)
    embedding = model.encode(full_text).tolist()
    collection.add(
        documents=[full_text],
        embeddings=[embedding],
        ids=[page_id],
        metadatas=[{"source": "notion", "page_id": page_id}]
    )

print("✅ Notion docs embedded into DocuMind!")
