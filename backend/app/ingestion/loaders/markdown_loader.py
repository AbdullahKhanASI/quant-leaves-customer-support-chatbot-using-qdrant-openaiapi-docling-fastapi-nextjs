"""Markdown loader that preserves YAML front-matter."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml

from app.ingestion.types import DocumentChunk, DocumentMetadata

FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_front_matter(raw: str, path: Path) -> tuple[DocumentMetadata, str]:
    metadata: dict[str, object] = {}
    body = raw

    match = FRONT_MATTER_PATTERN.match(raw)
    if match:
        yaml_block, body = match.groups()
        metadata = yaml.safe_load(yaml_block) or {}

    meta = _metadata_from_dict(metadata, path)
    meta.title = meta.title or _extract_title(body)
    return meta, body.strip()


def load_markdown(path: Path) -> tuple[DocumentMetadata, str]:
    """Parse a markdown file, returning metadata + body."""
    raw = path.read_text(encoding="utf-8")
    return parse_front_matter(raw, path)


def chunk_markdown(path: Path, chunk_size: int, chunk_overlap: int) -> Iterable[DocumentChunk]:
    """Yield markdown content chunks with inherited metadata."""
    metadata, body = load_markdown(path)
    tokens = body.split()
    if not tokens:
        return []

    chunks: list[DocumentChunk] = []
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


def _metadata_from_dict(data: dict[str, object], path: Path) -> DocumentMetadata:
    doc_id = str(data.get("doc_id") or path.stem)
    effective_date = data.get("effective_date")
    effective_date_dt = None
    if isinstance(effective_date, str):
        try:
            effective_date_dt = datetime.fromisoformat(effective_date).date()
        except ValueError:
            effective_date_dt = None

    return DocumentMetadata(
        doc_id=doc_id,
        doc_type=_coerce_str(data.get("doc_type")),
        audience=_coerce_str(data.get("audience")),
        product_scope=_ensure_list(data.get("product_scope")),
        region_scope=_ensure_list(data.get("region_scope")),
        version=_coerce_str(data.get("version")),
        effective_date=effective_date_dt,
        source_path=path,
        extra={k: v for k, v in data.items() if k not in {
            "doc_id",
            "doc_type",
            "audience",
            "product_scope",
            "region_scope",
            "version",
            "effective_date",
        }},
    )


def _extract_title(body: str) -> str | None:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("# ")
    return None


def _ensure_list(value: object) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _coerce_str(value: object) -> str | None:
    return None if value is None else str(value)
