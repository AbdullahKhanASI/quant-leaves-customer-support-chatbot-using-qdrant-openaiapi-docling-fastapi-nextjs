---
doc_id: MAC-0001
doc_type: agent_macros
audience: agent-internal
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["All"]
---
# Agent Macro Pack

## Greeting + Verification (General)
Hi <first name> — happy to help! For security, could you confirm your org name and work email?

## Billing Dispute (Within 30 Days)
Thanks for flagging this. Per our policy, disputes must be raised within 30 days. I can review your invoices and apply any eligible **SLA credits** from outages. Shall I proceed?

## SSO Password Reset
Since your org uses **SSO**, password resets are handled by your identity provider. Please use your IdP’s self-service reset. If that fails, I can loop in our L2 team with SAML/OIDC logs.

## Rate Limit Guidance
I see `E1002` errors. Your plan allows **<limit>/min**. Please throttle requests or consider upgrading if your workload is sustained above this level. Here’s a sample backoff you can try.
