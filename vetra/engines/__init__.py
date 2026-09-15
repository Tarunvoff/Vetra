"""Inference engine adapters and registry."""

from vetra.core.registry import EngineRegistry
from vetra.engines.base import BaseInferenceEngineAdapter
from vetra.engines.vllm.adapter import VLLMAdapter
from vetra.engines.sglang.adapter import SGLangAdapter
from vetra.engines.tensorrt_llm.adapter import TensorRTLLMAdapter

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
