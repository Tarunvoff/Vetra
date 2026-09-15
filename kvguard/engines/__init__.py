"""Inference engine adapters and registry."""

from kvguard.core.registry import EngineRegistry
from kvguard.engines.base import BaseInferenceEngineAdapter
from kvguard.engines.vllm.adapter import VLLMAdapter
from kvguard.engines.sglang.adapter import SGLangAdapter
from kvguard.engines.tensorrt_llm.adapter import TensorRTLLMAdapter

# Register all engine adapters
EngineRegistry.register("vllm", VLLMAdapter)
EngineRegistry.register("sglang", SGLangAdapter)
EngineRegistry.register("tensorrt_llm", TensorRTLLMAdapter)

__all__ = [
    "BaseInferenceEngineAdapter",
    "VLLMAdapter",
    "SGLangAdapter",
    "TensorRTLLMAdapter",
    "EngineRegistry",
]
