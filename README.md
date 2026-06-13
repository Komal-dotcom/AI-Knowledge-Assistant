# AI Knowledge Assistant

A RAG-based document question answering system. Users upload PDF documents, the system indexes them into a vector store, and answers natural language questions with source attribution.

> **Status:** Phase 0 — project skeleton only. RAG pipeline not yet implemented.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12+, FastAPI |
| Vector DB | ChromaDB *(upcoming)* |
| Embeddings | Sentence Transformers *(upcoming)* |
| LLM | Google Gemini / OpenAI *(upcoming)* |
| PDF Processing | PyMuPDF *(upcoming)* |
| Frontend | React + TypeScript *(upcoming)* |
| Deployment | Docker, Docker Compose *(upcoming)* |

## Project Structure

```
AI-Knowledge-Assistant/
├── backend/
│   └── app/
│       ├── api/          # REST route modules
│       ├── core/         # Shared utilities
│       ├── config.py     # Environment-based settings
│       └── main.py       # FastAPI application entry point
├── uploads/              # Uploaded PDF storage (gitignored contents)
├── vector_db/            # ChromaDB persistence (gitignored contents)
├── tests/                # Unit, integration, and API tests
├── requirements.txt
├── .env.example
└── PROJECT_SPEC.md
```

## Prerequisites

- Python 3.12 or newer
- pip

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd AI-Knowledge-Assistant
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` as needed. Defaults work for local development.

## Run the API

From the project root:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=backend --cov-report=term-missing
```

## Roadmap

1. **Phase 0** — Project skeleton *(current)*
2. **Phase 1** — Document upload, list, delete
3. **Phase 2** — PDF ingestion pipeline (extract, chunk, embed, index)
4. **Phase 3** — RAG query engine with LLM
5. **Phase 4** — Chat UI and dashboard
6. **Phase 5** — Production hardening, Docker, 80% test coverage

See [PROJECT_SPEC.md](PROJECT_SPEC.md) for full requirements.
