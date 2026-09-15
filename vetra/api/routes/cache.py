"""Cache block inspection and decision application endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from vetra.api.dependencies import ServiceContainer, get_container
from vetra.core.models import KVBlockStats, UnifiedDecision

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.get("/blocks", response_model=List[KVBlockStats])
async def list_cache_blocks(
    tenant_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    container: ServiceContainer = Depends(get_container),
) -> List[KVBlockStats]:
    blocks = await container.metadata_repo.list_blocks(tenant_id=tenant_id, limit=limit, offset=offset)
    if not blocks:
        # Fallback to engine blocks if repo is empty (simulation mode)
        blocks = await container.engine_adapter.get_block_stats()
    return blocks


@router.get("/blocks/{block_id}", response_model=KVBlockStats)
async def get_cache_block(
    block_id: str, container: ServiceContainer = Depends(get_container)
) -> KVBlockStats:
    block = await container.metadata_repo.get_block(block_id)
    if not block:
        blocks = await container.engine_adapter.get_block_stats()
        block = next((b for b in blocks if b.block_id == block_id), None)

    if not block:
        raise HTTPException(status_code=404, detail=f"Block '{block_id}' not found.")
    return block


@router.post("/decisions/apply", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def apply_cache_decision(
    decision: UnifiedDecision,
    container: ServiceContainer = Depends(get_container),
):
    """Execution endpoint for applying KV cache mutation decisions.

    Returns HTTP 501 Not Implemented during Phase 1 dry-run mode until direct engine mutation is supported.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "status": "NOT_IMPLEMENTED",
            "message": "Direct KV cache mutation is disabled in dry-run mode / Phase 1.",
            "decision": decision.decision.value,
            "block_id": decision.block_id,
            "recommendation": "Use GET /api/v1/recommendations for policy suggestions.",
        },
    )
