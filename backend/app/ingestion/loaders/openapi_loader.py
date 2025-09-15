"""OpenAPI ingestion utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from app.core.paths import CORPUS_DIR
from app.ingestion.types import StructuredRecord

OPENAPI_PATH = CORPUS_DIR / "api" / "openapi.yaml"


def load_openapi_records() -> Iterable[StructuredRecord]:
    spec = yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, definition in methods.items():
            payload = {
                "path": path,
                "method": method.upper(),
                "summary": definition.get("summary"),
                "description": definition.get("description"),
                "extra": {
                    "parameters": definition.get("parameters"),
                    "responses": definition.get("responses"),
                },
            }
            yield StructuredRecord(table="api_endpoints", payload=payload)
