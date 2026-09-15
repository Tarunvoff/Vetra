"""Policy configuration and registered engine inspection."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from vetra.api.dependencies import ServiceContainer, get_container
from vetra.api.schemas.policies import PolicyStatusResponse
from vetra.core.models import PolicyConstraints
from vetra.core.registry import EngineRegistry

router = APIRouter(tags=["Policies & Engines"])


@router.get("/policies", response_model=PolicyStatusResponse)
async def get_policy_status(
    container: ServiceContainer = Depends(get_container),
) -> PolicyStatusResponse:
    constraints = PolicyConstraints(
        max_gpu_memory_percent=container.settings.policy.gpu_memory_threshold,
        max_cpu_memory_percent=container.settings.policy.cpu_memory_threshold,
        minimum_block_importance=container.settings.policy.min_importance_to_offload,
    )
    return PolicyStatusResponse(
        engine_name=container.settings.engine.value,
        active_policy="RuleBasedPolicyEngine (Phase 1)",
        constraints=constraints,
        rules_count=3,
    )


@router.get("/engines")
async def list_engines(
    container: ServiceContainer = Depends(get_container),
) -> Dict[str, Any]:
    current_info = await container.engine_adapter.get_engine_info()
    return {
        "active_engine": container.settings.engine.value,
        "available_engines": EngineRegistry.list_engines(),
        "active_engine_info": current_info,
    }
