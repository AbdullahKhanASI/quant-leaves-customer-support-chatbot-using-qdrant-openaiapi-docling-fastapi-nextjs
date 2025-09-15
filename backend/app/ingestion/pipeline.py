"""Ingestion pipeline orchestrating structured and unstructured corpus loading."""
from __future__ import annotations

import asyncio
import logging
from datetime import date
from pathlib import Path
from typing import Iterable

from langchain_openai import OpenAIEmbeddings
from sqlalchemy import delete

from app.core.paths import CORPUS_DIR, STRUCTURED_DIR, UNSTRUCTURED_DIRS, iter_pdf_paths
from app.core.settings import AppSettings, get_settings
from app.db.models import ApiEndpoint, Document, DocumentChunk, ErrorCode, Plan, Policy, Product
from app.db.session import get_session
from app.db.utils import init_db
from app.ingestion.loaders.markdown_loader import chunk_markdown
from app.ingestion.loaders.pdf_loader import chunk_pdf
from app.ingestion.loaders.structured_loader import load_structured_records
from app.ingestion.loaders.openapi_loader import load_openapi_records
from app.ingestion.types import DocumentChunk as Chunk, StructuredRecord

logger = logging.getLogger(__name__)


class IngestionError(RuntimeError):
    pass


class IngestionPipeline:
    """Top-level ingestion workflow."""

    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self._embeddings: OpenAIEmbeddings | None = None

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        if not self.settings.openai_api_key:
            raise IngestionError("OPENAI_API_KEY is not configured. Update backend/.env before running ingestion.")
        if self._embeddings is None:
            base_url = str(self.settings.openai_api_base) if self.settings.openai_api_base else None
            self._embeddings = OpenAIEmbeddings(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_embedding_model,
                base_url=base_url,
            )
        return self._embeddings

    async def run_full(self) -> None:
        """Execute structured + unstructured ingestion."""
        await init_db()
        async with get_session() as session:
            await self._clear_existing(session)
            await self._ingest_structured(session)
            await self._ingest_openapi(session)
            await session.commit()

        await self._ingest_unstructured()

    async def _clear_existing(self, session) -> None:
        logger.info("Clearing existing structured data")
        await session.execute(delete(ApiEndpoint))
        await session.execute(delete(ErrorCode))
        await session.execute(delete(Plan))
        await session.execute(delete(Product))
        await session.execute(delete(Policy))
        await session.execute(delete(DocumentChunk))
        await session.execute(delete(Document))

    async def _ingest_structured(self, session) -> None:
        logger.info("Loading structured corpus tables")
        for record in load_structured_records():
            await self._persist_structured_record(session, record)

    async def _ingest_openapi(self, session) -> None:
        logger.info("Loading OpenAPI metadata")
        for record in load_openapi_records():
            await self._persist_structured_record(session, record)

    async def _persist_structured_record(self, session, record: StructuredRecord) -> None:
        table = record.table
        payload = record.payload
        if table == "plans":
            session.add(Plan(**payload))
        elif table == "products":
            session.add(Product(**payload))
        elif table == "error_codes":
            session.add(ErrorCode(**payload))
        elif table == "policies":
            payload = payload.copy()
            payload["effective_date"] = _coerce_date(payload.get("effective_date"))
            session.add(Policy(**payload))
        elif table == "api_endpoints":
            session.add(ApiEndpoint(**payload))
        else:
            logger.warning("Unhandled structured table %s", table)

    async def _ingest_unstructured(self) -> None:
        logger.info("Ingesting markdown corpus")
        markdown_files = list(_iter_markdown_paths())
        pdf_files = list(iter_pdf_paths())
        logger.info("Found %d markdown files and %d PDFs", len(markdown_files), len(pdf_files))

        chunks: list[Chunk] = []
        for path in markdown_files:
            chunks.extend(chunk_markdown(path, self.settings.chunk_size, self.settings.chunk_overlap))
        for path in pdf_files:
            chunks.extend(chunk_pdf(path, self.settings.chunk_size, self.settings.chunk_overlap))

        if not chunks:
            logger.warning("No chunks produced from corpus")
            return

        logger.info("Embedding %d chunks", len(chunks))
        batch_size = self.settings.ingestion_batch_size
        async with get_session() as session:
            documents_index: dict[str, Document] = {}
            for start in range(0, len(chunks), batch_size):
                batch = chunks[start : start + batch_size]
                embeddings = await asyncio.to_thread(self.embeddings.embed_documents, [c.content for c in batch])
                for chunk, embedding in zip(batch, embeddings):
                    doc = documents_index.get(chunk.metadata.doc_id)
                    if doc is None:
                        doc = Document(
                            doc_id=chunk.metadata.doc_id,
                            title=chunk.metadata.title,
                            doc_type=chunk.metadata.doc_type,
                            audience=chunk.metadata.audience,
                            product_scope=chunk.metadata.product_scope,
                            region_scope=chunk.metadata.region_scope,
                            version=chunk.metadata.version,
                            effective_date=chunk.metadata.effective_date,
                        )
                        session.add(doc)
                        await session.flush()
                        documents_index[chunk.metadata.doc_id] = doc
                    chunk_record = DocumentChunk(
                        document_id=doc.id,
                        chunk_index=chunk.ordinal,
                        content=chunk.content,
                        chunk_metadata={"source_path": str(chunk.metadata.source_path), **chunk.metadata.extra},
                        embedding=embedding,
                    )
                    session.add(chunk_record)
            await session.commit()

        logger.info("Unstructured ingestion complete")


def _coerce_date(value) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except Exception:  # noqa: BLE001
        return None


def _iter_markdown_paths() -> Iterable[Path]:
    for directory in UNSTRUCTURED_DIRS:
        if not directory.exists():
            continue
        yield from sorted(directory.glob("*.md"))
