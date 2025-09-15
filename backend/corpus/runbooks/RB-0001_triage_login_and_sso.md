---
doc_id: RB-0001
doc_type: runbook
audience: agent-internal
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-DASH"]
---
# Runbook: Triage login/SSO issues

## Checklist
1. Confirm tenant uses **SSO** (Pro/Enterprise).
2. If SSO: ask user to reset via IdP; do not send QL reset link.
3. Verify seat active and below **users_limit**.
4. If non-SSO: send password reset and confirm email delivery.

## Decision tree
- SSO tenant → IdP reset flow → if still failing, escalate to L2 with SAML/OIDC logs.
- Non-SSO → standard reset → if bounce/no email, check user status.

## Escalation
- L2 if SAML assertions mismatch, clock skew > 5 min, or audience/ACS URL mismatch.

## References
- world_bible.plans[].entitlements
- KB-0001
