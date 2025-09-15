"""Database utility helpers."""
from sqlalchemy import text

from app.db.models import Base
from app.db.session import get_engine


async def init_db() -> None:
    """Create database schema if it doesn't exist."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
