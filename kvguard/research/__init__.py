"""Experimental and advanced research modules for Phase 5."""

from kvguard.research.cross_engine import CrossEngineKVBridge
from kvguard.research.distributed_kv import DistributedKVManager
from kvguard.research.multimodal import MultimodalKVManager
from kvguard.research.position_independent import PositionIndependentReuse
from kvguard.research.semantic_reuse import SemanticReuseEngine

__all__ = [
    "SemanticReuseEngine",
    "PositionIndependentReuse",
    "MultimodalKVManager",
    "DistributedKVManager",
    "CrossEngineKVBridge",
]
