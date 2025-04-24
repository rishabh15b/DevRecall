import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

# ✅ Page config should be first
st.set_page_config(page_title="DocuMind", layout="wide")

# ✅ New ChromaDB Client
client = chromadb.PersistentClient(path="./chroma")

# ✅ Load the model once using cache
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

st.title("DocuMind – Semantic Memory for Engineering Teams")

# ✅ Optional: Add sidebar navigation (good for demos)
st.sidebar.title("🔎 DocuMind Navigation")
st.sidebar.markdown("- Search PRs")
st.sidebar.markdown("- Search Docs")
st.sidebar.markdown("- Search Issues")

# --- GitHub PR Query Section ---
st.header("Search GitHub Pull Requests")
query = st.text_input("Ask something about your codebase or decisions:", placeholder="Why did we change the database?")
if st.button("Search") and query:
    query_vec = model.encode(query).tolist()
    collection = client.get_or_create_collection(name="documind_prs")
    results = collection.query(query_embeddings=[query_vec], n_results=5)

    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        st.markdown("### Result")
        st.write(doc[:500] + "...")
        st.markdown(f"[View on GitHub]({meta['url']})")
        st.divider()

# --- Divider ---
st.markdown("---")

# --- Documentation Query Section ---
st.header("Search Documentation")
query_docs = st.text_input("Ask a question about internal documentation:", key="doc_query")
if st.button("Search Docs"):
    query_vec = model.encode(query_docs).tolist()
    doc_collection = client.get_or_create_collection(name="documind_docs")
    results = doc_collection.query(query_embeddings=[query_vec], n_results=3)

    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        st.markdown("### Result")
        st.write(doc[:500] + "...")
        st.markdown(f"Source: `{meta['source']}`")
        st.divider()

# --- Divider ---
st.markdown("---")

# --- GitHub Issues Search ---
st.header("Search GitHub Issues")
query_issues = st.text_input("Ask a question about project issues:", key="issue_query")
if st.button("Search Issues"):
    query_vec = model.encode(query_issues).tolist()
    issue_collection = client.get_or_create_collection(name="documind_issues")
    results = issue_collection.query(query_embeddings=[query_vec], n_results=3)

    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        st.markdown("### Issue Match")
        st.write(doc[:500] + "...")
        st.markdown(f"[View on GitHub]({meta['url']})")
        st.divider()
