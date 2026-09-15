"""Optimization and simulation execution endpoints."""

from typing import Any, Dict
from fastapi import APIRouter, Depends
from kvguard.api.dependencies import ServiceContainer, get_container
from kvguard.simulation.environment import SimulatedPolicyEnvironment

router = APIRouter(tags=["Optimization & Simulation"])


@router.get("/optimization/status")
async def get_optimization_status(
    container: ServiceContainer = Depends(get_container),
) -> Dict[str, Any]:
    return {
        "optimization_enabled": container.settings.features.enable_optimization,
        "phase": "Phase 4 (Placement & Quantization Simulator)",
        "quantization_strategy": "simulation_ready",
        "prefetch_strategy": "heuristic_sequential",
    }


@router.post("/simulation/run")
async def run_simulation_step(
    pressure: float = 0.88,
    container: ServiceContainer = Depends(get_container),
) -> Dict[str, Any]:
    env = SimulatedPolicyEnvironment(base_utilization=pressure)
    step_result = await env.step()
    return {
        "status": "success",
        "memory_pressure": round(step_result["memory_pressure"], 3),
        "total_blocks_simulated": step_result["total_blocks"],
        "recommendations_count": len(step_result["recommendations"]),
        "recommendations": [r.model_dump() for r in step_result["recommendations"][:10]],
    }
