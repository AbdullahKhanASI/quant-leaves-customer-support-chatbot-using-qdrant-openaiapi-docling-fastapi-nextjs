# QuantLeaves Support RAG Backend

Sprint 0 scaffolding for the FastAPI + LangChain service powering the customer support chatbot.

## Structure
- `app/` — application package
  - `api/routes/` — FastAPI routers (`chat`, `ingest`, `health`)
  - `core/` — shared configuration, filesystem paths, logging utilities
  - `db/` — SQLAlchemy models and session helpers
  - `ingestion/` — corpus loaders and the hybrid ingestion pipeline
  - `retrieval/` — structured, vector, and hybrid retrievers
  - `services/` — application services (chat orchestration, ingestion wrapper)
  - `models/` — Pydantic schemas for API requests/responses
  - `utils/` — shared helpers (reserved for future usage)
- `corpus/` — first-party knowledge sources consumed by the pipeline
- `tests/` — pytest suite (currently smoke tests during Sprint 0)

## Local Development
```bash
cd backend
UV_CACHE_DIR=../.uv-cache uv venv
source .venv/bin/activate
UV_CACHE_DIR=../.uv-cache uv sync
cp .env.example .env  # add real OpenAI + Postgres credentials before running ingestion
uv run uvicorn app.main:app --reload
```

### Ingest the Corpus (after configuring `.env`)
```bash
uv run python -m ingest
```

`OPENAI_API_KEY` and `DATABASE_URL` must be set in `.env` before running ingestion. The ingestion job creates/updates structured tables, parses markdown + PDFs with Docling, generates embeddings with OpenAI, and stores them in Postgres/pgvector. Avoid running ingestion until valid credentials are supplied.
