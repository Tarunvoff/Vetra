"""Experimental and advanced research modules for Phase 5."""

from vetra.research.cross_engine import CrossEngineKVBridge
from vetra.research.distributed_kv import DistributedKVManager
from vetra.research.multimodal import MultimodalKVManager
from vetra.research.position_independent import PositionIndependentReuse
from vetra.research.semantic_reuse import SemanticReuseEngine

__all__ = [
    "SemanticReuseEngine",
    "PositionIndependentReuse",
    "MultimodalKVManager",
    "DistributedKVManager",
    "CrossEngineKVBridge",
]
