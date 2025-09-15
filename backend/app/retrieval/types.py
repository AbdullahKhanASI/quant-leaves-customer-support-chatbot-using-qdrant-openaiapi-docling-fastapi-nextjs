"""Retrieval result models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class StructuredHit:
    source: str
    identifier: str
    content: str
    metadata: dict[str, Any]


@dataclass(slots=True)
class VectorHit:
    doc_id: str
    score: float
    content: str
    metadata: dict[str, Any]


@dataclass(slots=True)
class HybridContext:
    query: str
    structured_hits: list[StructuredHit]
    vector_hits: list[VectorHit]
