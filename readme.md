# 🧠 DevRecall

> 💡 *Rediscover the “why” behind engineering decisions — across pull requests, internal docs, and issues.*

![DevRecall Banner](./assets/devrecall-banner.png)

DevRecall is a local-first AI memory assistant for engineering teams. It ingests your GitHub PRs, issues, and internal docs to let you semantically query project history and get context-rich answers — powered by local LLMs and vector search.

---

## 🚀 Features

- 🔁 **Ingest GitHub PRs and Issues** on demand
- 📄 **Upload internal docs** (`.txt`, `.md`, `.docx`)
- 🧠 **Semantic search across all sources** (Docs, PRs, Issues)
- 🔍 **Smart chunking** of long text for high-relevance matching
- 🎛 **Filter** by source type and file format
- 🔐 **Token-based GitHub access** for private repositories
- ✅ **Runs 100% locally** — no external API costs or data leaks

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Embeddings**: SentenceTransformers (`MiniLM`)
- **Vector Store**: ChromaDB (local)
- **Chunking**: LangChain
- **Ingestion**: GitHub API + local file parser
- **LLM** (Optional): Ollama + `llama3` (for summarization)

---

## 📁 Folder Structure

``` 
Devrecall/ 
├── data_docs/ # Place .md, .txt, .docx files here 
├── scripts/ 
│ ├── ingest_github.py 
│ ├── ingest_markdown.py 
│ └── ingest_github_issues.py 
│ ├── ingest_devrecall.py 
├── streamlit_app.py # Main Streamlit UI 
├── requirements.txt └── README.md 

```
- Scripts folder is optional now.
---

## 📦 Installation

```bash
# Clone this repo
git clone https://github.com/your-username/Devrecall.git
cd Devrecall

# Setup environment (recommended: conda)
conda create -n Devrecall python=3.10 -y
conda activate Devrecall

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠️ How It Works

- Ingests GitHub PRs, issues, and local docs (.md, .txt, .docx)
- Embeds them using sentence-transformers (MiniLM)
- Stores them in ChromaDB vector database
- Enables semantic querying via Streamlit UI

---

> ℹ️ All document and GitHub ingestion is handled inside the app — no need to run separate ingestion scripts manually.

## 📦 Setup Instructions

```bash
# 1. Install required dependencies
pip install -r requirements.txt

# 2. (Optional) Start your local LLM
ollama run llama3

# 3. Launch the app
streamlit run streamlit_app.py
```

---

## 💡 Example Queries

- “Why did we migrate to PostgreSQL?”
- “What decision was made in issue #45?”
- “Where is the reasoning behind the auth flow rewrite?”
- “What were the alternatives to Firebase?”

---

## 🌱 Planned Enhancements

- 🤖 LLM-powered summaries and Q&A using local Ollama
- 🧭 Interactive document explorer with full-chunk linking
- 🔄 GitHub PR timeline view with decision threads
- 🧩 Multi-user project mode with per-user storage
- 🌐 Qdrant migration for scalable vector search
- 📚 Exportable search insights and summaries (PDF, Markdown)

---

## 🙌 Contributing

- Feel free to fork and customize!
- Ideas, issues, or pull requests are welcome.

## 📜 License

- MIT License — free to use, modify, and share.

## 👨‍💻 Author

- Developed by [Rishabh Balaiwar](https://github.com/rishabh15b). Feel free to reach out for questions or collaboration opportunities!

---

## 📞 Contact

- For support or inquiries, contact me at:
- Email: <rbalaiwar@gmail.com>
- GitHub: [Your GitHub Profile](https://github.com/rishabh15b)

