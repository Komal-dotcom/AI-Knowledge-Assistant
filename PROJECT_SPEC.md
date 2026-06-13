# Build an AI Knowledge Assistant (RAG-Based Document Question Answering System)

You are a senior AI software engineer. Build a production-quality AI Knowledge Assistant that allows users to upload PDF documents and ask questions about their contents using Retrieval-Augmented Generation (RAG).

## Project Objective

Develop a web application where users can:

1. Upload one or more PDF documents.
2. Extract and process document text.
3. Convert document chunks into vector embeddings.
4. Store embeddings in a vector database.
5. Ask natural language questions.
6. Retrieve relevant document chunks using semantic similarity search.
7. Generate context-aware answers using an LLM.
8. Display source references used to generate answers.

The system should minimize hallucinations by grounding all answers in retrieved document content.

---

## Tech Stack

Backend:

* Python 3.12+
* FastAPI
* LangChain
* ChromaDB (local vector database)
* Sentence Transformers Embeddings
* Google Gemini API (or OpenAI API)

Frontend:

* React + TypeScript
  OR
* Streamlit (if rapid development is preferred)

Database:

* ChromaDB

PDF Processing:

* PyMuPDF

Deployment:

* Docker
* Docker Compose

---

## Functional Requirements

### Document Upload

Users should be able to:

* Upload PDF files.
* Upload multiple PDFs.
* View uploaded documents.
* Delete uploaded documents.
* Re-index documents after upload.

Supported size:

* Up to 100 MB per document.

---

### PDF Processing Pipeline

When a document is uploaded:

1. Extract text.
2. Clean text.
3. Split text into chunks.

Chunk settings:

* Chunk size: 1000 characters.
* Chunk overlap: 200 characters.

Store:

* Document name.
* Chunk text.
* Chunk ID.
* Page number.
* Metadata.

---

### Embedding Generation

Generate embeddings for every chunk.

Requirements:

* Use Sentence Transformers.
* Cache embeddings.
* Avoid duplicate indexing.

Store all vectors in ChromaDB.

---

### Semantic Retrieval

For every user question:

1. Convert question into embedding.
2. Retrieve top 5 most relevant chunks.
3. Rank chunks by similarity score.
4. Pass retrieved context to the LLM.

---

### LLM Answer Generation

Generate answers only using retrieved context.

Prompt instructions:

* Never fabricate information.
* If information is unavailable, explicitly state:
  "The uploaded documents do not contain enough information to answer this question."
* Cite source document names.
* Cite page numbers.

---

### Chat Interface

Features:

* Chat-style UI.
* Question history.
* Previous conversation context.
* Clear chat button.
* Loading indicator.
* Error handling.

---

### Source Attribution

Every answer must display:

* Source document name.
* Page number.
* Retrieved text snippets.

Example:

Sources:

* OperatingSystems.pdf (Page 12)
* DatabaseNotes.pdf (Page 45)

---

### Dashboard

Display:

* Total documents uploaded.
* Total chunks indexed.
* Total embeddings stored.
* Number of questions asked.

---

## FastAPI Endpoints

POST /upload-document

POST /index-document

POST /ask-question

GET /documents

DELETE /document/{id}

GET /statistics

---

## Performance Requirements

Target Metrics:

* Support 50+ PDFs.
* Index 10,000+ chunks.
* Average query response time below 2 seconds.
* Retrieval of top 5 chunks.
* Concurrent user support.

---

## Folder Structure

project-root/

backend/

frontend/

vector_db/

uploads/

tests/

docker/

README.md

requirements.txt

docker-compose.yml

---

## Security

* Validate file types.
* Reject malicious uploads.
* Limit upload size.
* Sanitize inputs.
* Store API keys in environment variables.

---

## Testing

Create:

* Unit tests
* Integration tests
* API tests

Minimum:

* 80% code coverage.

---

## Deliverables

Provide:

1. Complete source code.
2. Well-structured architecture.
3. README with setup instructions.
4. Docker configuration.
5. API documentation.
6. Sample PDFs for testing.
7. Deployment guide.
8. Requirements file.

The final application should be production-ready, modular, scalable, maintainable, and suitable for showcasing on a software engineering resume.
