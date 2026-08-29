# 🧬 VectorDNA

> A local Retrieval-Augmented Generation (RAG) application for asking questions about Python documentation.

VectorDNA combines semantic search, vector databases, embeddings, and local LLM generation to retrieve relevant Python documentation and generate grounded answers.

The project runs locally using Qdrant, Sentence Transformers, Ollama, FastAPI, and Streamlit.

## ✨ Features

- 🔎 Semantic search over Python documentation
- 🧠 Sentence Transformer embeddings
- 🗄️ Qdrant vector database for document retrieval
- 🤖 Local LLM generation through Ollama
- ⚡ FastAPI REST API
- 🎨 Streamlit web interface
- 📚 Displays retrieved sources
- 📊 Shows similarity scores
- ⚙️ Centralized application configuration
- 💻 Local-first architecture

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │      :8501          │
                    └──────────┬──────────┘
                               │
                               │ POST /ask
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       :8000         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Generator      │
                    │                     │
                    │  Retrieval + LLM    │
                    └───────┬─────┬───────┘
                            │     │
                 ┌──────────┘     └──────────┐
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │     Qdrant      │        │     Ollama      │
        │ Vector Database │        │    Local LLM    │
        │     :6333       │        │     :11434      │
        └────────┬────────┘        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Sentence     │
        │   Transformers  │
        │    Embeddings   │
        └─────────────────┘
```

## 🔄 How VectorDNA Works

VectorDNA follows a Retrieval-Augmented Generation pipeline.

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Search Qdrant
      │
      ▼
Retrieve Top-K Documents
      │
      ▼
Build Context
      │
      ▼
Send Context + Question to Ollama
      │
      ▼
Generate Answer
      │
      ▼
Return Answer + Sources
```

### 1. User asks a question

For example:

```text
What is a Python decorator?
```

### 2. Query embedding

The question is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 3. Semantic retrieval

The query vector is compared against vectors stored in Qdrant.

The most relevant documentation chunks are retrieved based on semantic similarity.

### 4. Context construction

The retrieved documentation is combined with the user's question to create the context used for generation.

### 5. Local LLM generation

The context is sent to an LLM running locally through Ollama.

### 6. Response

VectorDNA returns the generated answer together with the documentation sources and similarity scores.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API |
| Streamlit | Web UI |
| Qdrant | Vector database |
| Sentence Transformers | Text embeddings |
| Ollama | Local LLM inference |
| Pydantic | Data validation |
| Pydantic Settings | Configuration management |

## 📁 Project Structure

```text
vector-dna/
│
├── src/
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── generation/
│   │   └── generator.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── vectordb/
│   │   ├── client.py
│   │   ├── ingest.py
│   │   └── setup.py
│   │
│   ├── ui/
│   │   └── app.py
│   │
│   └── embeddings.py
│
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Configuration

VectorDNA uses environment-based configuration.

Create a `.env` file in the project root:

```env
TOP_K=3

QDRANT_URL=http://localhost:6333

OLLAMA_URL=http://127.0.0.1:11434

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

Configuration is centralized in:

```text
src/config/settings.py
```

This allows the application to use consistent configuration values across different components instead of hard-coding them throughout the project.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sripilla/vector-dna.git
cd vector-dna
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Qdrant

VectorDNA uses Qdrant as its vector database.

The application expects Qdrant at:

```text
http://localhost:6333
```

Make sure Qdrant is running before starting the application.

You can verify the connection with:

```bash
curl http://localhost:6333
```

A successful response confirms that Qdrant is reachable.

## 🤖 Ollama

VectorDNA uses Ollama for local LLM inference.

The application expects Ollama at:

```text
http://127.0.0.1:11434
```

Make sure Ollama is installed and running.

You also need a local model.

For example:

```bash
ollama pull llama3.2
```

Check installed models:

```bash
ollama list
```

## 📚 Vector Database Setup

The Qdrant-related functionality is located in:

```text
src/vectordb/
```

The main components are:

- `client.py` — Qdrant client configuration
- `setup.py` — vector collection setup
- `ingest.py` — document ingestion

The ingestion pipeline converts documentation into embeddings and stores them in Qdrant for semantic retrieval.

## ⚡ Running the API

Start the FastAPI server from the project root:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 🎨 Running the UI

Open a second terminal and activate the virtual environment.

Then run:

```bash
streamlit run src/ui/app.py
```

The Streamlit interface will open in your browser.

The UI communicates with the FastAPI backend through the `/ask` endpoint.

## 🔌 API

### POST `/ask`

The `/ask` endpoint accepts a question and returns a generated answer with its retrieved sources.

### Request

```json
{
  "question": "What is a Python decorator?"
}
```

### Response

```json
{
  "question": "What is a Python decorator?",
  "answer": "A Python decorator is a function that returns another function, usually used to modify or extend the behavior of the original function.",
  "sources": [
    {
      "source": "glossary.txt",
      "section": "Glossary",
      "score": 0.69758683
    },
    {
      "source": "whatsnew/2.5.txt",
      "section": "PEP 309: Partial Function Application",
      "score": 0.6716892
    },
    {
      "source": "library/functools.txt",
      "section": "\"functools\" --- Higher-order functions and operations on callable objects",
      "score": 0.67039824
    }
  ]
}
```

## 🧠 Embeddings

VectorDNA uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model converts text into dense numerical vectors.

Embeddings are normalized before being stored or searched:

```python
vectors = self.model.encode(
    texts,
    normalize_embeddings=True,
)
```

This allows semantically similar pieces of documentation to be retrieved even when their wording is different.

## 🔎 Retrieval

The retrieval layer is implemented in:

```text
src/retrieval/retriever.py
```

The retriever:

1. Receives the user's question
2. Generates a query embedding
3. Searches Qdrant
4. Retrieves the most relevant documents
5. Returns the top-K results

The number of retrieved results can be configured using:

```env
TOP_K=3
```

## 🤖 Generation

The generation layer is implemented in:

```text
src/generation/generator.py
```

The generator combines:

```text
User Question
+
Retrieved Documentation
```

and sends the resulting context to the local LLM through Ollama.

This allows the generated answer to be grounded in the retrieved documentation.

## 🎨 User Interface

The Streamlit UI provides a simple interface for interacting with VectorDNA.

Users can:

- Enter a question
- Submit the question
- View the generated answer
- View retrieved documentation sources
- View similarity scores

Example workflow:

```text
Question
   │
   ▼
"How does asyncio work?"
   │
   ▼
VectorDNA
   │
   ├── Generate embedding
   │
   ├── Search Qdrant
   │
   ├── Retrieve relevant documentation
   │
   └── Generate answer with Ollama
   │
   ▼
Answer + Sources
```

## 🏠 Local-First Design

VectorDNA is designed around a local RAG architecture.

```text
                 LOCAL MACHINE

┌────────────┐
│ Streamlit  │
│   :8501    │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  FastAPI   │
│   :8000    │
└─────┬──────┘
      │
      ├───────────────┐
      ▼               ▼
┌────────────┐  ┌────────────┐
│   Qdrant   │  │   Ollama   │
│   :6333    │  │   :11434   │
└────────────┘  └────────────┘
```

The core AI pipeline can therefore run locally without requiring a hosted LLM API.

## 📌 Current Scope

VectorDNA currently focuses on:

- Python documentation
- Semantic document retrieval
- Sentence Transformer embeddings
- Qdrant vector search
- Local LLM generation
- FastAPI REST API
- Streamlit interface
- Source attribution

The project intentionally keeps the architecture lightweight and focused on the core RAG workflow.

## 🔮 Future Improvements

Possible future improvements include:

- Better document chunking
- Improved retrieval ranking
- Metadata filtering
- Conversation history
- Streaming responses
- Additional document collections
- Better source previews
- Retrieval evaluation
- Generation evaluation
- Configurable models through the UI

## 🎯 Why VectorDNA?

VectorDNA demonstrates how a complete RAG application can be built from individual components.

Instead of treating RAG as simply:

```text
Documents → LLM
```

VectorDNA demonstrates the complete pipeline:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
Context Construction
    ↓
Local LLM
    ↓
Answer + Sources
```

This makes the project a practical demonstration of how modern retrieval-based AI applications are assembled.

## 👩‍💻 Development

The application is divided into a few focused components:

```text
config
    ↓
Application configuration

embeddings
    ↓
Text → vector conversion

vectordb
    ↓
Qdrant connection and ingestion

retrieval
    ↓
Semantic search

generation
    ↓
Context + LLM generation

api
    ↓
REST interface

ui
    ↓
Streamlit interface
```

The structure keeps the application modular without introducing unnecessary infrastructure.

## 📸 Screenshots

Add screenshots of the Streamlit interface here.

Example:

```text
docs/
└── screenshot.png
```

Then reference it in this section:

```markdown
![VectorDNA UI](docs/screenshot.png)
```

## 📜 License

This project is intended for learning, experimentation, and portfolio development.

Add an appropriate open-source license if the repository is later released under one.

---

# 🧬 VectorDNA

**Local RAG for Python documentation.**

Built with:

**FastAPI · Streamlit · Qdrant · Sentence Transformers · Ollama**