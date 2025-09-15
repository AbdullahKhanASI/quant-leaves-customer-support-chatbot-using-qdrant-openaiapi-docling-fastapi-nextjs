"""Admin ingestion endpoints."""
from fastapi import APIRouter, Depends

from app.api.deps import get_ingestion_service
from app.models.schemas import IngestionResponse
from app.services.ingestion import IngestionService

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/refresh", response_model=IngestionResponse, summary="Trigger corpus re-index")
async def refresh_index(service: IngestionService = Depends(get_ingestion_service)) -> IngestionResponse:
    """Run the ingestion pipeline on demand."""
    result = await service.run_full()
    return IngestionResponse(status=result.get("status", "unknown"), detail=result.get("detail"))
