"""High-level ingestion service."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.core.settings import AppSettings, get_settings
from app.ingestion.pipeline import IngestionPipeline, IngestionError

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self.pipeline = IngestionPipeline(self.settings)

    async def run_full(self) -> dict[str, Any]:
        try:
            await self.pipeline.run_full()
            return {"status": "completed"}
        except IngestionError as exc:
            logger.error("Ingestion failed: %s", exc)
            return {"status": "error", "detail": str(exc)}


async def run_ingestion_async() -> dict[str, Any]:
    service = IngestionService()
    return await service.run_full()


def run_ingestion() -> dict[str, Any]:
    return asyncio.run(run_ingestion_async())
