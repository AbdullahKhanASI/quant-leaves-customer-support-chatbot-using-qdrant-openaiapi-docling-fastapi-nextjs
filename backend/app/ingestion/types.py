"""Shared ingestion dataclasses."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class DocumentMetadata:
    doc_id: str
    doc_type: str | None = None
    title: str | None = None
    audience: str | None = None
    product_scope: list[str] | None = None
    region_scope: list[str] | None = None
    version: str | None = None
    effective_date: date | None = None
    source_path: Path | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DocumentChunk:
    content: str
    metadata: DocumentMetadata
    ordinal: int


@dataclass(slots=True)
class StructuredRecord:
    table: str
    payload: dict[str, Any]
