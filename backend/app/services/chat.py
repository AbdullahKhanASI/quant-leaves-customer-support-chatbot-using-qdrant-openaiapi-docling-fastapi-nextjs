"""Chat orchestration service."""
from __future__ import annotations

import asyncio
from collections import OrderedDict
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import AppSettings, get_settings
from app.models.schemas import ChatRequest, ChatResponse, Citation
from app.retrieval.hybrid import HybridRetriever

SYSTEM_PROMPT = """You are QuantLeaves' support assistant. Use the provided context to answer customer and agent questions about analytics products, rate limits, SLAs, billing, and troubleshooting. Always cite your sources using [doc_id] notation. If the answer is not in the context, admit you do not know."""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """Question: {question}\n\nStructured context:\n{structured_context}\n\nUnstructured context:\n{unstructured_context}\n\nProvide a concise answer with citations and, if relevant, bullet steps.""",
        ),
    ]
)


class ChatService:
    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self.retriever = HybridRetriever()
        self._llm: ChatOpenAI | None = None

    @property
    def llm(self) -> ChatOpenAI:
        if not self.settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured. Update backend/.env before running chat endpoint.")
        if self._llm is None:
            base_url = str(self.settings.openai_api_base) if self.settings.openai_api_base else None
            self._llm = ChatOpenAI(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_chat_model,
                base_url=base_url,
                temperature=0.2,
            )
        return self._llm

    async def answer(self, request: ChatRequest) -> ChatResponse:
        context = await self.retriever.search(request.question)
        structured_context = self._format_structured(context.structured_hits)
        unstructured_context = self._format_unstructured(context.vector_hits)

        response = await self.llm.ainvoke(
            PROMPT.format_messages(
                question=request.question,
                structured_context=structured_context,
                unstructured_context=unstructured_context,
            )
        )

        citations = self._build_citations(context.vector_hits)
        structured_payload = [
            {
                **({} if hit.metadata is None else hit.metadata),
                "source": hit.source,
                "identifier": hit.identifier,
                "content": hit.content,
            }
            for hit in context.structured_hits
        ]
        return ChatResponse(answer=response.content.strip(), citations=citations, structured_results=structured_payload)

    def _format_structured(self, hits) -> str:
        if not hits:
            return "(no structured matches)"
        lines = []
        for hit in hits:
            metadata_parts = [f"{key}={value}" for key, value in hit.metadata.items() if value is not None]
            meta_str = ", ".join(metadata_parts)
            lines.append(f"[{hit.source}:{hit.identifier}] {hit.content} ({meta_str})")
        return "\n".join(lines)

    def _format_unstructured(self, hits) -> str:
        if not hits:
            return "(no unstructured matches)"
        lines = []
        for hit in hits:
            lines.append(f"[{hit.doc_id}] score={hit.score:.4f} :: {hit.content}")
        return "\n".join(lines)

    def _build_citations(self, hits) -> list[Citation]:
        seen: OrderedDict[str, Citation] = OrderedDict()
        for hit in hits:
            if hit.doc_id not in seen:
                seen[hit.doc_id] = Citation(doc_id=hit.doc_id, snippet=hit.content[:300], metadata=hit.metadata)
        return list(seen.values())
