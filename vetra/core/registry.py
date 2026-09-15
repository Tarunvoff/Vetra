"""Engine and component registry for runtime dependency injection."""

from typing import Dict, Type
from vetra.core.enums import EngineType
from vetra.core.interfaces import IInferenceEngineAdapter


class EngineRegistry:
    """Registry holding available inference engine adapter classes."""

    _adapters: Dict[str, Type[IInferenceEngineAdapter]] = {}

    @classmethod
    def register(cls, engine_name: str, adapter_cls: Type[IInferenceEngineAdapter]) -> None:
        """Register an adapter class by engine name."""
        cls._adapters[engine_name.lower()] = adapter_cls

    @classmethod
    def get(cls, engine_name: str) -> Type[IInferenceEngineAdapter]:
        """Retrieve the adapter class for a given engine name."""
        name = engine_name.lower()
        if name not in cls._adapters:
            raise KeyError(f"No adapter registered for engine '{engine_name}'. Available: {list(cls._adapters.keys())}")
        return cls._adapters[name]

    @classmethod
    def list_engines(cls) -> list[str]:
        """List all registered engine names."""
        return list(cls._adapters.keys())
