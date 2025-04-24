import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
import requests
from github import Github
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# --- Page Settings ---
st.set_page_config(page_title="DevRecall", layout="wide")
st.title("🧠 DevRecall")
st.markdown("#### 💡 DevRecall helps you rediscover the 'why' behind engineering decisions — across code, docs, and issues.")

# --- Sidebar Upload + Navigation ---
# Local Doc Upload (moved to sidebar)
st.sidebar.subheader("📄 Upload Local Docs")
uploaded_files = st.sidebar.file_uploader("Upload .txt, .md, .docx", type=["txt", "md", "docx"], accept_multiple_files=True)
if uploaded_files:
    col = client.get_or_create_collection("devrecall_docs")
    for file in uploaded_files:
        file_bytes = file.read()
        text = ""
        filetype = os.path.splitext(file.name)[-1].lower()
        if filetype == ".txt":
            text = file_bytes.decode("utf-8")
        elif filetype == ".md":
            text = file_bytes.decode("utf-8")
        elif filetype == ".docx":
            import docx
            from io import BytesIO
            doc = docx.Document(BytesIO(file_bytes))
            text = "".join([p.text for p in doc.paragraphs])
        else:
            st.sidebar.warning(f"Unsupported file type: {file.name}")
            continue

        base_id = file.name.replace(" ", "_")
        chunk_and_embed(text, model, col, base_id, {"source": "Doc", "filetype": filetype, "label": "upload", "url": f"Uploaded: {file.name}"})
    st.sidebar.success("✅ Docs uploaded and embedded.")
st.sidebar.title("🧠 DevRecall")
st.sidebar.markdown("Navigate:")
st.sidebar.markdown("- 🔁 PRs")
st.sidebar.markdown("- 📄 Docs")
st.sidebar.markdown("- 🐞 Issues")
st.sidebar.markdown("- 🧠 Unified Search")

# --- Load model ---
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()
client = chromadb.PersistentClient(path="./chroma")

# --- Chunking Helper ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def chunk_and_embed(text, model, collection, base_id, metadata):
    chunks = text_splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        chunk_meta = metadata.copy()
        chunk_meta["chunk_index"] = i
        chunk_meta["chunk_total"] = len(chunks)
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{base_id}_{i}"],
            metadatas=[chunk_meta]
        )

# --- Step 1: GitHub Token ---
st.markdown("### 🚀 Step 1: Connect to GitHub")
token = st.text_input("🔐 GitHub Token (optional)", type="password", help="Used for private repos or rate limit boost", max_chars=40)
g = Github(token.strip()) if token.strip() else Github()

# --- Step 2: Fetch GitHub Data and Upload Local Docs ---
st.markdown("### 📥 Step 2: Fetch PRs and Issues")

st.subheader("📥 Fetch GitHub Issues")
issue_repo_name = st.text_input("GitHub repo for Issues (e.g. user/repo)")
if st.button("Fetch Issues"):
    try:
        repo = g.get_repo(issue_repo_name)
        issues = repo.get_issues(state="all")[:10]
        col = client.get_or_create_collection("devrecall_custom_issues")
        for i in issues:
            content = f"{i.title}\n{i.body or ''}"
            chunk_and_embed(content, model, col, f"{issue_repo_name}_{i.number}", {"url": i.html_url, "label": "issue", "source": "Issue", "filetype": ".md"})
        st.success("✅ Issues fetched and embedded.")
    except Exception as e:
        st.error(str(e))

st.subheader("📥 Fetch GitHub Pull Requests")
pr_repo_name = st.text_input("GitHub repo for PRs (e.g. user/repo)")
if st.button("Fetch PRs"):
    try:
        repo = g.get_repo(pr_repo_name)
        prs = repo.get_pulls(state="all")[:10]
        col = client.get_or_create_collection("devrecall_custom_prs")
        for pr in prs:
            content = f"{pr.title}\n{pr.body or ''}"
            chunk_and_embed(content, model, col, f"{pr_repo_name}_{pr.number}", {"url": pr.html_url, "label": "pr", "source": "PR", "filetype": ".md"})
        st.success("✅ PRs fetched and embedded.")
    except Exception as e:
        st.error(str(e))

# --- Step 3: Unified Search ---
st.markdown("### 🧠 Step 3: Ask Questions with Unified Semantic Search")

# --- Local Doc Upload ---
# (Moved to sidebar above)
query = st.text_input("🔍 Ask a question across PRs, Docs, and Issues:")

source_filter = st.multiselect("Filter by Source Type", ["PR", "Doc", "Issue"], default=["PR", "Doc", "Issue"])
filetype_filter = st.selectbox("Filter by File Type", ["All", ".md", ".docx", ".txt"])

if st.button("Search All") and query:
    query_vec = model.encode(query).tolist()
    results = []

    def search_collection(name, label):
        try:
            col = client.get_collection(name)
            r = col.query(query_embeddings=[query_vec], n_results=5)
            for doc, meta in zip(r['documents'][0], r['metadatas'][0]):
                if meta.get("source") not in source_filter:
                    continue
                if filetype_filter != "All" and meta.get("filetype") != filetype_filter:
                    continue
                chunk_info = f" (Chunk {meta.get('chunk_index') + 1} of {meta.get('chunk_total')})" if meta.get("chunk_index") is not None else ""
                results.append((label + chunk_info, doc, meta))
        except:
            pass

    search_collection("devrecall_custom_prs", "🔁 PR")
    search_collection("devrecall_docs", "📄 Doc")
    search_collection("devrecall_custom_issues", "🐞 Issue")

    for label, doc, meta in results:
        st.markdown(f"**{label}**\n\n{doc[:400]}...")
        with st.expander("🔎 Show Full Chunk"):
            st.write(doc)
            if meta.get("url"):
                st.markdown(f"[🔗 View Source]({meta.get('url')})")
            st.caption(f"Chunk {meta.get('chunk_index') + 1} of {meta.get('chunk_total')}")
        st.markdown("---")
