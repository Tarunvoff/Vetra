"""Policy recommendation generation and query endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from vetra.api.dependencies import ServiceContainer, get_container
from vetra.api.schemas.recommendations import (
    RecommendationListResponse,
    SimulateRecommendationRequest,
)
from vetra.core.enums import DecisionType
from vetra.core.models import Recommendation
from vetra.scoring.importance import compute_importance
from vetra.telemetry.metrics import RECOMMENDATIONS_TOTAL

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=RecommendationListResponse)
async def get_all_recommendations(
    container: ServiceContainer = Depends(get_container),
) -> RecommendationListResponse:
    gpu = await container.engine_adapter.get_gpu_stats()
    blocks = await container.metadata_repo.list_blocks(limit=100)

    # If no blocks stored, try engine block stats
    if not blocks:
        blocks = await container.engine_adapter.get_block_stats()

    recs: List[Recommendation] = []
    for blk in blocks:
        importance = compute_importance(
            blk,
            recency_weight=container.settings.scoring.recency_weight,
            frequency_weight=container.settings.scoring.frequency_weight,
            reuse_weight=container.settings.scoring.reuse_weight,
        )
        blk.importance_score = importance
        rec = container.policy_engine.evaluate(blk, gpu, importance)
        recs.append(rec)
        # Update metric counter
        RECOMMENDATIONS_TOTAL.labels(decision_type=rec.decision.value).inc()

    summary = {
        DecisionType.KEEP.value: sum(1 for r in recs if r.decision == DecisionType.KEEP),
        DecisionType.OFFLOAD_CPU.value: sum(1 for r in recs if r.decision == DecisionType.OFFLOAD_CPU),
        DecisionType.EVICT.value: sum(1 for r in recs if r.decision == DecisionType.EVICT),
        DecisionType.PREFETCH.value: sum(1 for r in recs if r.decision == DecisionType.PREFETCH),
    }

    return RecommendationListResponse(
        total=len(recs),
        recommendations=recs,
        gpu_pressure=round(gpu.memory_pressure, 3),
        summary=summary,
    )


@router.get("/{block_id}", response_model=Recommendation)
async def get_recommendation_by_block(
    block_id: str, container: ServiceContainer = Depends(get_container)
) -> Recommendation:
    blk = await container.metadata_repo.get_block(block_id)
    if not blk:
        # Search engine blocks
        blocks = await container.engine_adapter.get_block_stats()
        blk = next((b for b in blocks if b.block_id == block_id), None)

    if not blk:
        raise HTTPException(status_code=404, detail=f"Block {block_id} not found.")

    gpu = await container.engine_adapter.get_gpu_stats()
    importance = compute_importance(blk)
    blk.importance_score = importance
    return container.policy_engine.evaluate(blk, gpu, importance)


@router.post("/simulate", response_model=RecommendationListResponse)
async def simulate_recommendations(
    req: SimulateRecommendationRequest,
    container: ServiceContainer = Depends(get_container),
) -> RecommendationListResponse:
    from vetra.cache.block import create_sample_block
    import random

    gpu = await container.engine_adapter.get_gpu_stats()
    gpu.used_memory_bytes = int(gpu.total_memory_bytes * (req.gpu_pressure or 0.85))

    sim_blocks = [
        create_sample_block(
            block_id=f"sim_req_blk_{i:02d}",
            tenant_id=f"tenant_{i % 2}",
            importance=round(random.uniform(0.1, 0.95), 2),
        )
        for i in range(req.num_blocks or 10)
    ]

    recs = [
        container.policy_engine.evaluate(b, gpu, b.importance_score) for b in sim_blocks
    ]

    return RecommendationListResponse(
        total=len(recs),
        recommendations=recs,
        gpu_pressure=round(gpu.memory_pressure, 3),
        summary={"mode": "simulated_on_demand"},
    )
