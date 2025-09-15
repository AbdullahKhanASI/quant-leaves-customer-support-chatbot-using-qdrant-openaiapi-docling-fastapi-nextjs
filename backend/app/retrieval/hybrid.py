"""Hybrid retriever combining structured SQL lookup and vector similarity."""
from __future__ import annotations

from app.retrieval.structured import StructuredRetriever
from app.retrieval.types import HybridContext
from app.retrieval.vector import VectorRetriever


class HybridRetriever:
    def __init__(self, structured: StructuredRetriever | None = None, vector: VectorRetriever | None = None) -> None:
        self.structured = structured or StructuredRetriever()
        self.vector = vector or VectorRetriever()

    async def search(self, query: str) -> HybridContext:
        structured_hits = await self.structured.search(query)
        vector_hits = await self.vector.search(query)
        return HybridContext(query=query, structured_hits=structured_hits, vector_hits=vector_hits)
