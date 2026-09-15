"""Abstract interfaces defining extension points across KVGuard architectural layers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from kvguard.core.models import (
    CacheEvent,
    CostBreakdown,
    EngineCapabilities,
    GPUStats,
    KVBlockStats,
    PlacementDecision,
    PolicyConstraints,
    Prediction,
    Recommendation,
    RequestStats,
    SecurityAction,
    UnifiedDecision,
)


class IInferenceEngineAdapter(ABC):
    """Contract for inference engine connectors (vLLM, SGLang, TensorRT-LLM, Simulated)."""

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the engine."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the engine."""
        pass

    @abstractmethod
    async def health(self) -> bool:
        """Check engine health and responsiveness."""
        pass

    @abstractmethod
    async def get_engine_info(self) -> Dict[str, Any]:
        """Return engine metadata (version, model, status)."""
        pass

    @abstractmethod
    async def get_gpu_stats(self) -> GPUStats:
        """Return real-time GPU statistics."""
        pass

    @abstractmethod
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Return aggregated cache statistics from the engine."""
        pass

    @abstractmethod
    async def get_request_stats(self) -> List[RequestStats]:
        """Return recent request-level statistics."""
        pass

    @abstractmethod
    def get_capabilities(self) -> EngineCapabilities:
        """Return supported features and integration status."""
        pass

    @abstractmethod
    async def get_block_stats(self) -> List[KVBlockStats]:
        """Return block-level statistics if exposed, or fallback estimates."""
        pass

    @abstractmethod
    async def apply_decision(self, decision: UnifiedDecision) -> Dict[str, Any]:
        """Apply a cache decision to the engine. Returns status/recommendation-only."""
        pass


class ICacheMetadataRepository(ABC):
    """Contract for KV cache metadata persistence and retrieval."""

    @abstractmethod
    async def save_block(self, block: KVBlockStats) -> None:
        pass

    @abstractmethod
    async def get_block(self, block_id: str) -> Optional[KVBlockStats]:
        pass

    @abstractmethod
    async def update_block(self, block: KVBlockStats) -> None:
        pass

    @abstractmethod
    async def delete_block(self, block_id: str) -> bool:
        pass

    @abstractmethod
    async def list_blocks(
        self, tenant_id: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[KVBlockStats]:
        pass

    @abstractmethod
    async def record_access(self, block_id: str, request_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def record_reuse(self, block_id: str) -> None:
        pass

    @abstractmethod
    async def record_hit(self, block_id: str) -> None:
        pass

    @abstractmethod
    async def record_miss(self, block_id: str) -> None:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass


class IImportanceScorer(ABC):
    """Contract for calculating normalized block importance scores."""

    @abstractmethod
    def compute_importance(self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None) -> float:
        """Compute score in range [0.0, 1.0]."""
        pass


class IPolicyEngine(ABC):
    """Contract for evaluating cache decisions based on state, scoring, and constraints."""

    @abstractmethod
    def evaluate(
        self,
        block: KVBlockStats,
        gpu_stats: GPUStats,
        importance_score: float,
        constraints: Optional[PolicyConstraints] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Recommendation:
        pass


class IReusePredictor(ABC):
    """Contract for predicting future KV block reuse likelihood."""

    @abstractmethod
    def predict(self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None) -> Prediction:
        pass


class IPlacementPlanner(ABC):
    """Contract for determining physical location placement."""

    @abstractmethod
    def plan_placement(
        self,
        block: KVBlockStats,
        gpu_stats: GPUStats,
        importance: float,
        reuse_prob: float,
    ) -> PlacementDecision:
        pass


class ISecurityPolicyEngine(ABC):
    """Contract for multi-tenant isolation and ACL enforcement."""

    @abstractmethod
    def authorize_access(
        self,
        requesting_tenant: str,
        target_block: KVBlockStats,
        operation: str = "read",
    ) -> SecurityAction:
        pass


class ICostOptimizer(ABC):
    """Contract for estimating and optimizing infrastructure economic costs."""

    @abstractmethod
    def calculate_cost_breakdown(
        self,
        gpu_stats: GPUStats,
        total_blocks: int,
        cached_tokens: int,
        active_hours: float = 1.0,
    ) -> CostBreakdown:
        pass
