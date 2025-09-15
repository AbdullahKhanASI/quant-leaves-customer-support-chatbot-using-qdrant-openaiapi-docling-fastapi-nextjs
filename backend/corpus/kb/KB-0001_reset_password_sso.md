---
doc_id: KB-0001
doc_type: kb_article
audience: public
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-DASH"]
---
# Reset your password (with and without SSO)

## Summary
How to reset a QuantLeaves password, including SSO tenants (SAML/OIDC).

## Steps
1. **Check SSO**: If your org uses SSO (Pro/Enterprise entitlements include `sso`), you must reset the password with your identity provider.
2. **Non-SSO tenants**: Click **Forgot password** at sign-in → enter email → follow link (valid 60 minutes).
3. **No email?** Check spam and verify your email is the primary login.
4. **Still blocked?** Ask your admin to confirm your seat is active and not over **users_limit** for your plan.

## Edge cases
- **SSO enabled**: Reset link from QuantLeaves won’t work; use your IdP self-service.
- **Over limits**: If your org is above plan limits (see `Plan limit exceeded`), admins may be unable to add or re-activate users.

## FAQ
- *Which plans have SSO?* Pro and Enterprise.
- *Token lifetime?* 60 minutes.

## References
- world_bible.plans[].entitlements
- world_bible.api.rate_limits
- world_bible.error_codes (E3001)
