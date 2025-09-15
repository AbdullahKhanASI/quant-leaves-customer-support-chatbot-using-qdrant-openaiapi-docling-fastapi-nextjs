# Local Development Guide (Sprint 0)

## Prerequisites
- Python 3.11+ managed via `uv`
- Node.js 20+ with `pnpm`
- Local Postgres instance with `pgvector` extension (can be installed later in Sprint 1)

## Backend Setup
```bash
cd backend
UV_CACHE_DIR=../.uv-cache uv venv
source .venv/bin/activate
UV_CACHE_DIR=../.uv-cache uv sync
cp .env.example .env  # then edit with real secrets before running ingestion
uv run uvicorn app.main:app --reload
```

## Frontend Setup
```bash
cd frontend
pnpm install
pnpm dev
```

## Ingestion (run after configuring backend/.env)
```bash
cd backend
uv run python -m ingest
```

## Docker Services
```bash
docker compose up -d  # starts Postgres with pgvector
```
If Docker is not running, launch Docker Desktop first.
