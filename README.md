# 🧠 AI Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application built with Python, LangChain, Google Gemini, and vector embeddings. The assistant retrieves relevant information from a document collection and generates accurate, context-aware responses using a Large Language Model (LLM).

---

## 🚀 Features

- Semantic document search using embeddings
- Retrieval-Augmented Generation (RAG)
- Google Gemini integration
- Modular project architecture
- Document chunking
- Vector-based retrieval
- Command-line interface
- Easily extendable for PDFs, local folders, and web applications

---

## 🛠 Tech Stack

- Python
- LangChain
- Google Gemini API
- Vector Embeddings
- FAISS / Vector Store
- python-dotenv

---

## 📂 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── documents/
│       ├── docker.txt
│       ├── fastapi.txt
│       └── langchain.txt
│
├── utils/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── load_documents.py
│   ├── prompt_builder.py
│   └── retriever.py
│
└── vector_store/
    └── vector_store.py
```

---

## ⚙️ How It Works

1. Load documents
2. Split documents into chunks
3. Generate embeddings
4. Store embeddings in a vector store
5. Retrieve the most relevant chunks
6. Send retrieved context to Gemini
7. Generate an answer grounded in the retrieved documents

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Knowledge-Assistant.git
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run

```bash
python app.py
```

---

## 💬 Example Questions

- What is LangChain?
- Explain Docker.
- What is FastAPI?
- Compare Docker and FastAPI.

---

## 🎯 Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- LLM Integration
- Vector Embeddings
- Semantic Search
- Modular Python Development
- API Integration
- Git & GitHub

---

## 🔮 Future Improvements

- PDF support
- Local folder indexing
- Chat memory
- FastAPI backend
- Streamlit web interface
- Multi-agent workflow
- MCP integration
- Persistent vector database

---

## 👩‍💻 Author

Vasudha Pasumarthy
