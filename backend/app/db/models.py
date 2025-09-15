"""SQLAlchemy models for structured corpus and embeddings."""
from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    monthly_price: Mapped[float | None]
    annual_price: Mapped[float | None]
    users_limit: Mapped[int | None]
    api_calls_limit: Mapped[int | None]
    dashboards_limit: Mapped[int | None]
    entitlements: Mapped[list[str] | None] = mapped_column(JSON)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50))
    short_desc: Mapped[str | None] = mapped_column(Text)
    compatibility: Mapped[list[str] | None] = mapped_column(JSON)
    status: Mapped[str | None] = mapped_column(String(30))


class ErrorCode(Base):
    __tablename__ = "error_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    message: Mapped[str | None] = mapped_column(String(255))
    cause: Mapped[str | None] = mapped_column(String(255))
    fix: Mapped[str | None] = mapped_column(String(255))
    severity: Mapped[str | None] = mapped_column(String(20))
    service: Mapped[str | None] = mapped_column(String(50))


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str | None] = mapped_column(String(20))
    effective_date: Mapped[date | None] = mapped_column(Date)
    payload: Mapped[dict | None] = mapped_column(JSON)


class ApiEndpoint(Base):
    __tablename__ = "api_endpoints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String(200), nullable=False)
    method: Mapped[str] = mapped_column(String(10), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    extra: Mapped[dict | None] = mapped_column(JSON)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doc_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    title: Mapped[str | None] = mapped_column(String(200))
    doc_type: Mapped[str | None] = mapped_column(String(50))
    audience: Mapped[str | None] = mapped_column(String(50))
    product_scope: Mapped[list[str] | None] = mapped_column(JSON)
    region_scope: Mapped[list[str] | None] = mapped_column(JSON)
    version: Mapped[str | None] = mapped_column(String(20))
    effective_date: Mapped[date | None] = mapped_column(Date)

    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    chunk_metadata: Mapped[dict | None] = mapped_column(JSON)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(3072))

    document: Mapped[Document] = relationship(back_populates="chunks")
