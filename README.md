# 📚 AI Knowledge Assistant
### Turn your computer into a searchable knowledge base.

**Find the right document without remembering its filename.**

AI Knowledge Assistant is a local document discovery tool that lets you search across your files using natural-language questions. Instead of manually opening PDFs, Word documents, and text files, describe what you're looking for and retrieve relevant documents through semantic search.

Built with Python, Sentence Transformers, FAISS, and Streamlit, the project combines local document processing with an intuitive search interface.

---

## ✨ What It Does

🔎 **Search by meaning, not just keywords**  
Describe a topic in natural language and retrieve documents containing semantically relevant information.

📂 **Discover documents automatically**  
Scan permitted directories on your computer for supported document formats, without manually selecting each file.

📄 **Extract content from multiple formats**  
Read and process PDF, DOCX, and TXT files into searchable text.

🧠 **Generate local embeddings**  
Use Sentence Transformers to convert text into numerical vectors locally, without sending every document to an external embedding API.

⚡ **Search with FAISS**  
Store embeddings in a vector index and retrieve relevant text chunks through similarity search.

🗂️ **Reuse the saved index**  
Build the index separately and load it when launching the app, avoiding repeated document processing on every startup.

📝 **Understand your results**  
Display relevant excerpts and optionally generate concise explanations using the Gemini API.

🖥️ **Go straight to the file**  
View full file paths, open matching files, and locate them in Windows Explorer.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and document processing |
| Streamlit | Interactive search interface |
| Sentence Transformers | Local text embeddings |
| `all-MiniLM-L6-v2` | Embedding model |
| FAISS | Vector indexing and similarity search |
| PyPDF | PDF text extraction |
| python-docx | Word document text extraction |
| LangChain Text Splitters | Text chunking |
| Gemini API | Optional AI-generated summaries |
| NumPy | Numerical operations on embeddings |

---

## 🧠 How It Works

```text
Local Documents
      │
      ▼
Document Discovery
      │
      ▼
Text Extraction
(PDF · DOCX · TXT)
      │
      ▼
Text Chunking
      │
      ▼
Local Embeddings
(Sentence Transformers)
      │
      ▼
FAISS Vector Index
      │
      ▼
Saved Index + Metadata
      │
      ▼
Natural-Language Query
      │
      ▼
Query Embedding + Similarity Search
      │
      ▼
Ranked Document Results
      │
      ▼
Optional Gemini Summaries
      │
      ▼
Open File · Show Location
```

### Why this approach?

Traditional file searches often depend on filenames or exact keyword matches. Semantic search represents text as embeddings so that queries and document passages with related meanings can be matched even when their wording differs.

The document index is built separately from the Streamlit interface. This makes application startup faster and allows the saved index to be reused between searches.

---

## 📊 Current Project Results

| Metric | Result |
|---|---:|
| Documents indexed | 584 |
| Text chunks indexed | 36,863 |
| Embedding model | `all-MiniLM-L6-v2` |
| Embedding dimensions | 384 |
| Embedding generation | Local |
| Vector index | FAISS |

*These are results from the local indexing run. Retrieval quality has been tested with sample queries, including searches for ProSense research documents. A formal retrieval benchmark has not yet been established.*

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/iamimpeccable/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini (optional)

The local embedding and search pipeline does not require a Gemini API key. To enable AI-generated summaries, create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Use your own API key, keep `.env` out of version control, and never commit credentials.

### 5. Review document scanning settings

Before indexing, review the allowed scan root and excluded directories in `utils/file_scanner.py`. The scanner is designed for local use; only index directories you intend to search.

### 6. Build the document index

```bash
python build_index.py
```

This scans supported documents, extracts text, creates chunks and embeddings, and saves the index and metadata under `data/local_index/`.

The initial build can take several minutes depending on the number and size of documents and your hardware.

### 7. Launch the application

```bash
streamlit run streamlit_app.py
```

Enter a natural-language query and explore the matching documents.

> **Note:** The index is specific to the files available on the computer where it was built. Each user should build their own local index.

---

## 📁 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app.py
├── streamlit_app.py
├── build_index.py
├── requirements.txt
├── .gitignore
│
├── utils/
│   ├── chunker.py
│   ├── document_reader.py
│   ├── embeddings.py
│   ├── file_scanner.py
│   ├── indexer.py
│   ├── prompt_builder.py
│   ├── retriever.py
│   ├── search.py
│   └── load_documents.py
│
├── vector_store/
│   └── vector_store.py
│
└── data/
    └── local_index/  # Generated locally; excluded from Git
```

*The structure above highlights the main application modules. Some supporting files may vary as the project evolves.*

---

## 🔐 Privacy by Design

- Document text embeddings are generated locally.
- The FAISS index and metadata are stored on the user's machine.
- The local index contains extracted text chunks and file paths, so it should not be committed to a public repository.
- The `.env` file and API credentials must remain private.
- Gemini summaries, when enabled, send the selected retrieved excerpt to the Gemini API.
- Review scanner exclusions before indexing folders containing personal, confidential, or sensitive information.

Local embeddings reduce dependence on external embedding API requests; they do not automatically make every part of the application fully offline.

---

## 🧪 Testing

The project includes test scripts for core components such as:

- File discovery
- Document text extraction
- Index creation and persistence
- Semantic retrieval

Run individual tests from the project root, for example:

```bash
python test_file_scanner.py
python test_document_reader.py
python test_indexer.py
python test_search.py
```

Tests should be run in the project's configured virtual environment.

---

## 🗺️ Roadmap

- [ ] Improve retrieval ranking and reduce duplicate document results.
- [ ] Add incremental indexing for newly added or modified files.
- [ ] Support additional document formats, including PowerPoint.
- [ ] Add retrieval evaluation using precision@k, recall@k, and relevant test queries.
- [ ] Add a demo mode with sample documents.
- [ ] Improve document summaries and result explanations.
- [ ] Add filters by file type, folder, and modification date.

---

## 💡 What I Learned

Building this project provided hands-on experience with:

- Designing an end-to-end semantic search pipeline.
- Extracting and preprocessing text from real-world documents.
- Generating and storing local embeddings.
- Using FAISS for vector similarity search.
- Separating offline indexing from interactive application startup.
- Integrating optional LLM-generated summaries.
- Handling directory exclusions, persistent indexes, and local file operations.

---

## 👩‍💻 About

Built as a hands-on project exploring practical applications of embeddings, vector databases, semantic retrieval, and LLM-powered interfaces.

**Repository:** [AI Knowledge Assistant](https://github.com/iamimpeccable/AI-Knowledge-Assistant)

*From scattered files to searchable knowledge — one question at a time.* 🔍
