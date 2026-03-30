# AI Contract Intelligence

This project is a modular, scalable AI Document Intelligence System that processes PDF documents (like contracts), extracts structured data, generates embeddings, performs risk analysis, and provides semantic search capabilities using RAG (Retrieval-Augmented Generation).

## Architecture & Flow

The application follows a typical robust FastAPI architecture using Celery for background processing and `pgvector` for semantic search.

1. **Upload & Ingestion (`/api/v1/documents/upload`)**:
   - User uploads a PDF document via the API.
   - The file is temporarily saved to disk, and a background task is triggered using **Celery** (`app.workers.tasks.process_document`).
   - The API immediately responds with "Processing started".

2. **Background Processing (`app.services.ingestion` & `app.services.embedding`)**:
   - The Celery worker extracts the text from the PDF using `PyMuPDF`.
   - The text is chunked into overlapping segments (e.g., 500 characters, 50 overlap) to preserve context.
   - Each chunk generates an embedding vector via the OpenAI API (`text-embedding-3-small`).
   - The chunks and embeddings are stored in PostgreSQL using the `pgvector` extension.

3. **Query & Retrieval (RAG) (`/api/v1/query/ask`)**:
   - When a user asks a question about the contract, the query itself is embedded using OpenAI.
   - A cosine similarity semantic search (`app.services.retriever`) is performed in PostgreSQL (`pgvector`) to find the most relevant document chunks.
   - The retrieved context + the user query form a prompt tailored for a legal AI assistant.
   - The system calls an LLM (`gpt-4o-mini`) to generate a specialized response containing risk levels, issues, and recommendations.

## Directory Structure

```text
├── app
│   ├── api/v1
│   │   ├── endpoints         # Route handlers logic
│   │   │   ├── auth.py       # JWT authentication routes
│   │   │   ├── documents.py  # File upload endpoints
│   │   │   └── query.py      # RAG and QA endpoints
│   │   └── router.py         # Main router aggregating all v1 routes
│   ├── core
│   │   ├── config.py         # Type-safe environment configs using Pydantic Settings
│   │   ├── rate_limiter.py   # Outlines API rate-limiting structure
│   │   └── security.py       # Handles JWT token creation and verification
│   ├── db
│   │   ├── base.py           # SQLAlchemy declarative base
│   │   ├── models            # Application database schemas
│   │   │   ├── document.py   # Raw document meta/data DB model
│   │   │   └── embedding.py  # Document pgvector embedding chunks model 
│   │   └── session.py        # SQLAlchemy engine and session generation logic
│   ├── services              # Reusable standalone logic without FastAPI coupling
│   │   ├── embedding.py      # OpenAI embeddings logic
│   │   ├── ingestion.py      # PyMuPDF processing and chunking
│   │   ├── llm.py            # Chat GPT wrappers for generative RAG
│   │   ├── rag.py            # Aggregates retrieval and generation (The RAG flow)
│   │   └── retriever.py      # Executes pgvector semantic searches
│   ├── workers
│   │   └── tasks.py          # Celery configuration and async task definition
│   └── main.py               # FastAPI application initialization
├── .env                      # Contains secrets (e.g., OPENAI_API_KEY)
├── docker-compose.yml        # Multi-container local orchestration
├── Dockerfile                # API & Worker app containerization
└── requirements.txt          # Python dependencies
```

## Running the Project Locally

1. **Set your keys**:
   Update the `.env` file with your actual `OPENAI_API_KEY`.

2. **Start the services via Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   This will bring up:
   - `api`: The FastAPI server on port 8000.
   - `worker`: The Celery background worker.
   - `redis`: The message broker for Celery.
   - `db`: The PostgreSQL database with `pgvector` installed.

3. **Database Migrations** (For production use, you should run Alembic):
   Since this uses a generic structure, tables should be pushed to PostgreSQL.
   A basic method to test the app is simply letting SQLAlchemy run `Base.metadata.create_all(bind=engine)` inside `main.py` if no migrations are configured, but typically Alembic handles this.

4. **Access the Application**:
   - **Swagger Docs**: Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to explore and test the endpoints.
