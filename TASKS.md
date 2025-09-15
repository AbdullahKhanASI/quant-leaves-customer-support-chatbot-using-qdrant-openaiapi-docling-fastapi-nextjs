# Task Backlog

## Sprint 0 – Foundations
- [x] Define repo structure (`backend/`, `frontend/`, `docs/`) and bootstrap tooling configs (Poetry/uv, pnpm/yarn, Ruff, Prettier).
- [x] Provision local Postgres with pgvector, create seed scripts for initial corpus load, and supply `.env.example` covering DB + OpenAI credentials. (DB provisioning doc placeholder; actual DB setup scheduled for Sprint 1)
- [x] Install Docling, LangChain, FastAPI, and Next.js dependencies; validate OpenAI connectivity with local smoke scripts (pending key).

## Data & Ingestion
- [x] Build markdown loader that preserves YAML front-matter (`doc_id`, `doc_type`, `audience`, `product_scope`, `effective_date`, `region_scope`).
- [x] Implement structured ETL to normalize `plan_matrix.csv`, `products.csv`, `error_codes.json`, and `world_bible.json` subsets into Postgres tables.
- [x] Create Docling PDF ingestion pipeline that extracts YAML metadata blocks + body text, chunking content with overlap and storing parsed metadata fields.
- [x] Build OpenAPI parser to convert `corpus/api/openapi.yaml` into retrievable text snippets and endpoint metadata records.
- [x] Add ingestion CLI (`python -m ingest`) with subcommands for full rebuild, incremental updates, and integrity validation. (incremental modes TBD).
- [ ] Write automated tests covering parsers against existing corpus fixtures (KB, policies, runbooks, macros, eval PDFs).

## Retrieval & RAG Service (Backend)
- [x] Configure OpenAI embedding model (e.g., `text-embedding-3-large`) and create vector store client (pgvector) with schema definitions.
- [x] Implement keyword retriever over structured tables (SQL `tsvector`/`ILIKE`) returning normalized facts (plans, limits, error codes).
- [x] Compose LangChain hybrid retriever that merges keyword and vector results, deduplicates by `doc_id`, and annotates citations.
- [x] Design prompt templates enforcing grounded responses, refusal policy, and citation format for FastAPI endpoints.
- [x] Build FastAPI services (`/chat`, `/ingest`, `/health`) with async pipeline, streaming support, and dependency injection for retrievers and LLM client. (streaming pending).
- [ ] Add local telemetry hooks (LangChain callbacks, structured logging) capturing retrieval candidates and latency metrics for debugging.

## Frontend (Next.js)
- [ ] Scaffold Next.js app with TypeScript, Tailwind (or design system), and SSR-compatible data fetching.
- [ ] Implement chat UI with streaming responses, citation pills, follow-up question suggestions, and feedback controls.
- [ ] Build admin dashboard for ingestion status, evaluation history, and manual re-index trigger.
- [ ] Integrate authentication/authorization guardrails (stub provider, role-based UI gating for agent-internal content).
- [ ] Add API service layer handling FastAPI endpoints, error retries, and client-side caching of structured lookup results.

## Local Quality & Validation
- [ ] Automate regression evaluation using `corpus/eval/eval_questions.json` with LangChain Evaluate; surface reports in the repo.
- [ ] Create unit/integration tests for FastAPI routes, retriever composition, and structured lookup fallbacks.
- [ ] Set up Playwright (or Cypress) tests for chat UX, including streaming success, error handling, and citation rendering.
- [ ] Provide local scripts (`make test`, `npm run test`, etc.) to run linting, typing (`mypy`, `tsc`), tests, and evaluation suite.

## Developer Workflow (Local)
- [x] Document step-by-step local setup (`docs/local_dev.md`) covering environment variables, database migrations, ingestion runs, and how to start backend/frontend together. (DB migration stubs coming in Sprint 1)
- [ ] Add convenience scripts (`make dev`, `pnpm dev`, `uvicorn` hot reload) for running FastAPI and Next.js concurrently with automatic reload.
- [ ] Capture troubleshooting guide for common local issues (missing pgvector, OpenAI key errors, Docling parse failures).
