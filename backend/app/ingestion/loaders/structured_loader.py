"""Structured data loaders for CSV/JSON corpus tables."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from app.core.paths import STRUCTURED_DIR
from app.ingestion.types import StructuredRecord


def load_structured_records() -> Iterable[StructuredRecord]:
    """Load structured tables from the corpus."""
    yield from _load_plan_matrix(STRUCTURED_DIR / "plan_matrix.csv")
    yield from _load_products(STRUCTURED_DIR / "products.csv")
    yield from _load_error_codes(STRUCTURED_DIR / "error_codes.json")
    yield from _load_world_bible(STRUCTURED_DIR.parent / "world_bible.json")


def _load_plan_matrix(path: Path) -> Iterable[StructuredRecord]:
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            payload = {
                "name": row.get("plan"),
                "monthly_price": float(row["monthly_price"]) if row.get("monthly_price") else None,
                "annual_price": float(row["annual_price"]) if row.get("annual_price") else None,
                "users_limit": int(row["users_limit"]) if row.get("users_limit") else None,
                "api_calls_limit": int(row["api_calls_limit"]) if row.get("api_calls_limit") else None,
                "dashboards_limit": int(row["dashboards_limit"]) if row.get("dashboards_limit") else None,
                "entitlements": row.get("entitlements", "").split(";") if row.get("entitlements") else None,
            }
            yield StructuredRecord(table="plans", payload=payload)


def _load_products(path: Path) -> Iterable[StructuredRecord]:
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            payload = {
                "sku": row.get("sku"),
                "name": row.get("name"),
                "category": row.get("category"),
                "short_desc": row.get("short_desc"),
                "compatibility": row.get("compatibility", "").split(";") if row.get("compatibility") else None,
                "status": row.get("status"),
            }
            yield StructuredRecord(table="products", payload=payload)


def _load_error_codes(path: Path) -> Iterable[StructuredRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for row in data:
        yield StructuredRecord(table="error_codes", payload=row)


def _load_world_bible(path: Path) -> Iterable[StructuredRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    policies = data.get("policies", {})
    for name, policy in policies.items():
        payload = {
            "name": name,
            "version": policy.get("version"),
            "effective_date": policy.get("effective_date"),
            "payload": policy,
        }
        yield StructuredRecord(table="policies", payload=payload)

    api = data.get("api", {})
    rate_limits = api.get("rate_limits", {})
    for plan_name, limit in rate_limits.items():
        payload = {
            "code": f"RATE_LIMIT_{plan_name.upper()}",
            "message": "Rate limit",  # placeholder to populate table for cross-reference
            "cause": f"Quota for {plan_name}",
            "fix": f"Respect {limit}",
            "severity": "info",
            "service": "api_gateway",
        }
        yield StructuredRecord(table="error_codes", payload=payload)
