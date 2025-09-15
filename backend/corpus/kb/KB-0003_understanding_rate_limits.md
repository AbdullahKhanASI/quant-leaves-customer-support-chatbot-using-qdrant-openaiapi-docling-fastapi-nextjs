---
doc_id: KB-0003
doc_type: kb_article
audience: public
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-API"]
---
# Understanding API rate limits

## Summary
Each plan has a per-minute request quota.

## Limits by plan
- **Starter**: 60/min
- **Pro**: 600/min
- **Enterprise**: 2000/min

## Tips
- Use client-side throttling and retry-after headers.
- Batch reads where possible.

## Common errors
- `E1002 Rate limit exceeded` → slow down or upgrade.

## References
- world_bible.api.rate_limits
- world_bible.error_codes["E1002"]
