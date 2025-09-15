# QuantLeaves SaaS Analytics Support Chatbot — Delivery Plan

## Objectives
- Provide QuantLeaves support agents and customers with a reliable chat assistant that can answer product, policy, and troubleshooting questions using first-party content.
- Implement a Retrieval-Augmented Generation (RAG) service that combines structured data keyword lookup with vector similarity search over PDF and markdown knowledge sources.
- Expose the RAG service through FastAPI endpoints consumed by a Next.js frontend, powered by LangChain orchestration and OpenAI APIs for embeddings and response generation.

## Knowledge Corpus Overview
- **Structured sources** (`corpus/structured/error_codes.json`, `plan_matrix.csv`, `products.csv`, `world_bible.json` slices) provide authoritative facts such as limits, pricing, entitlements, API metadata, and product compatibility.
- **Operational references** (`corpus/kb/*.md`, `corpus/runbooks/*.md`, `corpus/policies/*.md`, `corpus/macros/*.md`) contain YAML front-matter metadata and procedural guidance to ground responses.
- **API schema** (`corpus/api/openapi.yaml`) defines endpoints, auth, and rate limits that must be queryable.
- **Evaluation set** (`corpus/eval/eval_questions.json`) drives regression tests for factual accuracy.
- **PDF manuals** (e.g., `backend/test_files/the-illusion-of-thinking.pdf` in the companion workspace) include YAML metadata blocks followed by unstructured prose; these must be parsed with Docling so metadata is preserved in embeddings and retriever filters.

## Target Architecture
- **Ingestion layer**
  - Build a Docling-based loader for PDFs that extracts YAML metadata + body text into LangChain `Document` objects with structured metadata fields.
  - Implement dedicated parsers for markdown (respecting existing YAML front-matter), JSON, and CSV assets, normalizing metadata (doc_id, doc_type, audience, product_scope, effective_date).
  - Store structured tables (`plan_matrix`, `products`, `error_codes`, `world_bible` slices) in Postgres schemas for keyword + attribute filtering; surface a lightweight data-access layer for the retriever to run `ILIKE` and equality filters.
  - Persist unstructured chunks in a `pgvector` or compatible vector store (Supabase/Postgres) with OpenAI embedding vectors and searchable metadata facets (doc_type, product_scope, audience, region_scope, version).
- **Retrieval strategy**
  - Hybrid search orchestrator queries Postgres keyword tables first for exact matches (e.g., plan limits, error codes, SLA rules) and uses LangChain's `SelfQueryRetriever` to combine with vector similarity over the chunked unstructured corpus.
  - Ensure YAML metadata fields from PDFs and markdown are indexed to support filtering (e.g., doc_type=policy, audience=public).
  - Enrich retrieved chunks with citations (doc_id, title) for grounding in the chat response.
- **LLM generation**
  - Use OpenAI `gpt-4o` or `gpt-4.1` for response synthesis with a template that enforces step-by-step grounding and refusal policy when data is missing.
  - Apply response post-processing to produce agent-friendly formatting (bullet lists, stepwise instructions) and include references to authoritative sources.
- **Backend (FastAPI)**
  - Expose endpoints: `POST /chat` (interactive RAG), `POST /ingest` (admin re-index), `GET /health`.
  - Implement async pipeline orchestrating retrieval + generation, streaming tokens to the frontend when possible (Server-Sent Events or WebSockets).
  - Provide dependency-injected services for embeddings, vector store, structured lookup, and Docling ingestion workers.
- **Frontend (Next.js)**
  - Build a chat UI with citation callouts, follow-up suggestions, and metadata filters (audience, products).
  - Offer admin-only pages for ingestion status and evaluation dashboard.
  - Integrate with FastAPI via `/api` routes, handling streaming responses and error states gracefully.
- **Observability & Ops**
  - Capture RAG trace metadata (retrieved documents, latency) via LangChain callbacks and forward to monitoring (OpenTelemetry or LangSmith).
  - Log structured analytics for evaluation coverage and model cost tracking.

## Implementation Milestones
1. **Foundation & Environment** (Week 1)
   - Confirm Python (3.11) and Node (20+) toolchains, set up repo structure with `backend/` and `frontend/` workspaces.
   - Provision Postgres with pgvector extension locally and define `.env` contract for API keys and DB credentials.
   - Validate access to OpenAI APIs and Docling installation.
2. **Corpus Ingestion** (Weeks 1-2)
   - Implement loaders for markdown + YAML front-matter, CSV, JSON, and OpenAPI to normalized schemas.
   - Build Docling ingestion job for PDFs, ensuring YAML metadata is parsed into structured fields.
   - Create ETL scripts to push structured data into Postgres tables and chunk unstructured docs into the vector store.
   - Unit-test parsers against existing corpus (KB, runbooks, policies, macros, PDF sample).
3. **Hybrid Retrieval Service** (Weeks 2-3)
   - Implement LangChain retriever composition (keyword SQL retriever + vector retriever) with configurable weighting.
   - Add guardrails for doc freshness (effective_date) and permission filtering (`audience`, `region_scope`, `product_scope`).
   - Build FastAPI services for ingestion refresh and chat inference, including streaming support.
   - Cover retrieval and grounding logic with integration tests using eval questions.
4. **Chat Experience (Frontend)** (Weeks 3-4)
   - Develop Next.js chat interface with streaming responses, citation chips, and follow-up question suggestions.
   - Provide admin view for triggering re-ingest and viewing evaluation results.
   - Add authentication stub (e.g., Clerk/Auth0 placeholder) to gate internal tools.
5. **Evaluation & Hardening** (Weeks 4-5)
   - Automate regression evaluation leveraging `corpus/eval/eval_questions.json` via LangChain Evaluate.
   - Configure load tests for concurrency, measure latency budgets (<3s first token, <10s full response).
   - Instrument observability, add alerting for ingestion failures and OpenAI quota breach.
   - Prepare deployment artifacts (Dockerfiles, Helm or Terraform skeleton) for staging.
6. **Launch & Iterate** (Week 6)
   - Conduct UAT with support team, gather feedback, refine prompts and retrieval weightings.
   - Document runbooks for ingestion, deployment, fallback modes, and on-call support.

## Evaluation & Quality Gates
- Daily automated eval run covering all 20 questions in `corpus/eval/eval_questions.json`; target ≥90% exact/fuzzy match rate.
- Manual spot checks for new corpus additions before publishing to production index.
- Synthetic user journeys (reset password, rate limits, billing) executed via Playwright and backend contract tests.
- Performance SLOs: P95 retrieval < 800ms, P95 total response < 6s, Streaming first token < 2s.

## Risks & Mitigations
- **Embedding cost or latency spikes**: cache embeddings, batch requests, and enable local fallback encoder for development.
- **Docling parsing variance on complex PDFs**: add regression fixtures; log parse warnings and fallback to manual QA for malformed metadata blocks.
- **Drift between structured truth tables and markdown guidance**: implement nightly diff checks between `world_bible` and Postgres tables; flag discrepancies to content ops.
- **OpenAI API limits**: implement exponential backoff, retry budgets, and queueing; keep model selection configurable.
- **Security & PII concerns**: enforce audience/product filters before returning content; stub redaction pipeline to sanitize transcripts before analytics storage.

## Dependencies & Assumptions
- Access to OpenAI API keys and the ability to store minimal chat transcripts for analytics.
- Ability to deploy Postgres + pgvector in target environment (or equivalent managed service).
- Next.js app will be hosted alongside FastAPI (e.g., Vercel + cloud API) with shared authentication provider.
- Engineering team can provision CI pipeline (GitHub Actions) for tests, linting, and evaluations prior to merge.
