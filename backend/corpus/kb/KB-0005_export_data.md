---
doc_id: KB-0005
doc_type: kb_article
audience: public
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-DASH","QL-API"]
---
# Export your data

## Summary
Export dashboards as CSV from UI or use the Metrics API.

## Steps (UI)
1. Open a dashboard → **Export → CSV**.
2. Choose date range and granularity → **Export**.

## Steps (API)
- Use `GET /v1/metrics?metric_id=...&from=...&to=...`.
- Authenticate with Bearer token.

## References
- world_bible.products["QL-API"]
- world_bible.api.base_url, auth
