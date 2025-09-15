"""Command-line entry point for ingestion."""
from __future__ import annotations

import asyncio
import logging

from app.services.ingestion import run_ingestion_async

logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Run the ingestion job."""
    result = asyncio.run(run_ingestion_async())
    status = result.get("status")
    detail = result.get("detail")
    if status != "completed":
        raise SystemExit(f"Ingestion failed: {detail}")


if __name__ == "__main__":
    main()
