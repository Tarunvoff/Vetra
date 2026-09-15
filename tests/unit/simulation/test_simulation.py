import pytest
from vetra.simulation.engine import SimulatedEngineAdapter
from vetra.simulation.environment import SimulatedPolicyEnvironment


@pytest.mark.asyncio
async def test_simulated_engine():
    adapter = SimulatedEngineAdapter(base_utilization=0.75)
    assert await adapter.health() is True

    gpu = await adapter.get_gpu_stats()
    assert gpu.total_memory_bytes > 0
    assert 0.1 <= gpu.memory_pressure <= 1.0

    blocks = await adapter.get_block_stats()
    assert len(blocks) > 0


@pytest.mark.asyncio
async def test_simulated_environment_step():
    env = SimulatedPolicyEnvironment(base_utilization=0.88)
    res = await env.step()

    assert "gpu_stats" in res
    assert "recommendations" in res
    assert len(res["recommendations"]) > 0
