"""Dependency container and runtime service manager for FastAPI routes."""

from __future__ import annotations

from typing import Optional
from kvguard.cache.manager import CacheManager
from kvguard.config import Settings, load_settings
from kvguard.core.enums import ExecutionMode
from kvguard.core.interfaces import ICacheMetadataRepository, IInferenceEngineAdapter
from kvguard.economics.cost_model import CostModel
from kvguard.economics.optimizer import CostOptimizer
from kvguard.engines.vllm.adapter import VLLMAdapter
from kvguard.policy.engine import PolicyEngine
from kvguard.security.policy import SecurityPolicyEngine
from kvguard.simulation.engine import SimulatedEngineAdapter
from kvguard.storage.memory import InMemoryMetadataRepository
from kvguard.storage.redis import RedisMetadataRepository
from kvguard.telemetry.aggregator import TelemetryAggregator
from kvguard.telemetry.collector import TelemetryCollector
from kvguard.telemetry.request_tracker import RequestTracker


class ServiceContainer:
    """Central dependency container initialized at application startup."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or load_settings()

        # Engine selection
        if self.settings.execution_mode == ExecutionMode.SIMULATION:
            self.engine_adapter: IInferenceEngineAdapter = SimulatedEngineAdapter()
        else:
            self.engine_adapter = VLLMAdapter(
                base_url=self.settings.vllm.base_url,
                metrics_path=self.settings.vllm.metrics_path,
                health_path=self.settings.vllm.health_path,
                timeout=self.settings.vllm.timeout_seconds,
            )

        # Storage repository
        if self.settings.redis.use_in_memory_fallback:
            self.metadata_repo: ICacheMetadataRepository = RedisMetadataRepository(
                url=self.settings.redis.url,
                key_prefix=self.settings.redis.key_prefix,
                use_in_memory_fallback=True,
            )
        else:
            self.metadata_repo = RedisMetadataRepository(
                url=self.settings.redis.url,
                key_prefix=self.settings.redis.key_prefix,
                use_in_memory_fallback=False,
            )

        # Services
        self.cache_manager = CacheManager(self.metadata_repo)
        self.aggregator = TelemetryAggregator(window_seconds=60.0)
        self.request_tracker = RequestTracker(max_size=self.settings.telemetry.buffer_size)

        self.telemetry_collector = TelemetryCollector(
            engine_adapter=self.engine_adapter,
            metadata_repo=self.metadata_repo,
            aggregator=self.aggregator,
            request_tracker=self.request_tracker,
            interval_seconds=self.settings.telemetry.interval_seconds,
        )

        self.policy_engine = PolicyEngine(
            gpu_pressure_high=self.settings.policy.gpu_pressure_high,
            gpu_pressure_medium=self.settings.policy.gpu_pressure_medium,
            min_importance_to_keep=self.settings.policy.min_importance_to_keep,
            min_importance_to_offload=self.settings.policy.min_importance_to_offload,
        )

        self.cost_model = CostModel(
            gpu_hourly_cost=self.settings.economics.gpu_cost_per_hour,
            cpu_hourly_cost=self.settings.economics.cpu_cost_per_hour,
            storage_per_gb_month=self.settings.economics.storage_cost_per_gb_month,
        )
        self.cost_optimizer = CostOptimizer(self.cost_model)
        self.security_engine = SecurityPolicyEngine()

    async def initialize(self) -> None:
        await self.engine_adapter.connect()
        if isinstance(self.metadata_repo, RedisMetadataRepository):
            await self.metadata_repo.initialize()
        await self.telemetry_collector.start()

    async def shutdown(self) -> None:
        await self.telemetry_collector.stop()
        await self.engine_adapter.disconnect()


# Global service container instance
_container: Optional[ServiceContainer] = None


def get_container() -> ServiceContainer:
    global _container
    if _container is None:
        _container = ServiceContainer()
    return _container


def set_container(container: ServiceContainer) -> None:
    global _container
    _container = container
