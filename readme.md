# 🧠 DocuMind — Semantic Memory for Engineering Teams

**DocuMind** is an AI-powered assistant that captures and recalls the reasoning behind your team’s technical decisions. It ingests pull requests, documentation, and GitHub issues, then allows developers to search across all of it using natural language — like having a memory layer for your codebase.

---

## 🚀 Key Features

- 🔍 **Semantic Search** over:
  - GitHub Pull Requests
  - Markdown, TXT, DOCX (Google Docs exported)
  - GitHub Issues

- 📚 **Reasoning Memory**
  - Understand *why* a decision was made, not just *what* was done

- 🧠 **Local LLM Embeddings**
  - Uses `MiniLM` with `SentenceTransformers`
  - No API cost, runs fully offline

- ⚡ **Fast & Lightweight**
  - Built with Streamlit, ChromaDB, and LangChain-ready
  - Perfect for local use, pitching, or internal team tools

---

## 💡 Example Queries

- “Why did we migrate to PostgreSQL?”
- “What decision was made in issue #45?”
- “Where is the reasoning behind the auth flow rewrite?”
- “What were the alternatives to Firebase?”

---

## 📦 Installation

```bash
# Clone this repo
git clone https://github.com/your-username/documind.git
cd documind

# Setup environment (recommended: conda)
conda create -n documind python=3.10 -y
conda activate documind

# Install dependencies
pip install -r requirements.txt

---

## 🛠️ How It Works

- Ingests GitHub PRs, issues, and local docs (.md, .txt, .docx)
- Embeds them using sentence-transformers (MiniLM)
- Stores them in ChromaDB vector database
- Enables semantic querying via Streamlit UI

```
---

## 📁 Folder Structure

``` documind/ 
├── data_docs/ # Place .md, .txt, .docx files here 
├── scripts/ 
│ ├── ingest_github.py 
│ ├── ingest_markdown.py 
│ └── ingest_github_issues.py 
├── streamlit_app.py # Main Streamlit UI 
├── requirements.txt └── README.md 

```

---

## ✨ Coming Soon

- 🔄 Unified search across all sources
- 🧠 Local summarizer agent
- 🖼️ Styled UI with result tagging and filters

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

