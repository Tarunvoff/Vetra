"""Core enumerations for the Vetra control plane."""

from enum import Enum


class CacheLocation(str, Enum):
    """Current or target physical location of a KV cache block/tensor."""

    GPU = "GPU"
    CPU = "CPU"
    REMOTE = "REMOTE"
    EVICTED = "EVICTED"


class DecisionType(str, Enum):
    """Action recommended or decided by the Vetra policy engine."""

    KEEP = "KEEP"
    OFFLOAD_CPU = "OFFLOAD_CPU"
    PREFETCH = "PREFETCH"
    EVICT = "EVICT"
    QUANTIZE = "QUANTIZE"
    NO_OP = "NO_OP"


class QuantizationPrecision(str, Enum):
    """KV cache quantization format."""

    FP16 = "FP16"
    BF16 = "BF16"
    INT8 = "INT8"
    INT4 = "INT4"
    NONE = "NONE"


class ModalityType(str, Enum):
    """Data modality for multimodal KV cache objects."""

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class SecurityAction(str, Enum):
    """Authorization decisions for tenant cache access."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    AUDIT_ONLY = "AUDIT_ONLY"


class EngineType(str, Enum):
    """Supported or stubbed inference backend engines."""

    VLLM = "vllm"
    SGLANG = "sglang"
    TENSORRT_LLM = "tensorrt_llm"
    SIMULATED = "simulated"


class ExecutionMode(str, Enum):
    """Runtime operational mode for Vetra."""

    DEVELOPMENT = "development"
    SIMULATION = "simulation"
    BENCHMARK = "benchmark"
    PRODUCTION = "production"
    RESEARCH = "research"


class FeatureStatus(str, Enum):
    """Implementation maturity marker."""

    IMPLEMENTED = "IMPLEMENTED"
    SIMULATED = "SIMULATED"
    STUB = "STUB"
    RESEARCH = "RESEARCH"
