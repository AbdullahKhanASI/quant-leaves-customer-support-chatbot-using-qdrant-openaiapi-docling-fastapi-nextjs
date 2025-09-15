# Project Rules & Conventions

## Architectural Guardrails
- RAG pipeline must combine SQL keyword lookups over structured truth tables with vector similarity retrieval over Docling-parsed PDFs and markdown sources; both retrievers run on every query unless explicitly disabled for diagnostics.
- Docling ingestion must retain YAML metadata fields from PDFs and markdown front-matter (`doc_id`, `doc_type`, `audience`, `product_scope`, `region_scope`, `effective_date`, `version`) to enable filtering and compliance checks.
- Structured references (`plan_matrix.csv`, `products.csv`, `error_codes.json`, `world_bible.json` subsets, `openapi.yaml`) are the source of truth for quantitative answers (limits, pricing, API details) and override conflicting prose content.
- LangChain orchestration is required for retriever composition and prompt management; OpenAI APIs supply both embeddings and completion models with configurable model IDs via environment variables.
- FastAPI owns all backend endpoints; Next.js consumes only documented REST/SSE interfaces—no direct database or vector store access from the frontend.

## Coding Standards
- Backend code uses Python 3.11+, typed with `mypy`, formatted with `ruff`/`black`, and organized into domain modules (`ingest`, `retrieval`, `api`, `models`).
- Frontend code uses Next.js 14+ with TypeScript, ESLint, and Prettier; favor React Server Components for data fetching and suspense for streaming chat.
- Tests accompany every module (pytest for backend, Vitest/Playwright for frontend) and must cover edge cases from eval questions (e.g., SSO resets, rate limit handling).
- Configuration lives in `.env` files surfaced through typed settings objects; never hard-code API keys, plan limits, or URLs.

## Data Handling & Compliance
- Respect `audience` and `product_scope` metadata at query time to prevent leaking agent-only runbooks or macros in customer-facing sessions.
- Store minimal chat transcripts; scrub PII and adhere to QuantLeaves policy windows (see `POL-0002` claim window, `POL-0001` SLA claims) when presenting billing guidance.
- On ingestion, validate effective dates and versioning; mark stale documents so the retrieval layer can deprioritize or exclude them.
- Maintain reproducible ingestion runs—every build of the index must be derivable from committed corpus artifacts plus configuration.

## Operational Practices
- CI must block merges unless linting, type checks, unit tests, and evaluation suite from `corpus/eval/eval_questions.json` all pass ≥90% target accuracy.
- Use feature branches with conventional commits; require PR reviews for any change touching retrieval logic or ingestion schemas.
- Log retrieval traces (document IDs, scores) and LLM prompts in observability tooling with access controls; redact user identifiers in logs.
- Schedule periodic sync (at least weekly) with support leadership to review new knowledge base changes before ingestion.

## Frontend Experience Requirements
- Surface citations (doc_id + title) for every factual statement; link back to canonical content where possible.
- Provide structured answer modes for quantitative lookups (e.g., plan comparison tables) using keyword retriever payloads instead of free-form text where feasible.
- Offer quick-reply suggestions derived from follow-up intents (e.g., “Reset password with SSO”, “Rate limit troubleshooting”, “Billing credits”).

## Reliability Expectations
- Target P95 total response < 6 seconds with first token < 2 seconds; implement graceful degradation (fallback canned response) when retrievers or LLMs fail.
- Implement exponential backoff and circuit breakers for OpenAI API calls; trigger alerts if failure rate > 5% over 5 minutes.
- Keep rollback path ready: ability to disable RAG (serve static FAQ answers) within 5 minutes if production issues occur.
