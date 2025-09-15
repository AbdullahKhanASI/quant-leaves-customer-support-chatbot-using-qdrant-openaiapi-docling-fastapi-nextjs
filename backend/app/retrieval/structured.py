"""Structured keyword retrieval using SQL lookup."""
from __future__ import annotations

from sqlalchemy import Select, cast, or_, select, String

from app.db.models import ApiEndpoint, ErrorCode, Plan, Policy, Product
from app.db.session import get_session
from app.retrieval.types import StructuredHit


class StructuredRetriever:
    def __init__(self, limit: int = 5) -> None:
        self.limit = limit

    async def search(self, query: str) -> list[StructuredHit]:
        pattern = f"%{query.lower()}%"
        hits: list[StructuredHit] = []
        async with get_session() as session:
            hits.extend(await self._search_plans(session, pattern))
            hits.extend(await self._search_products(session, pattern))
            hits.extend(await self._search_error_codes(session, pattern))
            hits.extend(await self._search_api_endpoints(session, pattern))
            hits.extend(await self._search_policies(session, pattern))
        return hits[: self.limit]

    async def _search_plans(self, session, pattern: str) -> list[StructuredHit]:
        stmt: Select = select(Plan).where(
            or_(Plan.name.ilike(pattern), cast(Plan.entitlements, String).ilike(pattern))
        ).limit(self.limit)
        result = await session.execute(stmt)
        hits = []
        for plan in result.scalars():
            hits.append(
                StructuredHit(
                    source="plans",
                    identifier=plan.name,
                    content=f"Plan {plan.name}: users {plan.users_limit}, API {plan.api_calls_limit}, dashboards {plan.dashboards_limit}",
                    metadata={
                        "monthly_price": plan.monthly_price,
                        "annual_price": plan.annual_price,
                        "entitlements": plan.entitlements,
                    },
                )
            )
        return hits

    async def _search_products(self, session, pattern: str) -> list[StructuredHit]:
        stmt = select(Product).where(
            or_(Product.name.ilike(pattern), Product.short_desc.ilike(pattern), Product.sku.ilike(pattern))
        ).limit(self.limit)
        result = await session.execute(stmt)
        hits = []
        for product in result.scalars():
            hits.append(
                StructuredHit(
                    source="products",
                    identifier=product.sku,
                    content=f"{product.name}: {product.short_desc}",
                    metadata={
                        "category": product.category,
                        "compatibility": product.compatibility,
                        "status": product.status,
                    },
                )
            )
        return hits

    async def _search_error_codes(self, session, pattern: str) -> list[StructuredHit]:
        stmt = select(ErrorCode).where(
            or_(
                ErrorCode.code.ilike(pattern),
                ErrorCode.message.ilike(pattern),
                ErrorCode.cause.ilike(pattern),
                ErrorCode.fix.ilike(pattern),
            )
        ).limit(self.limit)
        result = await session.execute(stmt)
        hits = []
        for error in result.scalars():
            hits.append(
                StructuredHit(
                    source="error_codes",
                    identifier=error.code,
                    content=f"{error.code}: {error.message}",
                    metadata={
                        "cause": error.cause,
                        "fix": error.fix,
                        "severity": error.severity,
                        "service": error.service,
                    },
                )
            )
        return hits

    async def _search_api_endpoints(self, session, pattern: str) -> list[StructuredHit]:
        stmt = select(ApiEndpoint).where(
            or_(
                ApiEndpoint.path.ilike(pattern),
                ApiEndpoint.summary.ilike(pattern),
                ApiEndpoint.description.ilike(pattern),
            )
        ).limit(self.limit)
        result = await session.execute(stmt)
        hits = []
        for endpoint in result.scalars():
            hits.append(
                StructuredHit(
                    source="api_endpoints",
                    identifier=f"{endpoint.method} {endpoint.path}",
                    content=endpoint.description or endpoint.summary or "",
                    metadata={"summary": endpoint.summary, **(endpoint.extra or {})},
                )
            )
        return hits

    async def _search_policies(self, session, pattern: str) -> list[StructuredHit]:
        stmt = select(Policy).where(
            or_(
                Policy.name.ilike(pattern),
                Policy.version.ilike(pattern),
                cast(Policy.payload, String).ilike(pattern),
            )
        ).limit(self.limit)
        result = await session.execute(stmt)
        hits = []
        for policy in result.scalars():
            hits.append(
                StructuredHit(
                    source="policies",
                    identifier=policy.name,
                    content=f"Policy {policy.name} v{policy.version}",
                    metadata={
                        "effective_date": policy.effective_date.isoformat() if policy.effective_date else None,
                        "payload": policy.payload,
                    },
                )
            )
        return hits
