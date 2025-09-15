"""Vector similarity retrieval using pgvector."""
from __future__ import annotations

import asyncio
from typing import Sequence

from langchain_openai import OpenAIEmbeddings
from sqlalchemy import select

from app.core.settings import AppSettings, get_settings
from app.db.models import Document, DocumentChunk
from app.db.session import get_session
from app.retrieval.types import VectorHit


class VectorRetriever:
    def __init__(self, settings: AppSettings | None = None, k: int = 6) -> None:
        self.settings = settings or get_settings()
        self.k = k
        self._embeddings: OpenAIEmbeddings | None = None

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        if not self.settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured. Update backend/.env before running retrieval.")
        if self._embeddings is None:
            base_url = str(self.settings.openai_api_base) if self.settings.openai_api_base else None
            self._embeddings = OpenAIEmbeddings(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_embedding_model,
                base_url=base_url,
            )
        return self._embeddings

    async def search(self, query: str) -> list[VectorHit]:
        embedding = await asyncio.to_thread(self.embeddings.embed_query, query)
        async with get_session() as session:
            distance = DocumentChunk.embedding.cosine_distance(embedding).label("distance")
            stmt = (
                select(DocumentChunk, Document, distance)
                .join(Document, DocumentChunk.document_id == Document.id)
                .order_by(distance)
                .limit(self.k)
            )
            result = await session.execute(stmt)
            hits: list[VectorHit] = []
            for chunk, document, distance_value in result.all():
                score = 1 - float(distance_value) if distance_value is not None else 0.0
                hits.append(
                    VectorHit(
                        doc_id=document.doc_id,
                        score=score,
                        content=chunk.content,
                        metadata={
                            "doc_type": document.doc_type,
                            "audience": document.audience,
                            "product_scope": document.product_scope,
                            "region_scope": document.region_scope,
                            "version": document.version,
                            "effective_date": document.effective_date.isoformat() if document.effective_date else None,
                            "chunk_index": chunk.chunk_index,
                        },
                    )
                )
            return hits
