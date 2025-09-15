"""PDF ingestion via Docling."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

from docling.document_converter import DocumentConverter

from app.ingestion.loaders.markdown_loader import FRONT_MATTER_PATTERN, parse_front_matter
from app.ingestion.types import DocumentChunk, DocumentMetadata


@lru_cache
def _converter() -> DocumentConverter:
    return DocumentConverter()


def load_pdf(path: Path) -> tuple[DocumentMetadata, str]:
    result = _converter().convert(path)
    if result.errors:
        raise RuntimeError(f"Docling reported errors converting {path}: {result.errors}")
    document = result.document or result.legacy_document
    if document is None:
        raise RuntimeError(f"Docling failed to produce a document for {path}")
    markdown = document.export_to_markdown()
    metadata, body = parse_front_matter(markdown, path)
    return metadata, body


def chunk_pdf(path: Path, chunk_size: int, chunk_overlap: int) -> Iterable[DocumentChunk]:
    metadata, body = load_pdf(path)
    tokens = body.split()
    chunks: list[DocumentChunk] = []
    if not tokens:
        return chunks
    start = 0
    ordinal = 0
    while start < len(tokens):
        end = min(len(tokens), start + chunk_size)
        chunk_text = " ".join(tokens[start:end])
        chunks.append(DocumentChunk(content=chunk_text, metadata=metadata, ordinal=ordinal))
        ordinal += 1
        if end == len(tokens):
            break
        start = max(end - chunk_overlap, start + 1)
    return chunks
