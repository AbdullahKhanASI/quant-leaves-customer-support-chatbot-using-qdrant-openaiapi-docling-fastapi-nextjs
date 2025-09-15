---
doc_id: KB-0002
doc_type: kb_article
audience: public
version: v1.0
effective_date: 2025-07-01
region_scope: ["US","EU"]
product_scope: ["QL-DASH"]
---
# Connect a data source

## Summary
Add a warehouse or database so dashboards can query data.

## Prerequisites
- Starter and up. Admin role.

## Steps
1. Go to **Settings → Connections → Add source**.
2. Choose **Postgres**, **Snowflake**, or **BigQuery**.
3. Enter credentials (read-only user recommended).
4. Click **Test** → **Save** → Select datasets to expose to QL-DASH.

## Edge cases
- Network allowlists may be required.
- Column-level security: apply in your warehouse; QL respects underlying permissions.

## References
- world_bible.products["QL-DASH"]
- world_bible.plans[].features
