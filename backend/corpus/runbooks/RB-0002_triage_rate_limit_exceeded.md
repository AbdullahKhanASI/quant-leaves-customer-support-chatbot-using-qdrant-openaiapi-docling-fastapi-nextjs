---
doc_id: RB-0002
doc_type: runbook
audience: agent-internal
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-API"]
---
# Runbook: Triage E1002 Rate Limit Exceeded

## Steps
1. Confirm plan (Starter/Pro/Enterprise) and expected quota.
2. Check `x-rate-limit-remaining` and `retry-after` headers.
3. Recommend client-side throttling or batching.
4. Offer upgrade path if sustained usage exceeds limits.

## Escalation
- L2 if bursts < plan quota still trigger E1002 (possible shared tenant or gateway bug).

## References
- KB-0003
- world_bible.api.rate_limits
- world_bible.error_codes["E1002"]
